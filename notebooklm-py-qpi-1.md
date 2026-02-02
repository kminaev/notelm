# Python API Reference

**Status:** Active
**Last Updated:** 2026-01-20

Complete reference for the `notebooklm` Python library.

## Quick Start

```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    # Create client from saved authentication
    async with await NotebookLMClient.from_storage() as client:
        # List notebooks
        notebooks = await client.notebooks.list()
        print(f"Found {len(notebooks)} notebooks")

        # Create a new notebook
        nb = await client.notebooks.create("My Research")
        print(f"Created: {nb.id}")

        # Add sources
        await client.sources.add_url(nb.id, "https://example.com/article")

        # Ask a question
        result = await client.chat.ask(nb.id, "Summarize the main points")
        print(result.answer)

        # Generate a podcast
        status = await client.artifacts.generate_audio(nb.id)
        final = await client.artifacts.wait_for_completion(nb.id, status.task_id)
        print(f"Audio ready: {final.url}")

asyncio.run(main())
```

---

## Core Concepts

### Async Context Manager

The client must be used as an async context manager to properly manage HTTP connections:

```python
# Correct - uses context manager
async with await NotebookLMClient.from_storage() as client:
    ...

# Also correct - manual management
client = await NotebookLMClient.from_storage()
await client.__aenter__()
try:
    ...
finally:
    await client.__aexit__(None, None, None)
```

### Authentication

The client requires valid Google session cookies obtained via browser login:

```python
# From storage file (recommended)
client = await NotebookLMClient.from_storage()
client = await NotebookLMClient.from_storage("/path/to/storage_state.json")

# From AuthTokens directly
from notebooklm import AuthTokens
auth = AuthTokens(
    cookies={"SID": "...", "HSID": "...", ...},
    csrf_token="...",
    session_id="..."
)
client = NotebookLMClient(auth)
```

**Environment Variable Support:**

The library respects these environment variables for authentication:

| Variable | Description |
|----------|-------------|
| `NOTEBOOKLM_HOME` | Base directory for config files (default: `~/.notebooklm`) |
| `NOTEBOOKLM_AUTH_JSON` | Inline auth JSON - no file needed (for CI/CD) |

**Precedence** (highest to lowest):
1. Explicit `path` argument to `from_storage()`
2. `NOTEBOOKLM_AUTH_JSON` environment variable
3. `$NOTEBOOKLM_HOME/storage_state.json`
4. `~/.notebooklm/storage_state.json`

**CI/CD Example:**
```python
import os

# Set auth JSON from environment (e.g., GitHub Actions secret)
os.environ["NOTEBOOKLM_AUTH_JSON"] = '{"cookies": [...]}'

# Client automatically uses the env var
async with await NotebookLMClient.from_storage() as client:
    notebooks = await client.notebooks.list()
```

### Error Handling

The library raises `RPCError` for API failures:

```python
from notebooklm import RPCError

try:
    result = await client.notebooks.create("Test")
except RPCError as e:
    print(f"RPC failed: {e}")
    # Common causes:
    # - Session expired (re-run `notebooklm login`)
    # - Rate limited (wait and retry)
    # - Invalid parameters
```

### Authentication & Token Refresh

**Automatic Refresh:** The client automatically refreshes CSRF tokens when authentication errors are detected. This happens transparently during any API call - you don't need to handle it manually.

When an RPC call fails with an auth error (HTTP 401/403 or auth-related message):
1. The client fetches fresh tokens from the NotebookLM homepage
2. Waits briefly to avoid rate limiting
3. Retries the failed request automatically

**Manual Refresh:** For proactive refresh (e.g., before a long-running operation):

```python
async with await NotebookLMClient.from_storage() as client:
    # Manually refresh CSRF token and session ID
    await client.refresh_auth()
```

**Note:** If your session cookies have fully expired (not just CSRF tokens), you'll need to re-run `notebooklm login`.

---

## API Reference

### NotebookLMClient

Main client class providing access to all APIs.

```python
class NotebookLMClient:
    notebooks: NotebooksAPI    # Notebook operations
    sources: SourcesAPI        # Source management
    artifacts: ArtifactsAPI    # AI-generated content
    chat: ChatAPI              # Conversations
    research: ResearchAPI      # Web/Drive research
    notes: NotesAPI            # User notes
    sharing: SharingAPI        # Notebook sharing

    @classmethod
    async def from_storage(cls, path: str = None) -> "NotebookLMClient"

    async def refresh_auth(self) -> AuthTokens
```

---

### NotebooksAPI (`client.notebooks`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list()` | - | `list[Notebook]` | List all notebooks |
| `create(title)` | `title: str` | `Notebook` | Create a notebook |
| `get(notebook_id)` | `notebook_id: str` | `Notebook` | Get notebook details |
| `delete(notebook_id)` | `notebook_id: str` | `bool` | Delete a notebook |
| `rename(notebook_id, new_title)` | `notebook_id: str, new_title: str` | `Notebook` | Rename a notebook |
| `get_description(notebook_id)` | `notebook_id: str` | `NotebookDescription` | Get AI summary and topics |
| `get_summary(notebook_id)` | `notebook_id: str` | `str` | Get raw summary text |
| `share(notebook_id, settings=None)` | `notebook_id: str, settings: dict` | `Any` | Share notebook with settings |
| `remove_from_recent(notebook_id)` | `notebook_id: str` | `None` | Remove from recently viewed |
| `get_raw(notebook_id)` | `notebook_id: str` | `Any` | Get raw API response data |

**Example:**
```python
# List all notebooks
notebooks = await client.notebooks.list()
for nb in notebooks:
    print(f"{nb.id}: {nb.title} ({nb.sources_count} sources)")

# Create and rename
nb = await client.notebooks.create("Draft")
nb = await client.notebooks.rename(nb.id, "Final Version")

# Get AI-generated description (parsed with suggested topics)
desc = await client.notebooks.get_description(nb.id)
print(desc.summary)
for topic in desc.suggested_topics:
    print(f"  - {topic.question}")

# Get raw summary text (unparsed)
summary = await client.notebooks.get_summary(nb.id)
print(summary)

# Share a notebook
await client.notebooks.share(nb.id, settings={"public": True})
```

**get_summary vs get_description:**
- `get_summary()` returns the raw summary text string
- `get_description()` returns a `NotebookDescription` object with the parsed summary and a list of `SuggestedTopic` objects for suggested questions

---

### SourcesAPI (`client.sources`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list(notebook_id)` | `notebook_id: str` | `list[Source]` | List sources |
| `get(notebook_id, source_id)` | `str, str` | `Source` | Get source details |
| `get_fulltext(notebook_id, source_id)` | `str, str` | `SourceFulltext` | Get full indexed text content |
| `get_guide(notebook_id, source_id)` | `str, str` | `dict` | Get AI-generated summary and keywords |
| `add_url(notebook_id, url)` | `str, str` | `Source` | Add URL source |
| `add_youtube(notebook_id, url)` | `str, str` | `Source` | Add YouTube video |
| `add_text(notebook_id, title, content)` | `str, str, str` | `Source` | Add text content |
| `add_file(notebook_id, path, mime_type=None)` | `str, Path, str` | `Source` | Upload file |
| `add_drive(notebook_id, file_id, title, mime_type)` | `str, str, str, str` | `Source` | Add Google Drive doc |
| `rename(notebook_id, source_id, new_title)` | `str, str, str` | `Source` | Rename source |
| `refresh(notebook_id, source_id)` | `str, str` | `bool` | Refresh URL/Drive source |
| `check_freshness(notebook_id, source_id)` | `str, str` | `bool` | Check if source needs refresh |
| `delete(notebook_id, source_id)` | `str, str` | `bool` | Delete source |

**Example:**
```python
# Add various source types
await client.sources.add_url(nb_id, "https://example.com/article")
await client.sources.add_youtube(nb_id, "https://youtube.com/watch?v=...")
await client.sources.add_text(nb_id, "My Notes", "Content here...")
await client.sources.add_file(nb_id, Path("./document.pdf"))

# List and manage
sources = await client.sources.list(nb_id)
for src in sources:
    print(f"{src.id}: {src.title} ({src.kind})")

await client.sources.rename(nb_id, src.id, "Better Title")
await client.sources.refresh(nb_id, src.id)  # Re-fetch URL content

# Check if a source needs refreshing (content changed)
is_fresh = await client.sources.check_freshness(nb_id, src.id)
if not is_fresh:
    await client.sources.refresh(nb_id, src.id)

# Get full indexed content (what NotebookLM uses for answers)
fulltext = await client.sources.get_fulltext(nb_id, src.id)
print(f"Content ({fulltext.char_count} chars): {fulltext.content[:500]}...")

# Get AI-generated summary and keywords
guide = await client.sources.get_guide(nb_id, src.id)
print(f"Summary: {guide['summary']}")
print(f"Keywords: {guide['keywords']}")
```

---

### ArtifactsAPI (`client.artifacts`)

#### Core Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list(notebook_id, type=None)` | `str, int` | `list[Artifact]` | List artifacts |
| `get(notebook_id, artifact_id)` | `str, str` | `Artifact` | Get artifact details |
| `delete(notebook_id, artifact_id)` | `str, str` | `bool` | Delete artifact |
| `rename(notebook_id, artifact_id, new_title)` | `str, str, str` | `None` | Rename artifact |
| `poll_status(notebook_id, task_id)` | `str, str` | `GenerationStatus` | Check generation status |
| `wait_for_completion(notebook_id, task_id, ...)` | `str, str, ...` | `GenerationStatus` | Wait for generation |

#### Type-Specific List Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list_audio(notebook_id)` | `str` | `list[Artifact]` | List audio overview artifacts |
| `list_video(notebook_id)` | `str` | `list[Artifact]` | List video overview artifacts |
| `list_reports(notebook_id)` | `str` | `list[Artifact]` | List report artifacts (Briefing Doc, Study Guide, Blog Post) |
| `list_quizzes(notebook_id)` | `str` | `list[Artifact]` | List quiz artifacts |
| `list_flashcards(notebook_id)` | `str` | `list[Artifact]` | List flashcard artifacts |
| `list_infographics(notebook_id)` | `str` | `list[Artifact]` | List infographic artifacts |
| `list_slide_decks(notebook_id)` | `str` | `list[Artifact]` | List slide deck artifacts |
| `list_data_tables(notebook_id)` | `str` | `list[Artifact]` | List data table artifacts |

#### Generation Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `generate_audio(...)` | See below | `GenerationStatus` | Generate podcast |
| `generate_video(...)` | See below | `GenerationStatus` | Generate video |
| `generate_report(...)` | See below | `GenerationStatus` | Generate report |
| `generate_quiz(...)` | See below | `GenerationStatus` | Generate quiz |
| `generate_flashcards(...)` | See below | `GenerationStatus` | Generate flashcards |
| `generate_slide_deck(...)` | See below | `GenerationStatus` | Generate slide deck |
| `generate_infographic(...)` | See below | `GenerationStatus` | Generate infographic |
| `generate_data_table(...)` | See below | `GenerationStatus` | Generate data table |
| `generate_mind_map(...)` | See below | `dict` | Generate mind map |

#### Downloading Artifacts

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `download_audio(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download audio to file (MP4/MP3) |
| `download_video(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download video to file (MP4) |
| `download_infographic(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download infographic to file (PNG) |
| `download_slide_deck(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download slide deck as PDF |
| `download_report(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download report as Markdown (.md) |
| `download_mind_map(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download mind map as JSON (.json) |
| `download_data_table(notebook_id, output_path, artifact_id=None)` | `str, str, str` | `str` | Download data table as CSV (.csv) |
| `download_quiz(notebook_id, output_path, artifact_id=None, output_format="json")` | `str, str, str, str` | `str` | Download quiz (json/markdown/html) |
| `download_flashcards(notebook_id, output_path, artifact_id=None, output_format="json")` | `str, str, str, str` | `str` | Download flashcards (json/markdown/html) |

**Download Methods:**

```python
# Download the most recent completed audio overview
path = await client.artifacts.download_audio(nb_id, "podcast.mp4")

# Download a specific audio artifact by ID
path = await client.artifacts.download_audio(nb_id, "podcast.mp4", artifact_id="abc123")

# Download video overview
path = await client.artifacts.download_video(nb_id, "video.mp4")

# Download infographic
path = await client.artifacts.download_infographic(nb_id, "infographic.png")

# Download slide deck as PDF
path = await client.artifacts.download_slide_deck(nb_id, "./slides.pdf")
# Returns: "./slides.pdf"

# Download report as Markdown
path = await client.artifacts.download_report(nb_id, "./study-guide.md")
# Extracts markdown content from Briefing Doc, Study Guide, Blog Post, etc.

# Download mind map as JSON
path = await client.artifacts.download_mind_map(nb_id, "./concept-map.json")
# JSON structure: {"name": "Topic", "children": [{"name": "Subtopic", ...}]}

# Download data table as CSV
path = await client.artifacts.download_data_table(nb_id, "./data.csv")
# CSV uses UTF-8 with BOM encoding for Excel compatibility

# Download quiz as JSON (default)
path = await client.artifacts.download_quiz(nb_id, "quiz.json")

# Download quiz as markdown with answers marked
path = await client.artifacts.download_quiz(nb_id, "quiz.md", output_format="markdown")

# Download flashcards as JSON (normalizes f/b to front/back)
path = await client.artifacts.download_flashcards(nb_id, "cards.json")

# Download flashcards as markdown
path = await client.artifacts.download_flashcards(nb_id, "cards.md", output_format="markdown")
```

**Notes:**
- If `artifact_id` is not specified, downloads the first completed artifact of that type
- Raises `ValueError` if no completed artifact is found
- Some URLs require browser-based download (handled automatically)
- Report downloads extract the markdown content from the artifact
- Mind map downloads return a JSON tree structure with `name` and `children` fields
- Data table downloads parse the complex rich-text format into CSV rows/columns
- Quiz/flashcard formats: `json` (structured), `markdown` (readable), `html` (raw)

#### Export Methods

Export artifacts to Google Docs or Google Sheets.

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `export_report(notebook_id, artifact_id, title, export_type)` | `str, str, str, ExportType` | `Any` | Export report to Google Docs/Sheets |
| `export_data_table(notebook_id, artifact_id, title)` | `str, str, str` | `Any` | Export data table to Google Sheets |
| `export(notebook_id, artifact_id, content, title, export_type)` | `str, str, str, str, ExportType` | `Any` | Generic export to Docs/Sheets |

**Export Types (ExportType enum):**
- `ExportType.DOCS` (1): Export to Google Docs
- `ExportType.SHEETS` (2): Export to Google Sheets

```python
from notebooklm import ExportType

# Export a report to Google Docs
result = await client.artifacts.export_report(
    nb_id,
    artifact_id="report_123",
    title="My Briefing Doc",
    export_type=ExportType.DOCS
)
# result contains the Google Docs URL

# Export a data table to Google Sheets
result = await client.artifacts.export_data_table(
    nb_id,
    artifact_id="table_456",
    title="Research Data"
)
# result contains the Google Sheets URL

# Generic export (e.g., export any artifact to Sheets)
result = await client.artifacts.export(
    nb_id,
    artifact_id="artifact_789",
    title="Exported Content",
    export_type=ExportType.SHEETS
)
```
