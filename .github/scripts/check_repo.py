#!/usr/bin/env python3
"""Repo checks: SKILL.md frontmatter validity and a privacy-pattern scan. Stdlib only."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", "node_modules"}
errors = []


def fail(msg):
    errors.append(msg)
    print(f"::error::{msg}")


# ---- 1. SKILL.md frontmatter ----
for skill in ROOT.glob("skills/*/SKILL.md"):
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    rel = skill.relative_to(ROOT)
    if not m:
        fail(f"{rel}: missing YAML frontmatter block")
        continue
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        fail(f"{rel}: name must be lowercase-hyphen, max 64 chars (got {name!r})")
    if name != skill.parent.name:
        fail(f"{rel}: name {name!r} does not match folder {skill.parent.name!r}")
    if not desc:
        fail(f"{rel}: description is empty")
    elif len(desc) > 1024:
        fail(f"{rel}: description is {len(desc)} chars (max 1024)")
    for ref in re.findall(r"`((?:references|scripts)/[^`\s]+)`", text):
        if not (skill.parent / ref).exists():
            fail(f"{rel}: referenced file {ref} does not exist")
if not list(ROOT.glob("skills/*/SKILL.md")):
    fail("no skills/*/SKILL.md found")

# ---- 2. privacy scan ----
ALLOWED_SLUGS = {"me", "old-slug", "new-slug", "your-slug", "your-name", "example"}
ALLOWED_EMAIL_DOMAINS = {"example.com", "example.org", "users.noreply.github.com"}
PATTERNS = [
    ("phone number", re.compile(r"(?<![\w.])(?:\+\d{1,3}[\s-]?)?(?:\d[\s-]?){10,12}(?![\w.])")),
    ("Drive/Docs link", re.compile(r"(?:drive|docs)\.google\.com/\S+")),
    ("local user path", re.compile(r"[A-Za-z]:\\+Users\\+[^\\\s]+|/(?:home|Users)/[^/\s]+/")),
    ("API key / token", re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16})\b")),
]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
LI = re.compile(r"linkedin\.com/in/([A-Za-z0-9_%-]+)")

for path in ROOT.rglob("*"):
    if not path.is_file() or any(p in SKIP_DIRS for p in path.parts) or path.name == "check_repo.py":
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    rel = path.relative_to(ROOT)
    for i, line in enumerate(text.splitlines(), 1):
        for label, rx in PATTERNS:
            if rx.search(line):
                fail(f"{rel}:{i}: possible {label}")
        for m in EMAIL.finditer(line):
            if m.group(1).lower() not in ALLOWED_EMAIL_DOMAINS:
                fail(f"{rel}:{i}: email address")
        for m in LI.finditer(line):
            if m.group(1).lower() not in ALLOWED_SLUGS:
                fail(f"{rel}:{i}: real-looking LinkedIn profile slug {m.group(1)!r}")

if errors:
    print(f"\n{len(errors)} problem(s) found")
    sys.exit(1)
print("All checks passed")