# Outreach DMs and the tracker

Use this only when the user explicitly asks to send a batch of messages. These are real messages sent in the user's name.

## Preconditions (all must be true)

1. The user explicitly authorised sending in this conversation, for this batch.
2. The message text is the user's approved text. Do not rewrite it, add to it, or send a second message.
3. Recipients are either named by the user or the user explicitly delegated the choice to you.
4. The correct Chrome profile is selected and signed in (see SKILL.md). Never enter credentials.
5. Each recipient is a **1st-degree connection**. Without Premium, LinkedIn does not allow messaging 2nd or 3rd-degree people. Do not substitute InMail, connection-request notes or other workarounds without the user asking.

## Choosing recipients (when delegated)

- Search people with the network filter for 1st-degree connections and a keyword for the company plus the role:
  `https://www.linkedin.com/search/results/people/?keywords=<company>%20<role>&network=%5B%22F%22%5D&origin=FACETED_SEARCH`
- Read results with the page-text tool. Each result shows degree, headline, location and a Message button.
- Pick one person per company: a current employee, the role closest to what the user asked for, the location the user prefers.
- If a company has no 1st-degree connection, skip it and say so. Do not pick someone from another company to fill the quota.
- Show the user the chosen list (name, headline, company, city) before sending. Say plainly when a pick is a weaker fit (for example a marketing role when product was requested).

## Sending

1. Open the person's profile (or the Message button in the search result).
2. Type the approved text with only the first-name placeholder replaced.
3. Do not attach files unless the user asked. Many first DMs deliberately do not attach anything.
4. Send, then confirm the message appears as sent in the thread.
5. If anything looks off (wrong person, a dialog you did not expect, a send that may not have landed), stop and check before continuing. Never send twice to be safe.

## Tracker sheet

Create or update a workbook with these columns so the user can follow up:

| Column | Notes |
|---|---|
| # | running number |
| Company | |
| LinkedIn search term | what was searched |
| Contact name | chosen recipient |
| Contact profile URL | |
| DM draft | approved text, with the placeholder |
| Attachment | none / file name |
| Sent date | |
| Replied? | Yes / No (dropdown) |
| Reply date | |
| Status | Not sent / Sent / Replied / Referral given / Interview / Closed - no reply / Closed - declined (dropdown) |
| Next step / notes | |

Add a second sheet "Before sending" with the user's own checklist (resume version to attach later, placeholder replacement, relocation or availability wording, realistic reply rates of about 10-20% for cold DMs, and the 3-week re-invite block after a withdrawal).

Keep the tracker in the user's own folder, not in a public repository: it contains names.

## Reporting

Return a table: company, person, sent or skipped, reason. Say how many were sent out of how many were requested.
