# linkedin-activity-audit

A Claude skill that audits what has been done on a LinkedIn account by reading it through the [Claude in Chrome](https://claude.com) browser extension, then writes a dated report.

It answers questions like:

- What connection requests are still pending, and how old are they?
- Who accepted recently?
- What messages did I send?
- Do I have any published posts or articles, drafts, or scheduled posts?
- Which invitations are stale enough to withdraw?

**Read-only by default.** It never sends, posts, withdraws or deletes anything unless you explicitly ask for that exact action, and it shows you what will be affected first.

## Install

### Claude Code (user-level skill)

Copy the skill folder into your skills directory:

```bash
git clone https://github.com/<your-username>/linkedin-activity-audit.git
cp -r linkedin-activity-audit/skills/linkedin-activity-audit ~/.claude/skills/
```

On Windows PowerShell:

```powershell
git clone https://github.com/<your-username>/linkedin-activity-audit.git
Copy-Item -Recurse linkedin-activity-audit\skills\linkedin-activity-audit $env:USERPROFILE\.claude\skills\
```

### Claude desktop / claude.ai

Zip the `skills/linkedin-activity-audit` folder and upload it as a custom skill.

## Requirements

- Claude with the Claude in Chrome extension connected.
- The Chrome profile you want to audit must already be signed in to LinkedIn. The skill never types credentials.

## Usage

Ask Claude something like:

> Audit my LinkedIn activity: pending invitations, recent connections, messages I sent, and any posts, articles, drafts or scheduled posts.

Follow-ups it can do when you ask (each one needs your explicit go-ahead, and it shows the exact targets first):

- **Withdraw stale invitations:** propose the pending invitations older than a threshold you choose, then withdraw them one at a time after you confirm the list. LinkedIn blocks re-inviting a withdrawn person for up to 3 weeks.
- **Delete a stray draft:** for example a leftover article draft, then confirm the published article is still there.
- **Send a batch of referral DMs** to 1st-degree connections you approve (or let it choose one per company), with your exact text, and record each send in a tracker workbook.
- **Check a named list** of people for pending / connected / neither.
- **Keep your profile URL consistent** across resume and cover-letter `.docx` files with a dry-run-first script that backs up every file.

## What is inside

```
skills/linkedin-activity-audit/
  SKILL.md                              the skill
  references/pages-and-gotchas.md       URLs and the quirks of each LinkedIn page
  references/report-template.md         report structure
  references/outreach-and-tracker.md    how to choose recipients, send, and track DMs
  scripts/update_linkedin_url.py        replace a profile URL across .docx files (dry-run by default)
```

### URL update script

```bash
# dry run: lists files that contain the old URL, changes nothing
python skills/linkedin-activity-audit/scripts/update_linkedin_url.py \
  --root "/path/to/resumes" --old linkedin.com/in/old-slug --new linkedin.com/in/new-slug

# apply: backs up each file first, edits text and hyperlinks, verifies, then swaps in
python skills/linkedin-activity-audit/scripts/update_linkedin_url.py \
  --root "/path/to/resumes" --old linkedin.com/in/old-slug --new linkedin.com/in/new-slug --apply
```

PDFs are not edited; re-export them from the updated `.docx` files.

## Permissions

Sending messages or withdrawing invitations changes your real account. Some Claude Code permission modes (for example Auto) refuse the browser steps that lead to sending a message, even if you said yes in chat. If that happens, switch the session to a mode where you approve each action (for example Manual), or start a new session in that mode. The skill will not change the permission mode itself.

## Notes and limits

- LinkedIn changes its UI often. The page quirks in `pages-and-gotchas.md` were observed in 2026 and may need updating.
- The sent-invitations list is virtualised; the skill uses real scrolling to read all of it.
- It can only see what the signed-in browser can see. It cannot see activity on other devices, likes and comments, or history LinkedIn does not show.
- Use it on your own account. LinkedIn's terms restrict automated access; this skill is intended for a person reviewing their own account through their own signed-in browser, not for bulk scraping or outreach automation.

## License

MIT
