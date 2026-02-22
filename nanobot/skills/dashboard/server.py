#!/usr/bin/env python3
"""
Dashboard Server - Serves the Nanobot Dashboard UI and API
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from fastapi import FastAPI, APIRouter, Request, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from datetime import datetime


# Pydantic models
class Bookmark(BaseModel):
    """Bookmark model"""

    title: str
    url: str
    folder: str = "General"
    tags: str = ""
    created: str = ""
    id: int = 0


class ChatMessage(BaseModel):
    """Chat message model"""

    message: str
    role: str = "user"
    timestamp: str = ""


class Task(BaseModel):
    """Task model"""

    name: str
    status: str = "running"
    created: str = ""
    id: str = ""


class Reminder(BaseModel):
    """Reminder model"""

    title: str
    date: str
    type: str = "once"
    id: str = ""


class DashboardServer:
    def __init__(self, workspace_dir: str):
        """Initialize dashboard server"""
        self.workspace_dir = Path(workspace_dir)
        self.data_dir = self.workspace_dir / "dashboard" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Initialize data files
        self._init_data_files()

        self.app = FastAPI(title="Nanobot Dashboard", version="2.0")
        self.router = APIRouter()

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Setup routes
        self._setup_routes()

        # Mount static files
        self._mount_static_files()

    def _init_data_files(self):
        """Initialize empty data files"""
        files = {"bookmarks.json": [], "chat.json": [], "tasks.json": [], "schedule.json": []}

        for filename, default_data in files.items():
            filepath = self.data_dir / filename
            if not filepath.exists():
                with open(filepath, "w") as f:
                    json.dump(default_data, f, indent=2)

    def _read_json(self, filename: str) -> List[Any]:
        """Read JSON data file"""
        filepath = self.data_dir / filename
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_json(self, filename: str, data: List[Any]):
        """Write JSON data file"""
        filepath = self.data_dir / filename
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _setup_routes(self):
        """Setup API routes"""

        # Health check
        @self.router.get("/health")
        async def health_check():
            return {"status": "OK", "timestamp": time.time()}

        # Bookmark routes
        @self.router.get("/bookmarks")
        async def get_bookmarks():
            return self._read_json("bookmarks.json")

        @self.router.post("/bookmarks")
        async def add_bookmark(bookmark: Bookmark):
            bookmarks = self._read_json("bookmarks.json")
            bookmark.id = int(time.time())
            bookmark.created = datetime.now().isoformat()

            # Validate URL
            if not bookmark.url.startswith(("http://", "https://")):
                bookmark.url = "https://" + bookmark.url

            bookmarks.append(bookmark.dict())
            self._write_json("bookmarks.json", bookmarks)
            return {"success": True, "id": bookmark.id}

        @self.router.put("/bookmarks/{bookmark_id}")
        async def update_bookmark(bookmark_id: int, bookmark: Bookmark):
            bookmarks = self._read_json("bookmarks.json")
            for i, bm in enumerate(bookmarks):
                if bm.get("id") == bookmark_id:
                    bookmark_dict = bookmark.dict()
                    bookmark_dict["id"] = bookmark_id
                    bookmark_dict["created"] = bm.get("created", "")
                    bookmarks[i] = bookmark_dict
                    self._write_json("bookmarks.json", bookmarks)
                    return {"success": True}
            raise HTTPException(status_code=404, detail="Bookmark not found")

        @self.router.delete("/bookmarks/{bookmark_id}")
        async def delete_bookmark(bookmark_id: int):
            bookmarks = self._read_json("bookmarks.json")
            bookmarks = [bm for bm in bookmarks if bm.get("id") != bookmark_id]
            self._write_json("bookmarks.json", bookmarks)
            return {"success": True}

        # Chat routes
        @self.router.get("/chat")
        async def get_chat_history():
            return self._read_json("chat.json")

        @self.router.post("/chat")
        async def send_message(msg: ChatMessage):
            chat = self._read_json("chat.json")
            msg.timestamp = datetime.now().isoformat()
            chat.append(msg.dict())
            # Keep only last 50 messages
            chat = chat[-50:]
            self._write_json("chat.json", chat)
            return {"success": True}

        # Task routes
        @self.router.get("/tasks")
        async def get_tasks():
            return self._read_json("tasks.json")

        # Schedule routes
        @self.router.get("/schedule")
        async def get_schedule():
            return self._read_json("schedule.json")

        # Topology routes
        @self.router.get("/topology")
        async def get_topology():
            """Get dynamic topology of nanobot infrastructure"""
            data = self._scan_nanobot_structure()
            return data

        @self.router.get("/topology/refresh")
        async def refresh_topology():
            """Refresh topology data"""
            return await get_topology()

        # Mount router
        self.app.include_router(self.router, prefix="/dashboard/api")

    def _scan_nanobot_structure(self) -> Dict[str, Any]:
        """Scan nanobot directory structure to build topology"""
        scan_data = {
            "skills": [],
            "channels": [],
            "providers": [],
            "tools": [],
            "timestamp": datetime.now().isoformat(),
        }

        # Get skills
        skills_dir = Path("/Users/adam/Documents/Nanobot/nanobot/skills")
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skill_name = skill_dir.name
                    try:
                        # Read SKILL.md to get description
                        skill_path = skill_dir / "SKILL.md"
                        with open(skill_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Extract first line or simple description
                            lines = content.split("\n")
                            description = "No description"
                            for line in lines:
                                if line.strip() and not line.startswith("#"):
                                    description = line.strip()
                                    break
                    except:
                        description = "No description"

                    scan_data["skills"].append(
                        {"name": skill_name, "description": description, "status": "active"}
                    )

        # Get channels from config
        config_path = Path("/Users/adam/.nanobot/config.json")
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    if "channels" in config:
                        for channel_name, channel_config in config["channels"].items():
                            if channel_config.get("enabled", False):
                                scan_data["channels"].append(
                                    {"name": channel_name, "status": "enabled"}
                                )
            except:
                pass

        # Get providers from config
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    if "providers" in config:
                        for provider_name, provider_config in config["providers"].items():
                            if provider_config and provider_config.get("apiKey"):
                                scan_data["providers"].append(
                                    {"name": provider_name, "status": "configured"}
                                )
            except:
                pass

        return scan_data

    def _mount_static_files(self):
        """Mount static files and dashboard page"""

        # Serve the dashboard HTML
        @self.app.get("/dashboard", response_class=FileResponse)
        async def serve_dashboard():
            template_path = Path(
                "/Users/adam/Documents/Nanobot/nanobot/skills/dashboard/templates/index.html"
            )
            return template_path

        @self.app.get("/", response_class=RedirectResponse)
        async def redirect_to_dashboard():
            return RedirectResponse(url="/dashboard")

        # Mount CSS and JS
        self.app.mount(
            "/dashboard/static",
            StaticFiles(
                directory="/Users/adam/Documents/Nanobot/nanobot/skills/dashboard/templates/"
            ),
            name="dashboard-static",
        )

        # Also serve from root for backward compatibility
        self.app.mount(
            "/",
            StaticFiles(
                directory="/Users/adam/Documents/Nanobot/nanobot/skills/dashboard/templates/"
            ),
            name="root-static",
        )

    def run(self, host: str = "0.0.0.0", port: int = 18790):
        """Run the dashboard server"""
        uvicorn.run(self.app, host=host, port=port)


# CLI entry point
if __name__ == "__main__":
    import sys

    workspace = sys.argv[1] if len(sys.argv) > 1 else "~/.nanobot/workspace"
    server = DashboardServer(workspace)
    server.run()
