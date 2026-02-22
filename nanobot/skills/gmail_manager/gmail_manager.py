#!/usr/bin/env python3
"""
Gmail Manager
Complete Gmail management via IMAP/SMTP
"""

import os
import sys
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Dict, Optional
import re
from datetime import datetime


class GmailManager:
    """Complete Gmail manager via IMAP/SMTP"""

    def __init__(self, credentials_path: str = None):
        """Initialize Gmail manager

        Args:
            credentials_path: Path to secrets file (default: ~/.nanobot/workspace/memory/SECRETS.md)
        """
        self.credentials_path = credentials_path or "~/.nanobot/workspace/memory/SECRETS.md"
        self._credentials = self._load_credentials()
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.imap_port = 993
        self.smtp_port = 587

    def _load_credentials(self) -> Dict[str, str]:
        """Load Gmail credentials from secure file"""
        cred_path = Path(self.credentials_path).expanduser()

        if not cred_path.exists():
            raise FileNotFoundError(
                f"Gmail credentials not found at {cred_path}\n"
                f"\nPlease run: ~/Documents/Nanodata/SETUP_GMAIL.sh\n"
                f"Or create manually:\n"
                f"  nano ~/.nanobot/workspace/memory/SECRETS.md\n"
                f"  chmod 600 ~/.nanobot/workspace/memory/SECRETS.md\n"
                f"  echo 'SECRETS.md' >> ~/.nanobot/.gitignore"
            )

        # Check permissions
        stat = cred_path.stat()
        if stat.st_mode & 0o077:
            print(f"⚠️  Warning: Permissions on {cred_path} are too open.")
            print(f"   Fix with: chmod 600 {cred_path}")

        try:
            with open(cred_path, "r") as f:
                content = f.read()

            # Parse simple format
            address = self._find_value(content, "GMAIL_ADDRESS")
            password = self._find_value(content, "GMAIL_PASSWORD")

            if not address or not password:
                raise ValueError(
                    "Could not find GMAIL_ADDRESS or GMAIL_PASSWORD in credentials file"
                )

            return {"address": address, "password": password}
        except Exception as e:
            raise RuntimeError(f"Error loading credentials: {e}")

    def _find_value(self, content: str, key: str) -> Optional[str]:
        """Find value in credentials file"""
        # Find line with key: value
        import re

        pattern = rf"{key}:\s*(.+)"
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def get_unread_count(self, folder: str = "INBOX") -> int:
        """Get unread email count"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select(folder)

            # Search for unread
            typ, data = mail.search(None, "UNSEEN")
            if typ == "OK":
                unread_ids = data[0].split()
                mail.logout()
                return len(unread_ids)

            mail.logout()
            return 0

        except Exception as e:
            return f"❌ Error checking unread: {e}"

    def list_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        """List recent emails"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select(folder)

            # Search for all
            typ, data = mail.search(None, "ALL")
            if typ != "OK":
                mail.logout()
                return []

            email_ids = data[0].split()
            # Get most recent
            recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids

            emails = []
            for eid in recent_ids:
                typ, msg_data = mail.fetch(eid, "(RFC822)")
                if typ == "OK":
                    msg = email.message_from_bytes(msg_data[0][1])
                    emails.append(self._parse_email(msg, eid.decode()))

            mail.logout()
            return emails

        except Exception as e:
            return [f"❌ Error listing emails: {e}"]

    def _parse_email(self, msg, msg_id: str) -> Dict[str, str]:
        """Parse email message"""
        try:
            subject = msg["Subject"] or "(No Subject)"
            sender = msg["From"] or "Unknown"
            to = msg.get("To") or "Unknown"
            date = msg.get("Date") or "Unknown"

            # Get body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                            break
                        except:
                            continue
            else:
                if msg.get_content_type() == "text/plain":
                    try:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="replace")
                    except:
                        body = "(Unreadable body)"

            # Truncate long body
            if len(body) > 500:
                body = body[:500] + "..."

            return {
                "id": msg_id,
                "subject": subject,
                "from": sender,
                "to": to,
                "date": date,
                "body": body or "(Empty body)",
                "has_attachments": bool(msg.get_content_type() == "multipart/mixed"),
            }
        except Exception as e:
            return {
                "id": msg_id,
                "subject": f"Parse Error: {e}",
                "from": "Unknown",
                "to": "Unknown",
                "date": "Unknown",
                "body": "",
                "has_attachments": False,
            }

    def read_email(self, email_id: str, folder: str = "INBOX") -> Dict[str, str]:
        """Read specific email by ID"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select(folder)

            typ, msg_data = mail.fetch(email_id, "(RFC822)")
            if typ == "OK":
                msg = email.message_from_bytes(msg_data[0][1])
                result = self._parse_email(msg, email_id)
                mail.logout()
                return result

            mail.logout()
            return {"error": f"Email {email_id} not found"}

        except Exception as e:
            return {"error": str(e)}

    def send_email(self, to: str, subject: str, body: str, attachments: List[str] = None) -> str:
        """Send email with optional attachments"""
        try:
            msg = MIMEMultipart()
            msg["From"] = self._credentials["address"]
            msg["To"] = to
            msg["Subject"] = subject

            # Body
            msg.attach(MIMEText(body, "plain"))

            # Attachments
            if attachments:
                for filepath in attachments:
                    if Path(filepath).exists():
                        part = MIMEBase("application", "octet-stream")
                        with open(filepath, "rb") as f:
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition", f"attachment; filename={Path(filepath).name}"
                        )
                        msg.attach(part)

            # Send via SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self._credentials["address"], self._credentials["password"])

            text = msg.as_string()
            server.sendmail(self._credentials["address"], to, text)
            server.quit()

            return f"✅ Email sent to {to}"

        except Exception as e:
            return f"❌ Send error: {e}"

    def search_emails(self, query: str, folder: str = "INBOX", limit: int = 20) -> List[Dict]:
        """Search emails by query"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select(folder)

            # Build search query
            # Common searches: FROM, SUBJECT, BODY, TEXT
            search_criteria = f'TEXT "{query}"'
            typ, data = mail.search(None, search_criteria)

            if typ == "OK":
                email_ids = data[0].split()
                # Get most recent matches
                matched_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids

                results = []
                for eid in matched_ids:
                    typ, msg_data = mail.fetch(eid, "(RFC822)")
                    if typ == "OK":
                        msg = email.message_from_bytes(msg_data[0][1])
                        results.append(self._parse_email(msg, eid.decode()))

                mail.logout()
                return results

            mail.logout()
            return []

        except Exception as e:
            return [f"❌ Search error: {e}"]

    def apply_label(self, email_id: str, label: str) -> str:
        """Apply label to email"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select()

            # Store label
            typ, _ = mail.store(email_id, "+X-GM-LABELS", label)
            if typ == "OK":
                mail.logout()
                return f"✅ Label '{label}' applied to {email_id}"

            mail.logout()
            return f"⚠️  Could not apply label"

        except Exception as e:
            return f"❌ Label error: {e}"

    def archive_email(self, email_id: str) -> str:
        """Archive email (move to All Mail)"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select()

            # Gmail archive: move to '[Gmail]/All Mail'
            mail.store(email_id, "+X-GM-LABELS", "\\Archive")
            typ, _ = mail.copy(email_id, "[Gmail]/All Mail")
            if typ == "OK":
                mail.store(email_id, "+FLAGS", "\\Deleted")
                mail.expunge()

            mail.logout()
            return f"✅ Email {email_id} archived"

        except Exception as e:
            return f"❌ Archive error: {e}"

    def delete_email(self, email_id: str) -> str:
        """Delete email permanently"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.select()

            mail.store(email_id, "+FLAGS", "\\Deleted")  # Mark for deletion
            mail.expunge()  # Permanently delete
            mail.logout()

            return f"✅ Email {email_id} deleted"

        except Exception as e:
            return f"❌ Delete error: {e}"

    def list_labels(self) -> List[str]:
        """List all Gmail labels"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])

            typ, labels = mail.list()
            if typ == "OK":
                mail.logout()
                label_names = []
                for label in labels:
                    # Decode label names
                    try:
                        label_str = label.decode()
                        match = re.search(r'"([^"]+)"', label_str)
                        if match:
                            label_names.append(match.group(1))
                    except:
                        continue
                return label_names

            mail.logout()
            return []

        except Exception as e:
            return [f"❌ Labels error: {e}"]

    def check_connection(self) -> str:
        """Test Gmail connectivity"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self._credentials["address"], self._credentials["password"])
            mail.logout()
            return "✅ Gmail connection successful"
        except Exception as e:
            return f"❌ Connection error: {e}"


# Convenience functions for nanobot
gmail_manager = GmailManager()


def check_unread():
    """Check unread count (for nanobot)"""
    count = gmail_manager.get_unread_count()
    if isinstance(count, int):
        return f"📨 You have {count} unread Gmail messages"
    else:
        return str(count)


def list_emails(limit: int = 10):
    """List recent emails (for nanobot)"""
    emails = gmail_manager.list_emails("INBOX", limit)
    if isinstance(emails, list):
        if not emails:
            return "No emails found"

        result = f"📧 Recent {len(emails)} emails:\n"
        for i, email in enumerate(emails[:limit], 1):
            result += f"\n{i}. {email.get('subject', '(No Subject)')}\n"
            result += f"   From: {email.get('from', 'Unknown')}\n"
            result += f"   Date: {email.get('date', 'Unknown')[:40]}\n"
        result += "\nFor full email, use: read_email <id>"
        return result
    else:
        return f"❌ Error: {emails}"


def read_email(email_id: str):
    """Read specific email (for nanobot)"""
    email = gmail_manager.read_email(email_id)
    if isinstance(email, dict) and "error" not in email:
        result = f"📄 Email: {email.get('id')}\n"
        result += f"   From: {email.get('from')}\n"
        result += f"   Subject: {email.get('subject')}\n"
        result += f"   Date: {email.get('date')}\n"
        result += f"\n   Preview:\n   {email.get('body', '')[:300]}"
        return result
    else:
        return f"❌ Error: {email}"


def send_email(to: str, subject: str, body: str, attachments: str = None):
    """Send email (for nanobot)"""
    attach_list = [a.strip() for a in attachments.split(",")] if attachments else None
    return gmail_manager.send_email(to=to, subject=subject, body=body, attachments=attach_list)


def search_emails(query: str, limit: int = 10):
    """Search emails (for nanobot)"""
    emails = gmail_manager.search_emails(query, "INBOX", limit)
    if isinstance(emails, list):
        if not emails:
            return f"No emails found matching '{query}'"

        result = f"🔍 Found {len(emails)} emails matching '{query}':\n"
        for i, email in enumerate(emails[: min(limit, len(emails))], 1):
            result += f"\n{i}. {email.get('subject', '(No Subject)')}\n"
            result += f"   From: {email.get('from', 'Unknown')}\n"
        return result
    else:
        return f"❌ Error: {emails}"


def get_unread_count(parsed=None):
    """Get unread count (alias for nanobot)"""
    return check_unread()


def apply_label(email_id: str, label: str):
    """Apply label (for nanobot)"""
    return gmail_manager.apply_label(email_id, label)


def archive_email(email_id: str):
    """Archive email (for nanobot)"""
    return gmail_manager.archive_email(email_id)


def delete_email(email_id: str):
    """Delete email (for nanobot)"""
    return gmail_manager.delete_email(email_id)


def list_labels():
    """List labels (for nanobot)"""
    labels = gmail_manager.list_labels()
    if isinstance(labels, list):
        return "📂 Gmail Labels:\n\n" + "\n".join(f"  - {label}" for label in labels[:20])
    else:
        return f"❌ Error: {labels}"


def check_connection():
    """Check Gmail connection (for nanobot)"""
    return gmail_manager.check_connection()


if __name__ == "__main__":
    # Test connection
    result = check_connection()
    print(result)
