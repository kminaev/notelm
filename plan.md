I  need a plan of writing  application that will backup my notebooklm notes.
THe application shoud list all my notebooklm files
for each file it should create a local folder to save notebook notes, and articatcat such as reports and data tables (id exists). The folder should be named as notebook title (do not forget to chage all unrelevant to file system chars with undescore)
Then app should list notes in the notebook and for each note it should create a markdown file with the note content and save it in the notebook folder. The markdown file should be named as note title (do not forget to chage all unrelevant to file system chars with undescore) and should include the note content, and if exists, the note report and data tables in the same markdown file.

Here is the plan:

1. **Setup and Initialization**:
   - Install necessary libraries (e.g., `requests`, `python-dotenv`, `markdown`, `os`, `shutil`).
   - Set up environment variables for NotebookLM API credentials.

2. **Fetch Notebooks**:
   - Use the NotebookLM API to list all notebooks.
   - For each notebook, create a local folder named after the notebook title (sanitized to remove invalid filesystem characters).

3. **Fetch Notes**:
   - For each notebook, fetch all notes.
   - For each note, create a markdown file named after the note title (sanitized to remove invalid filesystem characters).

4. **Save Note Content**:
   - Save the note content, report (if exists), and data tables (if exists) in the markdown file(s).
   - Ensure the markdown file includes the note content, report, and data tables in a structured format.