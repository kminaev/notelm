#!/usr/bin/env python3
"""
NotebookLM Backup Application

A CLI application that backs up all your NotebookLM notebooks, notes, 
and artifacts to local Markdown files and other formats.

Usage:
    python main.py                    # Use config.json output directory
    python main.py ./custom_backup    # Override output directory
    python main.py --delete           # Backup and delete notebooks from cloud
"""

import argparse
import asyncio
import json
from pathlib import Path

from notebooklm import NotebookLMClient

import config
from utils import (
    ensure_directory,
    print_error,
    print_progress,
    print_summary,
    sanitize_filename,
)


async def backup_notebooks(
    client: NotebookLMClient,
    output_dir: Path,
    artifact_types: dict[str, bool],
    delete_from_cloud: bool = False,
) -> dict[str, int]:
    """Backup all notebooks and their contents.
    
    Args:
        client: The NotebookLM client.
        output_dir: The base output directory.
        artifact_types: Dictionary of which artifact types to backup.
        delete_from_cloud: If True, delete notebooks from cloud after backup.
    
    Returns:
        Dictionary with backup statistics.
    """
    stats = {
        "notebooks": 0,
        "notes": 0,
        "reports": 0,
        "data_tables": 0,
        "audio": 0,
        "video": 0,
        "slides": 0,
        "fulltext": 0,
    }
    
    # Fetch all notebooks
    print_progress("Fetching notebooks...")
    notebooks = await client.notebooks.list()
    print_summary(f"Found {len(notebooks)} notebooks")
    
    for notebook in notebooks:
        stats["notebooks"] += 1
        
        # Create notebook folder
        notebook_folder_name = sanitize_filename(notebook.title)
        notebook_folder = ensure_directory(output_dir / notebook_folder_name)
        print_progress(f"Backing up notebook: {notebook.title}")
        
        # Save notebook info
        notebook_info = {
            "id": notebook.id,
            "title": notebook.title,
            "sources_count": notebook.sources_count,
        }
        
        # Get description if available
        try:
            description = await client.notebooks.get_description(notebook.id)
            notebook_info["description"] = description.summary
            notebook_info["suggested_topics"] = [
                topic.question for topic in description.suggested_topics
            ]
        except Exception:
            notebook_info["description"] = None
        
        notebook_info_path = notebook_folder / "notebook_info.json"
        with open(notebook_info_path, "w", encoding="utf-8") as f:
            json.dump(notebook_info, f, indent=2, ensure_ascii=False)
        
        # Backup notes
        notes_folder = ensure_directory(notebook_folder / "notes")
        notes = await client.notes.list(notebook.id)
        print_progress(f"  Found {len(notes)} notes in notebook")
        
        for note in notes:
            stats["notes"] += 1
            note_data = await client.notes.get(notebook.id, note.id)
            note_filename = sanitize_filename(note.title) + ".md"
            note_path = notes_folder / note_filename
            
            # Create markdown content
            markdown_content = f"# {note.title}\n\n"
            if note_data.content:
                markdown_content += note_data.content
            
            with open(note_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
        
        # Backup reports
        if artifact_types.get("reports", True):
            reports = await client.artifacts.list_reports(notebook.id)
            if reports:
                reports_folder = ensure_directory(notebook_folder / "reports")
                print_progress(f"  Found {len(reports)} reports")
                
                for report in reports:
                    stats["reports"] += 1
                    report_filename = sanitize_filename(report.title) + ".md"
                    report_path = reports_folder / report_filename
                    try:
                        await client.artifacts.download_report(
                            notebook.id, str(report_path), report.id
                        )
                        print_progress(f"    Downloaded report: {report.title}")
                    except Exception as e:
                        print_error(f"    Failed to download report: {report.title} - {e}")
            else:
                print_progress(f"  Found 0 reports")
        
        # Backup data tables
        if artifact_types.get("data_tables", True):
            data_tables = await client.artifacts.list_data_tables(notebook.id)
            if data_tables:
                data_tables_folder = ensure_directory(notebook_folder / "data_tables")
                print_progress(f"  Found {len(data_tables)} data tables")
                
                for dt in data_tables:
                    stats["data_tables"] += 1
                    dt_filename = sanitize_filename(dt.title) + ".csv"
                    dt_path = data_tables_folder / dt_filename
                    try:
                        await client.artifacts.download_data_table(
                            notebook.id, str(dt_path), dt.id
                        )
                        print_progress(f"    Downloaded data table: {dt.title}")
                    except Exception as e:
                        print_error(
                            f"    Failed to download data table: {dt.title} - {e}"
                        )
            else:
                print_progress(f"  Found 0 data tables")
        
        # Backup audio
        if artifact_types.get("audio", True):
            audio_files = await client.artifacts.list_audio(notebook.id)
            if audio_files:
                audio_folder = ensure_directory(notebook_folder / "audio")
                print_progress(f"  Found {len(audio_files)} audio files")
                
                for audio in audio_files:
                    stats["audio"] += 1
                    audio_filename = sanitize_filename(audio.title)
                    audio_path = audio_folder / f"{audio_filename}.mp4"
                    try:
                        await client.artifacts.download_audio(
                            notebook.id, str(audio_path), audio.id
                        )
                        print_progress(f"    Downloaded audio: {audio.title}")
                    except Exception as e:
                        print_error(f"    Failed to download audio: {audio.title} - {e}")
            else:
                print_progress(f"  Found 0 audio files")
        
        # Backup video
        if artifact_types.get("video", True):
            video_files = await client.artifacts.list_video(notebook.id)
            if video_files:
                video_folder = ensure_directory(notebook_folder / "video")
                print_progress(f"  Found {len(video_files)} video files")
                
                for video in video_files:
                    stats["video"] += 1
                    video_filename = sanitize_filename(video.title)
                    video_path = video_folder / f"{video_filename}.mp4"
                    try:
                        await client.artifacts.download_video(
                            notebook.id, str(video_path), video.id
                        )
                        print_progress(f"    Downloaded video: {video.title}")
                    except Exception as e:
                        print_error(f"    Failed to download video: {video.title} - {e}")
            else:
                print_progress(f"  Found 0 video files")
        
        # Backup slide decks
        if artifact_types.get("slides", True):
            slide_decks = await client.artifacts.list_slide_decks(notebook.id)
            if slide_decks:
                slides_folder = ensure_directory(notebook_folder / "slides")
                print_progress(f"  Found {len(slide_decks)} slide decks")
                
                for slide in slide_decks:
                    stats["slides"] += 1
                    slides_filename = sanitize_filename(slide.title) + ".pdf"
                    slides_path = slides_folder / slides_filename
                    try:
                        await client.artifacts.download_slide_deck(
                            notebook.id, str(slides_path), slide.id
                        )
                        print_progress(f"    Downloaded slide deck: {slide.title}")
                    except Exception as e:
                        print_error(f"    Failed to download slide deck: {slide.title} - {e}")
            else:
                print_progress(f"  Found 0 slide decks")
        
        # Backup fulltext for each source
        sources = await client.sources.list(notebook.id)
        if sources:
            fulltext_folder = ensure_directory(notebook_folder / "fulltext")
            print_progress(f"  Found {len(sources)} sources")
            
            for source in sources:
                try:
                    fulltext = await client.sources.get_fulltext(
                        notebook.id, source.id
                    )
                    stats["fulltext"] += 1
                    # Use source title for filename, fallback to source id
                    if source.title:
                        source_filename = sanitize_filename(source.title) + ".md"
                    else:
                        source_filename = f"{source.id}.md"
                    fulltext_path = fulltext_folder / source_filename
                    
                    # Create markdown content with metadata
                    markdown_content = f"# {source.title or 'Untitled Source'}\n\n"
                    markdown_content += f"**Kind:** {source.kind}\n\n"
                    if fulltext.url:
                        markdown_content += f"**URL:** {fulltext.url}\n\n"
                    markdown_content += f"---\n\n"
                    markdown_content += fulltext.content
                    
                    with open(fulltext_path, "w", encoding="utf-8") as f:
                        f.write(markdown_content)
                    print_progress(f"    Downloaded fulltext: {source.title or source.id}")
                except Exception as e:
                    print_error(
                        f"    Failed to download fulltext: {source.title or source.id} - {e}"
                    )
        else:
            print_progress(f"  Found 0 sources")
        
        # Delete from cloud if requested
        if delete_from_cloud:
            try:
                await client.notebooks.delete(notebook.id)
                print_progress(f"  Deleted notebook from cloud: {notebook.title}")
            except Exception as e:
                print_error(f"    Failed to delete notebook: {notebook.title} - {e}")
    
    return stats


async def main() -> None:
    """Main entry point for the backup application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Backup your NotebookLM notebooks, notes, and artifacts."
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=None,
        help="Output directory for backups (overrides config.json setting)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config.json file",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        default=False,
        help="Delete notebooks from cloud after backing up",
    )
    args = parser.parse_args()
    
    # Load configuration
    cfg = config.load_config(args.config)
    
    # Determine output directory (CLI arg overrides config)
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = config.get_output_directory(cfg)
    
    # Get artifact types to backup
    artifact_types = config.get_artifact_types(cfg)
    
    print_summary("Starting NotebookLM backup...")
    print_summary(f"Output directory: {output_dir}")
    if args.delete:
        print_summary("WARNING: Notebooks will be DELETED from cloud after backup!")
    
    # Ensure output directory exists
    ensure_directory(output_dir)
    
    # Create client and backup
    async with await NotebookLMClient.from_storage() as client:
        stats = await backup_notebooks(
            client, output_dir, artifact_types, args.delete
        )
    
    # Print final summary
    print_summary("Backup complete!")
    print_summary(f"  Notebooks: {stats['notebooks']}")
    print_summary(f"  Notes: {stats['notes']}")
    print_summary(f"  Reports: {stats['reports']}")
    print_summary(f"  Data Tables: {stats['data_tables']}")
    print_summary(f"  Audio Files: {stats['audio']}")
    print_summary(f"  Video Files: {stats['video']}")
    print_summary(f"  Slide Decks: {stats['slides']}")
    print_summary(f"  Fulltext Files: {stats['fulltext']}")
    print_summary(f"Total items backed up: {sum(stats.values())}")
    
    if args.delete:
        print_summary("Notebooks have been deleted from cloud.")


if __name__ == "__main__":
    asyncio.run(main())
