import asyncio
from notebooklm import NotebookLMClient

async def main():
    # Create client from saved authentication
    async with await NotebookLMClient.from_storage() as client:
        # List notebooks
        notebooks = await client.notebooks.list()
        print(f"Found {len(notebooks)} notebooks")

        counter = 0
        for notebook in notebooks:
            print(f"ID: {notebook.id}")
            print(f"Title: {notebook.title}")
            description = await client.notebooks.get_description(notebook.id)
        
            notes = await client.notes.list(notebook.id)
            print(f"Found {len(notes)} notes")

            for note in notes:
                print(f"Note ID: {note.id}")
                print(f"Note Title: {note.title}")
                note_data = await client.notes.get(notebook_id=notebook.id, note_id=note.id)
                print(f"Note Content: {note_data.content}")

            counter += 1
            if counter >= 2:
                break
            

       

if __name__ == "__main__":
    asyncio.run(main())
