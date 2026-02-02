# NotebookLM Backup Application Plan

## Overview
A CLI application that backs up all your NotebookLM notebooks, notes, and artifacts to local Markdown files and other formats.

## Config File (config.json)
Create a `config.json` file in the project root with:
```json
{
  "output_directory": "./backups",
  "backup_artifact_types": {
    "reports": true,
    "data_tables": true,
    "audio": true,
    "video": true,
    "slides": true
  }
}
```

**Notes:**
- CLI arguments can override `output_directory`
- Set any artifact type to `false` to skip backing up that type
- Folders are created on-demand (only if artifacts exist)

## CLI Usage
```bash
python main.py                    # Use config.json output directory
python main.py ./custom_backup    # Override output directory
python main.py --delete           # Backup and delete notebooks from cloud
python main.py ./backup --delete  # Backup to custom dir and delete from cloud
```

## File Structure
```
output_directory/
└── Notebook_Title_1/
    ├── notebook_info.json
    ├── notes/
    │   ├── Note_Title_1.md
    │   └── Note_Title_2.md
    ├── reports/
    │   ├── Briefing_Doc.md
    │   └── Study_Guide.md
    ├── data_tables/
    │   └── Data_Table_1.csv
    ├── audio/
    │   └── Audio_Overview.mp4
    ├── video/
    │   └── Video_Overview.mp4
    ├── slides/
    │   └── Slide_Deck.pdf
    └── fulltext/
        ├── Source_Title_1.md
        └── Source_Title_2.md
```

**Note:** Artifact folders (`reports/`, `data_tables/`, `audio/`, `video/`, `slides/`, `fulltext/`) are only created if artifacts actually exist in the notebook.

## Fulltext Markdown Format
Each fulltext file includes metadata at the top:
```markdown
# Source Title

**Kind:** pdf

**URL:** https://example.com/document

---

Full indexed text content here...
```

## Implementation Steps

### 1. Project Setup
- [x] Add `notebooklm` package to dependencies in pyproject.toml

### 2. Config File Support
- [x] Create `config.json` with output_directory and artifact type settings
- [x] Create `config.py` module to load and parse config
- [x] Support CLI argument override for output directory
- [x] Add `--delete` flag to delete notebooks from cloud after backup

### 3. Utility Functions
- [x] Create `sanitize_filename(title: str) -> str` function
  - Replace invalid filesystem characters (`:`, `/`, `\`, `*`, `?`, `"`, `<`, `>`, `|`) with underscores
  - Trim leading/trailing spaces and periods

### 4. Notebook Backup
- [x] Fetch all notebooks using `await client.notebooks.list()`
- [x] For each notebook:
  - Create folder named after notebook title (sanitized)
  - Save `notebook_info.json` with:
    - `id`: Notebook ID
    - `title`: Notebook title
    - `description`: AI-generated description (from `get_description()`)
    - `suggested_topics`: List of suggested questions
    - `sources_count`: Number of sources

### 5. Notes Backup
- [x] For each notebook, fetch notes using `await client.notes.list(notebook_id)`
- [x] For each note:
  - Create markdown file with sanitized note title
  - Include note content in the markdown file
  - Save to `notes/` subfolder

### 6. Reports Backup
- [x] For each notebook, list reports using `await client.artifacts.list_reports(notebook_id)`
- [x] For each report:
  - Download as Markdown using `await client.artifacts.download_report()`
  - Save to `reports/` subfolder (only if reports exist)

### 7. Data Tables Backup
- [x] For each notebook, list data tables using `await client.artifacts.list_data_tables(notebook_id)`
- [x] For each data table:
  - Download as CSV using `await client.artifacts.download_data_table()`
  - Save to `data_tables/` subfolder (only if data tables exist)

### 8. Audio Backup
- [x] For each notebook, list audio using `await client.artifacts.list_audio(notebook_id)`
- [x] For each audio file:
  - Download using `await client.artifacts.download_audio()`
  - Save to `audio/` subfolder (only if audio files exist)

### 9. Video Backup
- [x] For each notebook, list video using `await client.artifacts.list_video(notebook_id)`
- [x] For each video file:
  - Download using `await client.artifacts.download_video()`
  - Save to `video/` subfolder (only if video files exist)

### 10. Slide Decks Backup
- [x] For each notebook, list slide decks using `await client.artifacts.list_slide_decks(notebook_id)`
- [x] For each slide deck:
  - Download as PDF using `await client.artifacts.download_slide_deck()`
  - Save to `slides/` subfolder (only if slide decks exist)

### 11. Fulltext Backup
- [x] For each notebook, list sources using `await client.sources.list(notebook_id)`
- [x] For each source:
  - Get fulltext using `await client.sources.get_fulltext(notebook_id, source_id)`
  - Create markdown file with:
    - `# {title}` - Source title as heading
    - `**Kind:** {source.kind}` - Source type (pdf, youtube, web_page, etc.)
    - `**URL:** {url}` - Original URL if available
    - Full content as body
  - Save to `fulltext/` subfolder (only if sources exist)

### 12. Delete from Cloud
- [x] Add `--delete` command-line argument (default: False)
- [x] After successful backup, delete notebook from cloud if `--delete` is specified
- [x] Show warning message when delete mode is enabled

### 13. Progress Output
- [x] Print notebook count when fetched
- [x] Print note count and artifacts being saved
- [x] Print folder creation messages (on-demand)
- [x] Print summary at the end:
  - Total notebooks backed up
  - Total notes, reports, data tables, audio, video, slides, fulltext files saved

## API References Used
- `client.notebooks.list()` - List all notebooks
- `client.notebooks.get_description()` - Get notebook description
- `client.notebooks.delete(notebook_id)` - Delete notebook from cloud
- `client.notes.list()` - List all notes in a notebook
- `client.notes.get()` - Get note content
- `client.sources.list()` - List all sources in a notebook
- `client.sources.get_fulltext()` - Get full indexed content of a source
- `client.artifacts.list_reports()` - List report artifacts
- `client.artifacts.list_data_tables()` - List data table artifacts
- `client.artifacts.list_audio()` - List audio artifacts
- `client.artifacts.list_video()` - List video artifacts
- `client.artifacts.list_slide_decks()` - List slide deck artifacts
- `client.artifacts.download_report()` - Download report as Markdown
- `client.artifacts.download_data_table()` - Download data table as CSV
- `client.artifacts.download_audio()` - Download audio file
- `client.artifacts.download_video()` - Download video file
- `client.artifacts.download_slide_deck()` - Download slide deck as PDF
