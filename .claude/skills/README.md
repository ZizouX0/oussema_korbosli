# Installed Agent Skills

Installed **60 skills** from a `skillslock.json` (v1) lock file, 
to both `~/.claude/skills/` (personal) and this repo's `.claude/skills/` (project, version-controlled).

## Verification

Each skill's content was verified against the lock's `computedHash` using the **exact** 
folder-hash algorithm from the Skills CLI (`vercel-labs/skills` `computeSkillFolderHash`): 
SHA-256 over every file in the skill folder (relative path + content, sorted by JS `localeCompare`).

- **60/60 skills match the locked hash exactly.**
- 56 skills matched at the source repo's current `HEAD`.
- 4 skills had drifted upstream since the lock was created, so they were **pinned to the exact historical commit** whose folder-hash matches the lock:
  - `claude-api` → `claude-api` @ `da20c92503b2` (2026-05-28)
  - `frontend-design` → `frontend-design` @ `00756142ab04` (2025-12-04)
  - `firecrawl` → `firecrawl-cli` @ `9007a7139be4` (2026-05-27)
  - `firecrawl-scrape` → `firecrawl-scrape` @ `2618c20d8d50` (2026-04-08)
- All bundled scripts pass syntax checks (72 Python via `py_compile`, JS via `node --check`, shell via `bash -n`).
- All skills have valid frontmatter (`name` + `description`) and were loaded/discovered by Claude Code.

## Skills by source

### `anthropics/skills` (17)
- algorithmic-art  ·  _algorithmic-art_
- brand-guidelines  ·  _brand-guidelines_
- canvas-design  ·  _canvas-design_
- claude-api  ·  _claude-api_
- doc-coauthoring  ·  _doc-coauthoring_
- docx  ·  _docx_
- frontend-design  ·  _frontend-design_
- internal-comms  ·  _internal-comms_
- mcp-builder  ·  _mcp-builder_
- pdf  ·  _pdf_
- pptx  ·  _pptx_
- skill-creator  ·  _skill-creator_
- slack-gif-creator  ·  _slack-gif-creator_
- theme-factory  ·  _theme-factory_
- web-artifacts-builder  ·  _web-artifacts-builder_
- webapp-testing  ·  _webapp-testing_
- xlsx  ·  _xlsx_

### `firecrawl/cli` (10)
- firecrawl-cli  ·  _firecrawl_
- firecrawl-agent  ·  _firecrawl-agent_
- firecrawl-crawl  ·  _firecrawl-crawl_
- firecrawl-download  ·  _firecrawl-download_
- firecrawl-interact  ·  _firecrawl-interact_
- firecrawl-map  ·  _firecrawl-map_
- firecrawl-monitor  ·  _firecrawl-monitor_
- firecrawl-parse  ·  _firecrawl-parse_
- firecrawl-scrape  ·  _firecrawl-scrape_
- firecrawl-search  ·  _firecrawl-search_

### `obra/superpowers-skills` (31)
- brainstorming  ·  _Brainstorming Ideas Into Designs_
- receiving-code-review  ·  _Code Review Reception_
- collision-zone-thinking  ·  _Collision-Zone Thinking_
- condition-based-waiting  ·  _Condition-Based Waiting_
- defense-in-depth  ·  _Defense-in-Depth Validation_
- dispatching-parallel-agents  ·  _Dispatching Parallel Agents_
- executing-plans  ·  _Executing Plans_
- finishing-a-development-branch  ·  _Finishing a Development Branch_
- gardening-skills-wiki  ·  _Gardening Skills Wiki_
- using-skills  ·  _Getting Started with Skills_
- inversion-exercise  ·  _Inversion Exercise_
- meta-pattern-recognition  ·  _Meta-Pattern Recognition_
- preserving-productive-tensions  ·  _Preserving Productive Tensions_
- pulling-updates-from-skills-repository  ·  _Pulling Updates from Skills Repository_
- remembering-conversations  ·  _Remembering Conversations_
- requesting-code-review  ·  _Requesting Code Review_
- root-cause-tracing  ·  _Root Cause Tracing_
- scale-game  ·  _Scale Game_
- sharing-skills  ·  _Sharing Skills_
- simplification-cascades  ·  _Simplification Cascades_
- subagent-driven-development  ·  _Subagent-Driven Development_
- systematic-debugging  ·  _Systematic Debugging_
- test-driven-development  ·  _Test-Driven Development (TDD)_
- testing-anti-patterns  ·  _Testing Anti-Patterns_
- testing-skills-with-subagents  ·  _Testing Skills With Subagents_
- tracing-knowledge-lineages  ·  _Tracing Knowledge Lineages_
- using-git-worktrees  ·  _Using Git Worktrees_
- verification-before-completion  ·  _Verification Before Completion_
- when-stuck  ·  _When Stuck - Problem-Solving Dispatch_
- writing-plans  ·  _Writing Plans_
- writing-skills  ·  _Writing Skills_

### `vercel-labs/agent-skills` (1)
- web-design-guidelines  ·  _web-design-guidelines_

### `vercel-labs/skills` (1)
- find-skills  ·  _find-skills_

## Runtime dependencies

Some skills call external tools at run time. These have been **installed and
verified** in this session. To reinstall them (e.g. in a fresh/ephemeral
container, where installs do not persist), run:

```bash
bash .claude/skills/setup-deps.sh
```

What it installs, and the verification performed:

| For skills | Installed | Verified |
|---|---|---|
| `pdf` | `pypdf`, `pdfplumber`, `reportlab`, `pdf2image`, `pypdfium2`, `pytesseract` + `tesseract-ocr`, `poppler-utils` | create→read→extract PDF round-trip ✓ |
| `xlsx` | `openpyxl`, `pandas`, `numpy` | workbook write→read ✓ |
| `pptx` | `python-pptx`, `markitdown[pptx]`, `pptxgenjs` (npm) | presentation create→read ✓ |
| `docx` | `docx` (npm) + OOXML libs (`lxml`, `defusedxml`) | module loads via `NODE_PATH` ✓ |
| `webapp-testing` | `playwright` + chromium browser | headless launch + render ✓ |
| `slack-gif-creator` | `Pillow`, `imageio`, `imageio-ffmpeg`, `numpy` | imports ✓ |
| `mcp-builder` | `anthropic`, `mcp` | imports ✓ |
| `firecrawl-*` | `firecrawl-cli` (npm, bin `firecrawl`) | CLI runs (`--status`) ✓ |

**Manual configuration still required:**
- **`firecrawl-*`** need a Firecrawl API key: `export FIRECRAWL_API_KEY=fc-...` (or `firecrawl login`), then verify with `firecrawl --status`.
- The **JS** generators in `docx`/`pptx` need global node modules on the path: `export NODE_PATH=$(npm root -g)`.
- **`remembering-conversations`** builds a small TS tool on first use.

See each skill's `SKILL.md` for specifics. Verified per-skill hashes are recorded in `install-manifest.json`.
