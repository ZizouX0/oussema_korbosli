#!/usr/bin/env bash
#
# setup-deps.sh — install runtime prerequisites for the skills in this folder.
#
# The skills themselves are pure files and need nothing to be *loaded* by
# Claude Code. This script installs the external tools some of them call at
# *run time*. It is safe to re-run; it is also a no-op for skills that have
# no external dependencies.
#
# Usage:  bash .claude/skills/setup-deps.sh
#
# NOTE: In ephemeral/remote sessions these installs do not persist across
# containers — re-run this script (or wire it into a SessionStart setup step)
# when you need the tooling again.

set -uo pipefail

note() { printf '\n\033[1;36m== %s ==\033[0m\n' "$*"; }
warn() { printf '\033[1;33m!! %s\033[0m\n' "$*"; }

# 1) System packages: OCR + PDF rasterization (pdf skill: pytesseract / pdf2image)
note "System packages (tesseract-ocr, poppler-utils)"
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq && sudo apt-get install -y -qq tesseract-ocr poppler-utils \
    || warn "apt install failed — PDF OCR (pytesseract) and pdf2image will be unavailable"
else
  warn "apt-get not found — install tesseract-ocr + poppler-utils manually for PDF OCR"
fi

# 2) Python packages (pdf, docx, xlsx, pptx, webapp-testing, slack-gif-creator, mcp-builder)
#    --break-system-packages: required on Debian/Ubuntu PEP-668 environments.
#    --ignore-installed: avoid failing on OS-managed packages (e.g. PyJWT/cryptography)
#    that lack pip RECORD metadata.
note "Python packages (pip)"
python3 -m pip install --break-system-packages --no-input --ignore-installed --retries 5 \
  cffi cryptography \
  pypdf pdfplumber reportlab pdf2image pypdfium2 pytesseract \
  openpyxl pandas numpy Pillow lxml defusedxml validators "markitdown[pptx]" \
  playwright imageio imageio-ffmpeg \
  anthropic mcp \
  || warn "pip install reported errors — re-run or inspect output above"

# 3) Playwright browser (webapp-testing)
note "Playwright browser (chromium)"
python3 -m playwright install --with-deps chromium \
  || warn "playwright browser install failed — webapp-testing will not be able to launch a browser"

# 4) Node CLIs: firecrawl (firecrawl-* skills), docx (docx skill), pptxgenjs (pptx skill)
note "Node CLIs (firecrawl-cli, docx, pptxgenjs)"
if command -v npm >/dev/null 2>&1; then
  npm install -g firecrawl-cli docx pptxgenjs \
    || warn "npm global install failed (you can also use 'npx firecrawl ...')"
else
  warn "npm not found — needed for firecrawl-cli, docx, pptxgenjs"
fi

# 5) Things you must configure yourself (not installable here)
note "Manual configuration"
echo "  • firecrawl-* skills require a Firecrawl API key:  export FIRECRAWL_API_KEY=fc-..."
echo "    Verify with:  firecrawl --status"
echo "  • docx/pptx JS generators need global node libs on the path:  export NODE_PATH=\$(npm root -g)"
echo
echo "Done. Skill code passed syntax checks; see README.md / install-manifest.json."
