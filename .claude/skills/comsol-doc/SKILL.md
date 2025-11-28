# COMSOL Documentation Search Skill

Search and retrieve COMSOL Multiphysics documentation using automated browser tools.

## Available Commands

### 1. Search Documentation

Search COMSOL documentation for specific terms and get structured results:

```bash
uv run comsol-search search "<search_term>" [OPTIONS]
```

**Options:**
- `--version, -v`: COMSOL version (default: 6.4)
- `--max-results, -n`: Maximum results to return (default: 20)
- `--module, -m`: Filter by module name (partial matches, comma-separated for multiple)
- `--format, -f`: Output format - table, json, markdown, plain (default: table)
- `--output, -o`: Save to file instead of stdout

**Examples:**
```bash
# Search for phase change materials
uv run comsol-search search "phase change materials"

# Search with specific version and JSON output
uv run comsol-search search "heat transfer" --version 6.3 --format json

# Save results to file
uv run comsol-search search "turbulent flow" --max-results 50 --output results.json

# Filter to API documentation only
uv run comsol-search search "model object" --module "Application Programming"

# Filter to Battery Design Module
uv run comsol-search search "battery" --module "Battery Design"

# Filter to multiple modules
uv run comsol-search search "thermal" --module "Battery Design,Heat Transfer"
```

### 2. Retrieve Documentation Content

Retrieve full content from a specific COMSOL documentation URL:

```bash
uv run comsol-search retrieve "<url>" [OPTIONS]
```

**Options:**
- `--format, -f`: Output format - markdown, plain, html (default: markdown)
- `--output, -o`: Save to file instead of stdout

**Examples:**
```bash
# Retrieve documentation in markdown format
uv run comsol-search retrieve "https://doc.comsol.com/6.4/docserver/#!/com.comsol.help.models.porous.packed_bed_latent_heat_storage/packed_bed_latent_heat_storage.html"

# Save as HTML file
uv run comsol-search retrieve "<url>" --format html --output doc.html
```

## Skill Usage

When users ask you to search COMSOL documentation, use the following approach:

1. **For search queries**: Use the `search` command with appropriate search terms
2. **For specific documents**: Use the `retrieve` command if the user provides a URL
3. **Format selection**:
   - Use `table` for quick terminal viewing
   - Use `json` for programmatic processing
   - Use `markdown` for documentation/reports

## CRITICAL: Search Strategy

**The COMSOL documentation search uses keyword matching, NOT semantic search.**

### ✅ Good Search Queries (What Works)

Use **2-3 simple keywords** that would appear in documentation:

- ✅ "battery aging" (2 words, broad)
- ✅ "thermal runaway" (2 words, specific concept)
- ✅ "lithium ion battery" (3 words, common term)
- ✅ "heat transfer porous" (3 words, descriptive)
- ✅ "phase change" (2 words, broad concept)

### ❌ Bad Search Queries (What Fails)

Avoid these patterns:

- ❌ "How do I model electrochemical thermal coupling?" (full question, too long)
- ❌ "fast charging simulation optimization" (4+ words, too specific)
- ❌ "C-rate battery discharge" (technical abbreviations)
- ❌ "battery pack thermal management system design" (too many words)
- ❌ "What is the Butler-Volmer equation for lithium batteries?" (conversational)

### 🎯 Query Transformation Rules

When users ask questions, transform them to short keyword searches:

| User Request | Good Search Query |
|--------------|-------------------|
| "How do I model battery aging?" | "battery aging" |
| "I need help with thermal runaway in Li-ion batteries" | "thermal runaway battery" |
| "What's the C-rate for fast charging?" | "discharge rate" or "charge rate" |
| "How to couple electrochemical and thermal physics?" | "multiphysics battery" or "thermal electrochemical" |
| "Where do I find SEI layer modeling?" | "electrode interface" or "electrolyte interface" |
| "Dendrite formation in lithium metal" | "dendrite lithium" or "lithium plating" |

### 🔄 Progressive Search Strategy

If a specific search fails, try broader terms:

1. **Start specific** (if user provided exact terminology)
   - "C-rate battery" → No results

2. **Fall back to broader terms**
   - "discharge rate" → Success!
   - "battery performance" → Success!

3. **Try related concepts**
   - "charging protocol" → Success!

### 🎯 Module Filtering for Specific Use Cases

Use `--module` flag to focus on relevant documentation sections:

**For API/Coding Documentation:**
```bash
# Get API-specific results only
uv run comsol-search search "add physics" --module "Application Programming"
uv run comsol-search search "model object" --module "Application Programming"
uv run comsol-search search "run study" --module "Application Programming"
```

**For Battery Engineering:**
```bash
# Get Battery Design Module docs only
uv run comsol-search search "aging" --module "Battery Design"
uv run comsol-search search "thermal runaway" --module "Battery Design,Heat Transfer"
```

**For Specific Physics Modules:**
```bash
uv run comsol-search search "porous media" --module "Porous Media Flow"
uv run comsol-search search "turbulence" --module "CFD"
```

**Impact:** Module filtering can improve relevance from 30% to 70%+ by excluding unrelated documentation sections.

### 📊 Search Query Guidelines

**Length:**
- Ideal: 2-3 words
- Maximum: 4 words
- Avoid: Full sentences or questions

**Word Choice:**
- Use: Common technical terms ("battery", "thermal", "flow")
- Avoid: Abbreviations initially ("C-rate", "SEI", "SOC")
- Avoid: Brand names or very specific compounds

**Structure:**
- Use: Noun phrases ("battery aging", "heat transfer")
- Avoid: Questions ("how to", "what is", "where can I")
- Avoid: Qualifiers ("very fast", "extremely accurate")

## Technical Details

- Uses Playwright browser automation to interact with COMSOL's Vaadin-based SPA
- Headless browser mode enabled by default
- Handles dynamic JavaScript-rendered content
- Extracts structured data: module, title, path, snippets

## Example Search Terms (Battery Engineering)

**Electrochemistry & Physics:**
- "lithium ion battery"
- "battery discharge"
- "electrochemical impedance"
- "Butler Volmer" (not "Butler-Volmer equation")

**Thermal Management:**
- "thermal runaway battery"
- "battery cooling"
- "heat generation"
- "phase change cooling"

**Aging & Degradation:**
- "battery aging"
- "capacity fade"
- "lithium plating"
- "electrode degradation"

**General COMSOL Topics:**
- "phase change materials"
- "heat transfer porous"
- "turbulent flow"
- "multiphysics coupling"
- "finite element"

## Notes

- The COMSOL documentation website requires JavaScript, so simple HTTP requests (curl) won't work
- Search results are organized by COMSOL module (Heat Transfer, Porous Media Flow, etc.)
- Chromium browser must be installed: `uv run playwright install chromium`
