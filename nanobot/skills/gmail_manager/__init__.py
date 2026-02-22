"""Gmail Manager Skill - Complete email operations"""

from .gmail_manager import (
    gmail_manager,
    check_unread,
    list_emails,
    read_email,
    send_email,
    search_emails,
    get_unread_count,
    apply_label,
    archive_email,
    delete_email,
    list_labels,
    create_label,
    download_attachment,
    check_connection
)

__all__ = [
    'gmail_manager',
    'check_unread',
    'list_emails',
    'read_email',
    'send_email',
    'search_emails',
    'get_unread_count',
    'apply_label',
    'archive_email',
    'delete_email',
    'list_labels',
    'create_label',
    'download_attachment',
    'check_connection'
]

__version__ = "1.0.0"
__codename__ = "Postmaster"
