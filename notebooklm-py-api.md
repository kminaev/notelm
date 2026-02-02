# NotebookLM Python API Documentation

A summary of the `notebooklm-py` library API for programmatic access to NotebookLM features.

## Client Initialization

```python
from notebooklm import NotebookLMClient

async with await NotebookLMClient.from_storage() as client:
    # Perform operations
    pass
```

The client uses stored session information for authentication.

---

## Notebooks API (`client.notebooks`)

### Methods Overview

| Method | HTTP | Endpoint | Description |
|--------|------|----------|-------------|
| [`list()`](#list-all-notebooks) | GET | `/notebooks` | List all available notebooks |
| [`create(title)`](#create-notebook) | POST | `/notebooks` | Create a new notebook |
| [`get(notebook_id)`](#get-notebook) | GET | `/notebooks/{notebook_id}` | Get notebook details |
| [`delete(notebook_id)`](#delete-notebook) | DELETE | `/notebooks/{notebook_id}` | Delete a notebook |
| [`rename(notebook_id, new_title)`](#rename-notebook) | PUT | `/notebooks/{notebook_id}/rename` | Rename a notebook |
| [`get_description(notebook_id)`](#get-description) | GET | `/notebooks/{notebook_id}/description` | Get AI-generated description |
| [`get_summary(notebook_id)`](#get-summary) | GET | `/notebooks/{notebook_id}/summary` | Get raw AI summary |
| [`share(notebook_id, settings)`](#share-notebook) | POST | `/notebooks/{notebook_id}/share` | Share notebook |
| [`remove_from_recent(notebook_id)`](#remove-from-recent) | POST | `/notebooks/{notebook_id}/remove_from_recent` | Remove from recent list |
| [`get_raw(notebook_id)`](#get-raw-data) | GET | `/notebooks/{notebook_id}/raw` | Get raw API response |

---

### List All Notebooks

**`await client.notebooks.list()`**

Returns a list of all notebooks.

**Response:** `list[Notebook]` - Each Notebook contains `id`, `title`, `sources_count`

---

### Create Notebook

**`await client.notebooks.create(title: str)`**

Creates a new notebook with the specified title.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | str | Yes | Title for the new notebook |

**Response:** `Notebook` - The created notebook object

---

### Get Notebook

**`await client.notebooks.get(notebook_id: str)`**

Retrieves details for a specific notebook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |

**Response:** `Notebook` - Notebook object with details

---

### Delete Notebook

**`await client.notebooks.delete(notebook_id: str)`**

Deletes a specified notebook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook to delete |

**Response:** `bool` - True if deletion was successful

---

### Rename Notebook

**`await client.notebooks.rename(notebook_id: str, new_title: str)`**

Renames a notebook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `new_title` | str | Yes | The new title |

**Response:** `Notebook` - The updated notebook object

---

### Get Description

**`await client.notebooks.get_description(notebook_id: str)`**

Gets the AI-generated description and suggested topics.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |

**Response:** `NotebookDescription` with:
- `summary` (str): AI-generated summary
- `suggested_topics` (list): List of suggested questions

---

### Get Summary

**`await client.notebooks.get_summary(notebook_id: str)`**

Gets the raw AI-generated summary text.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |

**Response:** `str` - Raw summary text

---

### Share Notebook

**`await client.notebooks.share(notebook_id: str, settings: dict = None)`**

Shares a notebook with specified settings.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `settings` | dict | No | Sharing settings (e.g., `{"public": True}`) |

**Response:** `Any` - Result of share operation

---

### Remove from Recent

**`await client.notebooks.remove_from_recent(notebook_id: str)`**

Removes a notebook from the user's recently viewed list.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |

**Response:** `None`

---

### Get Raw Data

**`await client.notebooks.get_raw(notebook_id: str)`**

Retrieves raw API response data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |

**Response:** `Any` - Raw API response with notebook details and sources

---

## Sources API (`client.sources`)

### Methods Overview

| Method | HTTP | Endpoint | Description |
|--------|------|----------|-------------|
| [`list(notebook_id)`](#list-sources) | GET | `/notebooks/{notebook_id}/sources` | List all sources |
| [`get(notebook_id, source_id)`](#get-source) | GET | `/notebooks/{notebook_id}/sources/{source_id}` | Get source details |
| [`get_fulltext(notebook_id, source_id)`](#get-fulltext) | GET | `/notebooks/{notebook_id}/sources/{source_id}/fulltext` | Get indexed content |
| [`get_guide(notebook_id, source_id)`](#get-guide) | GET | `/notebooks/{notebook_id}/sources/{source_id}/guide` | Get AI summary & keywords |
| [`add_url(notebook_id, url)`](#add-url) | POST | `/notebooks/{notebook_id}/sources/add_url` | Add URL source |
| [`add_youtube(notebook_id, url)`](#add-youtube) | POST | `/notebooks/{notebook_id}/sources/add_youtube` | Add YouTube source |
| [`add_text(notebook_id, title, content)`](#add-text) | POST | `/notebooks/{notebook_id}/sources/add_text` | Add text source |
| [`add_file(notebook_id, path, mime_type=None)`](#add-file) | POST | `/notebooks/{notebook_id}/sources/add_file` | Upload file source |
| [`add_drive(notebook_id, file_id, title, mime_type)`](#add-drive) | POST | `/notebooks/{notebook_id}/sources/add_drive` | Add Google Drive source |
| [`rename(notebook_id, source_id, new_title)`](#rename-source) | PUT | `/notebooks/{notebook_id}/sources/{source_id}/rename` | Rename source |
| [`refresh(notebook_id, source_id)`](#refresh-source) | POST | `/notebooks/{notebook_id}/sources/{source_id}/refresh` | Refresh URL/Drive content |
| [`delete(notebook_id, source_id)`](#delete-source) | DELETE | `/notebooks/{notebook_id}/sources/{source_id}` | Delete source |

---

### List Sources

**`await client.sources.list(notebook_id: str)`**

Lists all sources in a notebook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |

**Response:** `list[Source]` - Each Source contains `id`, `title`, `source_type`

---

### Get Source

**`await client.sources.get(notebook_id: str, source_id: str)`**

Gets details for a specific source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `source_id` | str | Yes | The ID of the source |

**Response:** `Source` - Source object with details

---

### Get Fulltext

**`await client.sources.get_fulltext(notebook_id: str, source_id: str)`**

Gets the full indexed text content of a source (what NotebookLM uses for answers).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `source_id` | str | Yes | The ID of the source |

**Response:** `SourceFulltext` with:
- `content` (str): Full indexed content
- `char_count` (int): Character count

---

### Get Guide

**`await client.sources.get_guide(notebook_id: str, source_id: str)`**

Gets AI-generated summary and keywords for a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `source_id` | str | Yes | The ID of the source |

**Response:** `dict` with:
- `summary` (str): AI-generated summary
- `keywords` (list): List of keywords

---

### Add URL

**`await client.sources.add_url(notebook_id: str, url: str)`**

Adds a URL as a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `url` | str | Yes | The URL to add |

**Response:** `Source` - The newly added source

---

### Add YouTube

**`await client.sources.add_youtube(notebook_id: str, url: str)`**

Adds a YouTube video as a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `url` | str | Yes | The YouTube URL |

**Response:** `Source` - The newly added source

---

### Add Text

**`await client.sources.add_text(notebook_id: str, title: str, content: str)`**

Adds plain text content as a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `title` | str | Yes | Title for the text source |
| `content` | str | Yes | Text content |

**Response:** `Source` - The newly added source

---

### Add File

**`await client.sources.add_file(notebook_id: str, path: Path, mime_type: str = None)`**

Uploads a file as a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `path` | Path | Yes | File path to upload |
| `mime_type` | str | No | MIME type of the file |

**Response:** `Source` - The newly added source

---

### Add Google Drive

**`await client.sources.add_drive(notebook_id: str, file_id: str, title: str, mime_type: str)`**

Adds a Google Drive document as a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `file_id` | str | Yes | Google Drive file ID |
| `title` | str | Yes | Title of the document |
| `mime_type` | str | Yes | MIME type |

**Response:** `Source` - The newly added source

---

### Rename Source

**`await client.sources.rename(notebook_id: str, source_id: str, new_title: str)`**

Renames a source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `source_id` | str | Yes | The ID of the source |
| `new_title` | str | Yes | New title |

**Response:** `Source` - The updated source

---

### Refresh Source

**`await client.sources.refresh(notebook_id: str, source_id: str)`**

Refreshes content of a URL or Drive source.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `source_id` | str | Yes | The ID of the source |

**Response:** `bool` - True if refresh successful

---

### Delete Source

**`await client.sources.delete(notebook_id: str, source_id: str)`**

Deletes a source from a notebook.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `notebook_id` | str | Yes | The ID of the notebook |
| `source_id` | str | Yes | The ID of the source |

**Response:** `bool` - True if deletion successful

---

## Complete Usage Example

```python
import asyncio
from notebooklm import NotebookLMClient
from pathlib import Path

async def main():
    async with await NotebookLMClient.from_storage() as client:
        # List notebooks
        notebooks = await client.notebooks.list()
        print(f"Found {len(notebooks)} notebooks")

        # Create a notebook
        nb = await client.notebooks.create("API Test")
        print(f"Created: {nb.id}")

        # Add various source types
        await client.sources.add_url(nb.id, "https://example.com/article")
        await client.sources.add_youtube(nb.id, "https://youtube.com/watch?v=...")
        await client.sources.add_text(nb.id, "My Notes", "Content here...")
        await client.sources.add_file(nb.id, Path("./document.pdf"))

        # List sources
        sources = await client.sources.list(nb.id)
        for src in sources:
            print(f"{src.id}: {src.title} ({src.source_type})")

        # Get full indexed content
        if sources:
            fulltext = await client.sources.get_fulltext(nb.id, sources[0].id)
            print(f"Content ({fulltext.char_count} chars)")

            # Get AI summary
            guide = await client.sources.get_guide(nb.id, sources[0].id)
            print(f"Summary: {guide['summary']}")

        # Get notebook description
        desc = await client.notebooks.get_description(nb.id)
        print(f"Description: {desc.summary}")

asyncio.run(main())
```

---

## Type References

### Notebook
```python
{
    "id": str,           # Notebook ID (e.g., "nb-123")
    "title": str,        # Notebook title
    "sources_count": int # Number of sources
}
```

### Source
```python
{
    "id": str,        # Source ID (e.g., "src-abc")
    "title": str,     # Source title
    "source_type": str # Type: "URL", "YOUTUBE", "TEXT", "FILE", "DRIVE"
}
```

### NotebookDescription
```python
{
    "summary": str,                    # AI-generated summary
    "suggested_topics": [{"question": str}] # Suggested questions
}
```

### SourceFulltext
```python
{
    "content": str,   # Full indexed content
    "char_count": int # Character count
}
```
