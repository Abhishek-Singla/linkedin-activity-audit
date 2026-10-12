# LinkedIn pages and gotchas

Everything here was learned by driving the pages with Claude in Chrome. LinkedIn changes its UI often, so treat selectors and layouts as hints and re-check.

## URLs

| Purpose | URL |
|---|---|
| Sent invitations | `https://www.linkedin.com/mynetwork/invitation-manager/sent/` |
| Received invitations | `https://www.linkedin.com/mynetwork/invitation-manager/received/` |
| Connections (recently added) | `https://www.linkedin.com/mynetwork/invite-connect/connections/` |
| Messaging | `https://www.linkedin.com/messaging/` |
| Your activity (posts) | `https://www.linkedin.com/in/me/recent-activity/all/` |
| Article manager | `https://www.linkedin.com/article/manage/drafts/` (also `/scheduled/`, `/published/`) |
| Post composer | `https://www.linkedin.com/feed/` then Start a post (or `/sharing/compose`) |

## Gotchas

### Sent invitations list is virtualised
- Only about 10 invitations are in the DOM at once. The header shows the true total as `People (N)`.
- Scrolling with JavaScript (`window.scrollTo`, `scrollTop`) does not trigger loading. A loop of those can freeze the tab and time out.
- What works: the browser tool's real mouse-wheel scroll, 10 ticks at a time, waiting a few seconds between, then `get_page_text`. The page text accumulates as you go (entries can repeat, so de-duplicate by name).
- There is no "Show more" button on this page.

### Posts vs articles
- The activity page lists posts only. Articles live in the article manager. "Nothing to see for now" on activity does not mean nothing was published.
- The "Drafts N" count in the profile card links to the article drafts, not post drafts.
- Editing a published article can leave a draft copy with the same title and an empty body.

### Messaging renders late
- The first `get_page_text` often returns nothing or only the shell. Wait a few seconds and read again.
- Thread previews prefixed with `You:` are messages the user sent. An "attachment" preview means the user sent a file.
- Sponsored messages appear at the top of the list and are not conversations the user started.

### Tabs freeze on heavy pages
- LinkedIn tabs in a background Chrome window can be slow or throttled. If a screenshot or JS call times out, wait a few seconds and retry. Do not loop retries.
- Keep one tab for the whole run and close it at the end.

### Do not open the composer to "look" without a plan
- Opening the composer and closing it with no text typed does not save anything. Do not type, and do not click Post.

### Sign-in
- A redirect to `/uas/login` means that Chrome profile is not signed in. Stop and ask the user to sign in themselves or choose another profile.

## Reading dates
- "Sent 3 weeks ago", "1 month ago", "7 months ago" are rounded buckets. Convert to approximate months for the report and say so.
