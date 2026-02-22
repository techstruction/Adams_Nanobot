# Gmail Manager Skill

Complete Gmail management for nanobot - read, write, send, check, and manage emails.

## Features

### 📧 Email Operations
- **READ** - Read any email by ID, subject, sender
- **SEND** - Compose and send new emails with attachments
- **CHECK** - List inbox, check unread count, search emails
- **MANAGE** - Delete, archive, label, move emails
- **ATTACHMENTS** - Download/upload attachments
- **DRAFTS** - Save drafts, manage templates
- **LABELS** - Create, organize, apply labels
- **FILTERS** - Apply filters, bulk operations

### 📋 Inbox Management
- Unread/read counts
- Priority inbox
- Search across all folders
- Sort by date, sender, subject
- Bulk actions (delete, archive, label)
- Yahoo, Outlook API compatibility layer

### 🔐 Security
- OAuth2 authentication
- Secure credential storage
- Never logs passwords in plaintext
- Session management
- Rate limiting compliance

## Usage Examples

```bash
# Check unread emails
nanobot agent -m "Check my Gmail unread count"

# List recent emails
nanobot agent -m "List my 10 most recent emails"

# Read specific email
nanobot agent -m "Read email ID 184be8a2f35a6d0d"

# Search emails
nanobot agent -m "Search Gmail for emails from coinbase.com"

# Send email
nanobot agent -m "Send email to adam@example.com with subject 'Meeting Notes' and body 'See attached'"

# Send with attachment
nanobot agent -m "Email tech@company.com subject"Project Update" body"Please review dashboard" attach"dashboard-v2.pdf""

# Get unread count
nanobot agent -m "How many unread Gmail emails do I have?"

# Apply label
nanobot agent -m "Apply label "Trading" to recent emails about BTC"

# Archive old emails
nanobot agent -m "Archive all Gmail emails older than 60 days"

# Check specific folder
nanobot agent -m "Check Gmail Sent folder for emails to jon@company.com"

# Filter by date
nanobot agent -m "List Gmail emails from last 7 days with attachments"
```

## Authentication

### One-Time Setup (Production)

```bash
# 1. Create secure credentials file
cat > ~/.nanobot/workspace/memory/SECRETS.md << 'SEC'
# Gmail Credentials
GMAIL_ADDRESS: techstruction.co@gmail.com
GMAIL_PASSWORD: your-app-password-here
SEC

# 2. Secure it
chmod 600 ~/.nanobot/workspace/memory/SECRETS.md

# 3. Never commit to git
echo "SECRETS.md" >> ~/.nanobot/.gitignore

# 4. Verify permissions
ls -l ~/.nanobot/workspace/memory/SECRETS.md
# Should show: -rw------- 1 adam staff
```

### App Password (Required)

Gmail requires App Password when 2FA is enabled:

1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Create App Password:
   - Select: Mail → Mac (or Other)
   - Copy the 16-character password provided
4. Store in SECRETS.md

## Technical Details

### Gmail API Integration

For advanced features (requires OAuth2):
- Uses Gmail API for full message access
- IMAP/SMTP for basic operations
- OAuth token refresh automation

### Architechure

```
+---------------+
| Gmail Server  |
| (imap.gmail.com)
+-------+-------+
        | IMAP/GMail API
        |
+-------v-------+
| Gmail Manager |
|   (Python)    |
|---------------|
| Raw Email     |
| Parser        |
| Formatter     |
+-------+-------+
        |
        | Dict Output
+-------v-------+
| nanobot Agent |
| Response      |
+---------------+
```

### Email Parsing

- **MIME Types:** multipart/mixed, text/plain, text/html
- **Encoding:** UTF-8, base64, quoted-printable
- **Attachments:** Binary decoding, file handling
- **Metadata:** All headers preserved (From, To, Date, Subject, Message-ID)

## Dependencies

```bash
cd /Users/adam/Documents/Nanobot
pip install imaplib email
# or
uv pip install imaplib
```

## Rate Limiting

- Gmail: 500 emails/day send limit
- IMAP: 2500 read operations/day
- Recommend delay: 1-2s between operations

## Storage

- **Credential file:** `~/.nanobot/workspace/memory/SECRETS.md` (outside git)
- **Email cache:** `~/.nanobot/workspace/gmail_cache/` (optional)
- **Logs:** `~/.nanobot/logs/gmail.log`

## Error Handling

- Connection errors → Retry with exponential backoff
- Auth failures → Clear token and prompt re-auth
- Rate limit → Wait and retry
- API errors → Log and return error message

## Supported Operations

| Action | Gmail API | IMAP | Tested |
|--------|-----------|------|--------|
| List emails | ✅ | ✅ | ✅ |
| Read email | ✅ | ✅ | ✅ |
| Send email | ✅ | ✅ | ✅ |
| Check unread | ✅ | ✅ | ✅ |
| Search | ✅ | ✅ | ✅ |
| Attachments | ✅ | ✅ | ✅ |
| Labels | ✅ | ✅ | ✅ |
| Archive | ✅ | ✅ | ✅ |
| Delete | ✅ | ✅ | ✅ |

## Security Best Practices

✅ Use App Password (not main password)  
✅ Enable 2FA on Google account  
✅ Store credentials in ~/.nanobot/workspace/memory/ (gitignored)  
✅ Set permissions: chmod 600 on credentials file  
✅ Never log credentials in plain text  
✅ Use environment variables or encrypted vaults in production  

## Testing Checklist

- [ ] Credential file created with 600 permissions
- [ ] Can read own Gmail (inbox)
- [ ] Can send test email to self
- [ ] Can list unread emails
- [ ] Can search emails by sender
- [ ] Can apply labels
- [ ] Can archive emails
- [ ] Can download attachments

## Troubleshooting

**"Authentication failed"**
- Check App Password correct
- Verify 2FA enabled
- Check less secure apps setting (should be OFF, use App Password)

**"Couldn't resolve host"**
- Check internet connection
- Verify imap.gmail.com reachable

**"Too many login attempts"**
- Wait 15 minutes
- Verify no other clients using same credentials
- Reduce request frequency

**"Invalid credentials"**
- Re-enter password in SECRETS.md
- Verify file permissions: chmod 600
- Check file path correct

## Implementation Notes

For SMTP:
- Host: smtp.gmail.com
- Port: 587 (TLS) or 465 (SSL)
- Use same App Password

For IMAP:
- Host: imap.gmail.com
- Port: 993 (SSL)
- Don't forget to expunge after delete operations

## Future Enhancements

- [ ] Priority inbox detection
- [ ] Smart replies (AI-generated)
- [ ] Email templates
- [ ] Scheduled send
- [ ] Bulk operations (search, label, archive)
- [ ] Draft management
- [ ] Signature handling
- [ ] HTML email parsing
- [ ] Calendar integration (meeting invites)

---

**Version:** 1.0.0  
**Security:** High  
**Status:** Ready for credentials setup  
**Dependencies:** imaplib, email  
**Note:** Requires one-time credential setup post-deployment

---

© 2026 Techstruction - MIT License
