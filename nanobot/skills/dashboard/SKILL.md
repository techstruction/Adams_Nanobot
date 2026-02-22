# Dashboard Skill

Serve an interactive web-based dashboard for monitoring and managing nanobot.

## Features

- **Gateway Monitoring**: Real-time system status, LLM provider status, API connections, memory usage
- **Bookmark Manager**: Save, organize, and manage URLs with folders and tags
- **Task Queue**: Monitor active tasks and their status
- **Schedule & Reminders**: View and manage scheduled jobs and reminders
- **Chat Interface**: ChatGPT-style interface with file upload support
- **Topology Visualization**: Dynamic map of skills, channels, providers, and tools

## Usage

```bash
# Start the dashboard server
nanobot dashboard

# Dashboard will be available at http://localhost:18790/dashboard
```

## Data Storage

The dashboard stores data in JSON files at `~/.nanobot/workspace/dashboard/data/`:
- `bookmarks.json` - Bookmark entries
- `chat.json` - Chat history
- `schedule.json` - Scheduled reminders
- `tasks.json` - Active tasks

## API Endpoints

- `GET /dashboard/api/bookmarks` - List all bookmarks
- `POST /dashboard/api/bookmarks` - Add new bookmark
- `PUT /dashboard/api/bookmarks/:id` - Update bookmark
- `DELETE /dashboard/api/bookmarks/:id` - Delete bookmark
- `GET /dashboard/api/tasks` - List active tasks
- `GET /dashboard/api/schedule` - List schedule/reminders
- `GET /dashboard/api/topology` - Get topology data
- `POST /dashboard/api/chat` - Send chat message
- `GET /dashboard/api/chat` - Get chat history
