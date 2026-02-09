# Plan: Add Infographic Export to NotebookLM Backup

## Current State
- Infographics are NOT currently exported in the backup application
- The notebooklm library supports infographics with:
  - `list_infographics(notebook_id)` - lists infographic artifacts
  - `download_infographic(notebook_id, output_path, artifact_id)` - downloads as PNG

## Files to Modify

### 1. config.py
Add `"infographics": True` to `get_default_config()` backup_artifact_types dictionary.

### 2. config.json
Add `"infographics": true` to `backup_artifact_types`.

### 3. main.py
Three changes:
1. Add `"infographics": 0` to stats dictionary
2. Add infographic backup logic (similar to slide_deck backup)
3. Add infographics count to final summary print

## Implementation

### Infographic Backup Logic Pattern
```python
# Backup infographics
if artifact_types.get("infographics", True):
    infographics = await client.artifacts.list_infographics(notebook.id)
    if infographics:
        infographics_folder = ensure_directory(notebook_folder / "infographics")
        print_progress(f"  Found {len(infographics)} infographics")
        
        for infographic in infographics:
            stats["infographics"] += 1
            infographic_filename = sanitize_filename(infographic.title) + ".png"
            infographic_path = infographics_folder / infographic_filename
            try:
                await client.artifacts.download_infographic(
                    notebook.id, str(infographic_path), infographic.id
                )
                print_progress(f"    Downloaded infographic: {infographic.title}")
            except Exception as e:
                print_error(f"    Failed to download infographic: {infographic.title} - {e}")
    else:
        print_progress(f"  Found 0 infographics")
```

## Output Structure
After implementation, backups will include:
```
notebook_name/
├── notebook_info.json
├── notes/
├── reports/
├── data_tables/
├── audio/
├── video/
├── slides/
├── infographics/     # NEW FOLDER
│   ├── infographic1.png
│   └── infographic2.png
└── fulltext/
```
