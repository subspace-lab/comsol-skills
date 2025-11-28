# COMSOL Documentation Search Skill

Search and retrieve COMSOL Multiphysics documentation.

## Commands

### Search

```bash
uv run comsol-search search "<term>" [OPTIONS]
```

**Options:**
- `--version, -v`: COMSOL version (default: 6.4)
- `--max-results, -n`: Max results (default: 20)
- `--module, -m`: Filter by module (partial match, comma-separated)
- `--format, -f`: Output format (table, json, markdown, plain)
- `--output, -o`: Save to file

### Retrieve

```bash
uv run comsol-search retrieve "<url>" [OPTIONS]
```

**Options:**
- `--format, -f`: Output format (markdown, plain, html)
- `--output, -o`: Save to file

## Search Strategy

**Use 2-3 keywords, not questions.** COMSOL uses keyword matching.

### Query Transformation

| User Request | Search Query |
|--------------|--------------|
| "How do I model battery aging?" | `"battery aging"` |
| "thermal runaway in Li-ion batteries" | `"thermal runaway battery"` |
| "C-rate for fast charging" | `"discharge rate"` |
| "SEI layer modeling" | `"electrode interface"` |

### Progressive Search

If no results, try broader terms:
1. `"C-rate battery"` → fails
2. `"discharge rate"` → success
3. `"battery performance"` → success

### Web Search for Terminology

When user terms don't match COMSOL vocabulary, use WebSearch first:

```
User: "particle-level battery behavior"
→ WebSearch: "COMSOL particle model battery"
→ Discover: "intercalation", "porous electrode"
→ Search: uv run comsol-search search "intercalation" --module "Battery"
```

## Module Filtering

Common modules (partial match supported):
- `"Application Programming"` - API docs
- `"Battery Design"` - Battery modeling
- `"Heat Transfer"` - Thermal analysis
- `"CFD"` - Fluid dynamics
- `"Electrochemistry"` - Electrochemical systems

```bash
# API documentation
uv run comsol-search search "model object" --module "Application Programming"

# Battery + thermal
uv run comsol-search search "thermal" --module "Battery,Heat Transfer"
```

## Example Queries

**Battery:** `"battery aging"`, `"thermal runaway"`, `"capacity fade"`, `"lithium plating"`

**API:** `"model object"`, `"java api"`, `"run study"`, `"add physics"`

**General:** `"phase change"`, `"heat transfer"`, `"turbulent flow"`, `"multiphysics"`
