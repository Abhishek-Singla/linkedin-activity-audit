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

Optional follow-ups it can do when you ask:

- Propose invitations older than a threshold to withdraw, and withdraw them after you confirm the list.
- Delete a stray draft after you confirm it.
- Check a named list of people for pending / connected / neither.

## What is inside

```
skills/linkedin-activity-audit/
  SKILL.md                         the skill
  references/pages-and-gotchas.md  URLs and the quirks of each LinkedIn page
  references/report-template.md    report structure
```

## Notes and limits

- LinkedIn changes its UI often. The page quirks in `pages-and-gotchas.md` were observed in 2026 and may need updating.
- The sent-invitations list is virtualised; the skill uses real scrolling to read all of it.
- It can only see what the signed-in browser can see. It cannot see activity on other devices, likes and comments, or history LinkedIn does not show.
- Use it on your own account. LinkedIn's terms restrict automated access; this skill is intended for a person reviewing their own account through their own signed-in browser, not for bulk scraping or outreach automation.

## License

MIT
