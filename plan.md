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
    "video": true
  }
}
```

**Notes:**
- CLI arguments can override `output_directory`
- Set any artifact type to `false` to skip backing up that type

## CLI Usage
```bash
python main.py                    # Use config.json output directory
python main.py ./custom_backup    # Override output directory
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
    └── video/
        └── Video_Overview.mp4
```

## Implementation Steps

### 1. Project Setup
- [ ] Add `notebooklm` package to dependencies in pyproject.toml

### 2. Config File Support
- [ ] Create `config.json` with output_directory and artifact type settings
- [ ] Create `config.py` module to load and parse config
- [ ] Support CLI argument override for output directory

### 3. Utility Functions
- [ ] Create `sanitize_filename(title: str) -> str` function
  - Replace invalid filesystem characters (`:`, `/`, `\`, `*`, `?`, `"`, `<`, `>`, `|`) with underscores
  - Trim leading/trailing spaces and periods

### 4. Notebook Backup
- [ ] Fetch all notebooks using `await client.notebooks.list()`
- [ ] For each notebook:
  - Create folder named after notebook title (sanitized)
  - Save `notebook_info.json` with:
    - `id`: Notebook ID
    - `title`: Notebook title
    - `description`: AI-generated description (from `get_description()`)
    - `created_at`: Creation timestamp
    - `sources_count`: Number of sources

### 5. Notes Backup
- [ ] For each notebook, fetch notes using `await client.notes.list(notebook_id)`
- [ ] For each note:
  - Create markdown file with sanitized note title
  - Include note content in the markdown file
  - Save to `notes/` subfolder

### 6. Reports Backup
- [ ] For each notebook, list reports using `await client.artifacts.list_reports(notebook_id)`
- [ ] For each report:
  - Download as Markdown using `await client.artifacts.download_report()`
  - Save to `reports/` subfolder

### 7. Data Tables Backup
- [ ] For each notebook, list data tables using `await client.artifacts.list_data_tables(notebook_id)`
- [ ] For each data table:
  - Download as CSV using `await client.artifacts.download_data_table()`
  - Save to `data_tables/` subfolder

### 8. Audio Backup
- [ ] For each notebook, list audio using `await client.artifacts.list_audio(notebook_id)`
- [ ] For each audio file:
  - Download using `await client.artifacts.download_audio()`
  - Save to `audio/` subfolder

### 9. Video Backup
- [ ] For each notebook, list video using `await client.artifacts.list_video(notebook_id)`
- [ ] For each video file:
  - Download using `await client.artifacts.download_video()`
  - Save to `video/` subfolder

### 10. Progress Output
- [ ] Print notebook count when fetched
- [ ] Print note count and artifacts being saved
- [ ] Print summary at the end:
  - Total notebooks backed up
  - Total notes backed up
  - Total reports, data tables, audio, video files saved

## API References Used
- `client.notebooks.list()` - List all notebooks
- `client.notebooks.get_description()` - Get notebook description
- `client.notes.list()` - List all notes in a notebook
- `client.artifacts.list_reports()` - List report artifacts
- `client.artifacts.list_data_tables()` - List data table artifacts
- `client.artifacts.list_audio()` - List audio artifacts
- `client.artifacts.list_video()` - List video artifacts
- `client.artifacts.download_report()` - Download report as Markdown
- `client.artifacts.download_data_table()` - Download data table as CSV
- `client.artifacts.download_audio()` - Download audio file
- `client.artifacts.download_video()` - Download video file
