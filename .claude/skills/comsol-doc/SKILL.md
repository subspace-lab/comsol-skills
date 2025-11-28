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

### 🌐 Composing with Web Search for Semantic Understanding

**Problem:** Users often use general terms that don't match COMSOL's technical vocabulary.

**Solution:** Use web search to discover COMSOL-specific terminology, then search documentation.

#### Workflow: Terminology Discovery

**Step 1: Use WebSearch to understand COMSOL terminology**
```
When user asks: "I want to model particle-level battery behavior"
→ Use WebSearch to discover COMSOL terminology
→ Learn: COMSOL calls this "intercalation", "porous electrode", "particle diffusion"
```

**Step 2: Use discovered terms in comsol-search**
```bash
uv run comsol-search search "intercalation lithium" --module "Battery"
uv run comsol-search search "porous electrode" --module "Battery"
```

#### Example Pattern

**User Request:** "Set up particle model for iPhone battery OCV using script"

**Composable Workflow:**

1. **WebSearch for terminology**
   ```
   Query: "COMSOL particle model battery terminology"
   Result: Discover terms "intercalation", "single particle model", "lithium-ion battery interface"
   ```

2. **Search COMSOL docs with proper terms**
   ```bash
   uv run comsol-search search "lithium ion battery interface" --max-results 20
   uv run comsol-search search "intercalation" --module "Battery"
   uv run comsol-search search "open circuit voltage" --module "Battery"
   ```

3. **WebSearch for API terminology**
   ```
   Query: "COMSOL Java API create physics interface"
   Result: Learn about "Model object", "physics().create()", "study().run()"
   ```

4. **Search COMSOL API docs**
   ```bash
   uv run comsol-search search "model object" --module "programming"
   uv run comsol-search search "java api physics" --module "programming"
   ```

#### Common Terminology Transformations

Use WebSearch to map user terminology → COMSOL terminology:

| User Term | WebSearch Query | COMSOL Term Found | Search Query |
|-----------|----------------|-------------------|--------------|
| "particle model" | "COMSOL battery particle" | "intercalation", "porous electrode" | `search "intercalation"` |
| "OCV curve" | "COMSOL open circuit voltage" | "equilibrium potential", "OCV modeling" | `search "equilibrium potential"` |
| "battery script" | "COMSOL battery automation Java" | "Lithium-Ion Battery interface", "Java API" | `search "java api"` |
| "aging simulation" | "COMSOL battery aging" | "capacity fade", "calendar aging", "SEI layer" | `search "capacity fade"` |

#### When to Use This Pattern

**Use web search for terminology discovery when:**
- User query returns 0 results from comsol-search
- User uses generic/academic terms (not COMSOL-specific)
- User is new to COMSOL and unfamiliar with terminology
- Exploring unfamiliar domain (e.g., moving from CFD to battery modeling)

**Example:**
```bash
# Direct search fails
$ uv run comsol-search search "particle model" --module "Battery"
⠹ Found 15 results, filtered to 0 by module  # ❌

# Use web search to discover terminology
→ WebSearch: "COMSOL particle model battery"
→ Learn: "intercalation", "spherical diffusion", "porous electrode"

# Try again with COMSOL terms
$ uv run comsol-search search "intercalation" --module "Battery"
⠹ Found 10 results, filtered to 3 by module  # ✅

$ uv run comsol-search search "porous electrode" --module "Battery"
⠹ Found 12 results, filtered to 5 by module  # ✅
```

#### Advanced: Multi-Step Discovery

For complex tasks, chain web search and documentation search:

```
User: "Create thermal-electrochemical coupled battery model with aging"

Step 1: WebSearch "COMSOL battery thermal electrochemical coupling"
→ Learn: "Nonisothermal Lithium-Ion Battery interface", "multiphysics coupling"

Step 2: Search interface documentation
$ comsol-search search "nonisothermal lithium ion battery" --module "Battery"

Step 3: WebSearch "COMSOL battery aging mechanisms"
→ Learn: "SEI layer", "lithium plating", "capacity fade", "impedance rise"

Step 4: Search aging documentation
$ comsol-search search "SEI layer" --module "Battery"
$ comsol-search search "capacity fade" --module "Battery"

Step 5: WebSearch "COMSOL Java API multiphysics"
→ Learn: "multiphysics().create()", "physics interface names"

Step 6: Search API documentation
$ comsol-search search "java api multiphysics" --module "programming"
```

#### Benefits of Composable Approach

✅ **Flexibility:** Use web search when needed, skip when not
✅ **No tight coupling:** Tools remain independent
✅ **Semantic understanding:** Web search provides context
✅ **Accurate results:** COMSOL search provides authoritative docs
✅ **User control:** You decide when to use each tool

### 🎯 Module Filtering for Specific Use Cases

Use `--module` flag to focus on relevant documentation sections:

**For API/Coding Documentation:**
```bash
# Get API-specific results only
uv run comsol-search search "add physics" --module "Application Programming"
uv run comsol-search search "model object" --module "Application Programming"
uv run comsol-search search "run study" --module "Application Programming"
```

### 📚 Available Modules and Guides (COMSOL 6.4)

The `--module` flag accepts partial matches. Here are the main modules/guides available:

**Core Documentation:**
- `COMSOL Multiphysics` - Core documentation
- `Application Programming Guide` - API and Java programming
- `Model Manager API` - Model management API
- `Physics Builder Manual` - Custom physics interfaces

**Physics Modules:**
- `Battery Design Module` - Battery modeling and simulation
- `CFD Module` - Computational fluid dynamics
- `Heat Transfer Module` - Heat transfer modeling
- `Structural Mechanics Module` - Structural analysis
- `Acoustics Module` - Acoustics and vibration

**Specialized Modules:**
- `Chemical Reaction Engineering Module` - Chemical reactions
- `Corrosion Module` - Corrosion modeling
- `Electrochemistry Module` - Electrochemical systems
- `Electrodeposition Module` - Electroplating and deposition
- `Fuel Cell & Electrolyzer Module` - Fuel cells and electrolyzers
- `Microfluidics Module` - Microfluidic devices
- `Optimization Module` - Design optimization
- `Plasma Module` - Plasma physics
- `Electric Discharge Module` - Electrical discharge

**Flow and Porous Media:**
- `Pipe Flow Module` - Pipe networks and flow
- `Porous Media Flow Module` - Flow in porous media
- `Polymer Flow Module` - Non-Newtonian flow
- `Subsurface Flow Module` - Groundwater and subsurface

**Other Resources:**
- `Material Library` - Material properties database
- `Release Notes` - Version updates and changes
- `Reference Manual` - Complete reference documentation
- `LiveLink™ for Simulink®` - MATLAB/Simulink integration

**Usage Examples:**
```bash
# Use partial matches for convenience
uv run comsol-search search "aging" --module "Battery"
uv run comsol-search search "turbulence" --module "CFD"
uv run comsol-search search "java api" --module "programming"
uv run comsol-search search "material properties" --module "Material"

# Combine multiple modules (comma-separated)
uv run comsol-search search "thermal" --module "Battery,Heat Transfer"
uv run comsol-search search "flow" --module "CFD,Microfluidics"
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
