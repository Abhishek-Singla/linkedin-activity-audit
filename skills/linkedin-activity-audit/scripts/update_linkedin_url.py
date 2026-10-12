#!/usr/bin/env python3
"""Replace a LinkedIn profile URL across .docx files, safely.

Dry-run by default. With --apply it:
  1. copies each file that needs a change into a backup folder (same relative path),
  2. rewrites the visible text AND hyperlink targets (document, headers, footers, rels),
  3. verifies the new file (zip integrity, no old URL left) before swapping it in.

Files where the URL is split across Word text runs are reported, not edited.
PDFs are not touched; re-export them from the updated .docx files.

Usage:
  python update_linkedin_url.py --root "C:/path/to/resumes" \
      --old linkedin.com/in/old-slug --new linkedin.com/in/new-slug          # dry run
  python update_linkedin_url.py ... --apply                                   # do it
"""
import argparse
import glob
import os
import re
import shutil
import sys
import zipfile


def xml_parts(z):
    return [n for n in z.namelist() if n.endswith(".xml") or n.endswith(".rels")]


def plain(xml):
    return re.sub(r"<[^>]+>", "", xml)


def scan(root, old, skip_dir):
    hits = []
    for f in glob.glob(os.path.join(root, "**", "*.docx"), recursive=True):
        if skip_dir and os.path.abspath(f).startswith(os.path.abspath(skip_dir)):
            continue
        if os.path.basename(f).startswith("~$"):
            continue
        try:
            z = zipfile.ZipFile(f)
        except Exception:
            continue
        plain_hits, split_parts = [], []
        for n in xml_parts(z):
            x = z.read(n).decode("utf8", "ignore")
            c = x.count(old)
            if c:
                plain_hits.append((n, c))
            elif old in plain(x):
                split_parts.append(n)
        z.close()
        if plain_hits or split_parts:
            hits.append((f, plain_hits, split_parts))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--old", required=True, help="e.g. linkedin.com/in/old-slug (no scheme)")
    ap.add_argument("--new", required=True, help="e.g. linkedin.com/in/new-slug (no scheme)")
    ap.add_argument("--backup", default=None, help="backup folder (default: <root>/_backup_before_linkedin_url_update)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    backup = a.backup or os.path.join(a.root, "_backup_before_linkedin_url_update")
    hits = scan(a.root, a.old, backup)
    split = [h for h in hits if h[2]]
    print(f"files containing the old URL: {len(hits)}")
    print(f"files with the URL split across runs (not edited): {len(split)}")
    for f, _, parts in split:
        print("  SPLIT:", os.path.relpath(f, a.root), parts)

    if not a.apply:
        for f, plain_hits, _ in hits:
            print(" ", os.path.relpath(f, a.root), plain_hits)
        print("dry run only. Re-run with --apply to change files.")
        return 0

    done, failed = 0, []
    for f, plain_hits, _ in hits:
        if not plain_hits:
            continue
        rel = os.path.relpath(f, a.root)
        b = os.path.join(backup, rel)
        os.makedirs(os.path.dirname(b), exist_ok=True)
        if not os.path.exists(b):
            shutil.copy2(f, b)
        tmp = f + ".tmp_urlupdate"
        try:
            zin = zipfile.ZipFile(f)
            zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.endswith(".xml") or item.filename.endswith(".rels"):
                    t = data.decode("utf8", "ignore")
                    if a.old in t:
                        data = t.replace(a.old, a.new).encode("utf8")
                zout.writestr(item, data)
            zout.close()
            zin.close()
            zc = zipfile.ZipFile(tmp)
            bad = zc.testzip()
            left = sum(zc.read(n).decode("utf8", "ignore").count(a.old) for n in xml_parts(zc))
            zc.close()
            if bad or left:
                os.remove(tmp)
                failed.append((rel, f"verify failed bad={bad} left={left}"))
                continue
            os.replace(tmp, f)
            done += 1
        except Exception as e:  # locked file, permission, corrupt zip
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
            failed.append((rel, str(e)))
    print(f"updated: {done} | failed: {len(failed)} | backup: {backup}")
    for r in failed:
        print("  FAILED:", r)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
