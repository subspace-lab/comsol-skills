# COMSOL Documentation Search Tool

A CLI tool for searching COMSOL Multiphysics documentation using browser automation.

## Why This Tool?

The COMSOL documentation website uses dynamic JavaScript rendering (Vaadin SPA) that cannot be scraped with simple HTTP requests. This tool uses Playwright to automate a real browser and extract structured results.

## Quick Start

```bash
# Install dependencies
uv sync

# Install browser
uv run playwright install chromium

# Search!
uv run comsol-search search "battery aging"
```

## Usage

### Search Documentation

```bash
# Basic search
uv run comsol-search search "phase change materials"

# Filter by module
uv run comsol-search search "model object" --module "Application Programming"
uv run comsol-search search "aging" --module "Battery Design"

# More options
uv run comsol-search search "turbulent flow" \
  --version 6.3 \
  --max-results 50 \
  --format json \
  --output results.json
```

### Retrieve Full Content

```bash
uv run comsol-search retrieve "https://doc.comsol.com/..." --format markdown
```

## Search Tips

**Use 2-3 keywords, not questions.** COMSOL uses keyword matching, not semantic search.

| Instead of... | Use... |
|---------------|--------|
| "How do I model battery aging?" | `"battery aging"` |
| "C-rate for fast charging?" | `"discharge rate"` |

**Use module filtering** to focus results:
- `--module "Application Programming"` for API docs
- `--module "Battery Design"` for battery engineering
- `--module "Heat Transfer,CFD"` for multiple modules

## Project Structure

```
src/comsol_doc/       # Main package (cli, core, models, formatters)
.claude/skills/       # Claude Code skill definition
pyproject.toml        # Dependencies & config
```

## Development

```bash
# Prerequisites
# - Python 3.12+
# - uv (https://github.com/astral-sh/uv)

# Setup
uv sync
uv run playwright install chromium

# Test
uv run comsol-search search "battery" --module "Battery Design"
```

## License

Apache License 2.0 - See [LICENSE](LICENSE)
