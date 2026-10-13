<#
.SYNOPSIS
  Re-export PDFs from updated .docx files with Microsoft Word, safely.

.DESCRIPTION
  For every <name>.docx that has a same-name <name>.pdf in the same folder:
    1. backs up the existing PDF (same relative path under -BackupDir),
    2. exports the DOCX to a temporary PDF with Word,
    3. swaps it in only if the page count matches the old PDF and (when -ExpectText is given)
       the new PDF contains that text. Otherwise the original is kept and reported.
  Dry-run by default: nothing is changed unless -Apply is passed.

  Needs: Windows, Microsoft Word, Python with pypdf (used only to count pages / read text).

.EXAMPLE
  .\reexport_docx_to_pdf.ps1 -Root "C:\Resumes" -BackupDir "C:\Resumes\_backup_pdf" -ExpectText "abhishek-singla-pm"
  .\reexport_docx_to_pdf.ps1 -Root "C:\Resumes" -BackupDir "C:\Resumes\_backup_pdf" -ExpectText "abhishek-singla-pm" -Apply
#>
param(
  [Parameter(Mandatory = $true)] [string] $Root,
  [Parameter(Mandatory = $true)] [string] $BackupDir,
  [string] $ExpectText = "",
  [switch] $Apply
)

$ErrorActionPreference = "Stop"

$py = @'
import sys, pypdf
p, needle = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
r = pypdf.PdfReader(p)
txt = "".join((pg.extract_text() or "") for pg in r.pages)
uris = []
for pg in r.pages:
    for a in (pg.get("/Annots") or []):
        try:
            u = a.get_object().get("/A", {}).get("/URI")
            if u: uris.append(str(u))
        except Exception:
            pass
found = bool(needle) and (needle in txt or any(needle in u for u in uris))
print(f"{len(r.pages)}|{found}")
'@
$pyFile = Join-Path ([IO.Path]::GetTempPath()) "pdfinfo_$([guid]::NewGuid().ToString('N')).py"
Set-Content -Path $pyFile -Value $py -Encoding UTF8

function Get-PdfInfo([string] $path) {
  $out = (python -I $pyFile $path $ExpectText) -join ""
  $parts = $out.Split("|")
  [pscustomobject]@{ Pages = [int]$parts[0]; HasText = ($parts[1] -eq "True") }
}

$pairs = Get-ChildItem -Path $Root -Recurse -Filter *.docx -File |
  Where-Object { $_.FullName -notlike "$BackupDir*" -and $_.Name -notlike "~$*" } |
  ForEach-Object {
    $pdf = [IO.Path]::ChangeExtension($_.FullName, ".pdf")
    if (Test-Path $pdf) { [pscustomobject]@{ Docx = $_.FullName; Pdf = $pdf } }
  }

"DOCX files with a same-name PDF: $(@($pairs).Count)"
if (-not $Apply) {
  $pairs | ForEach-Object { "  " + $_.Pdf.Substring($Root.Length).TrimStart('\') }
  "Dry run only. Re-run with -Apply to export."
  Remove-Item $pyFile -Force
  return
}

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$report = @()
try {
  foreach ($p in $pairs) {
    $rel = $p.Pdf.Substring($Root.Length).TrimStart('\')
    $backup = Join-Path $BackupDir $rel
    New-Item -ItemType Directory -Force (Split-Path $backup) | Out-Null
    if (-not (Test-Path $backup)) { Copy-Item $p.Pdf $backup }

    $before = Get-PdfInfo $p.Pdf
    $tmp = "$($p.Pdf).new.pdf"
    $doc = $word.Documents.Open($p.Docx, $false, $true)   # read-only
    $doc.ExportAsFixedFormat($tmp, 17)
    $doc.Close($false)
    $after = Get-PdfInfo $tmp

    $textOk = ([string]::IsNullOrEmpty($ExpectText)) -or $after.HasText
    if ($after.Pages -eq $before.Pages -and $textOk) {
      Move-Item -Force $tmp $p.Pdf
      $report += "UPDATED        pages $($before.Pages)->$($after.Pages)  $rel"
    } else {
      Remove-Item $tmp -Force
      $report += "KEPT ORIGINAL  pages $($before.Pages)->$($after.Pages) expectedText=$textOk  $rel"
    }
  }
} finally {
  $word.Quit()
  Remove-Item $pyFile -Force -ErrorAction SilentlyContinue
}
$report
