
**Generation Methods:**

```python
# Audio (podcast)
status = await client.artifacts.generate_audio(
    notebook_id,
    source_ids=None,           # List of source IDs (None = all)
    instructions="...",        # Custom instructions
    audio_format=AudioFormat.DEEP_DIVE,  # DEEP_DIVE, BRIEF, CRITIQUE, DEBATE
    audio_length=AudioLength.DEFAULT,    # SHORT, DEFAULT, LONG
    language="en"
)

# Video
status = await client.artifacts.generate_video(
    notebook_id,
    source_ids=None,
    instructions="...",
    video_format=VideoFormat.EXPLAINER,  # EXPLAINER, BRIEF
    video_style=VideoStyle.AUTO_SELECT,  # AUTO_SELECT, CLASSIC, WHITEBOARD, KAWAII, ANIME, etc.
    language="en"
)

# Report
status = await client.artifacts.generate_report(
    notebook_id,
    source_ids=None,
    title="...",
    description="...",
    format=ReportFormat.STUDY_GUIDE,  # BRIEFING_DOC, STUDY_GUIDE, BLOG_POST, CUSTOM
    language="en"
)

# Quiz
status = await client.artifacts.generate_quiz(
    notebook_id,
    source_ids=None,
    instructions="...",
    quantity=QuizQuantity.STANDARD,    # FEWER, STANDARD
    difficulty=QuizDifficulty.MEDIUM,  # EASY, MEDIUM, HARD
    language="en"
)
```

**Waiting for Completion:**

```python
# Start generation
status = await client.artifacts.generate_audio(nb_id)

# Wait with polling
final = await client.artifacts.wait_for_completion(
    nb_id,
    status.task_id,
    timeout=300,      # Max wait time in seconds
    poll_interval=5   # Seconds between polls
)

if final.is_complete:
    print(f"Download URL: {final.url}")
else:
    print(f"Failed or timed out: {final.status}")
```

---

### ChatAPI (`client.chat`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `ask(notebook_id, question, ...)` | `str, str, ...` | `AskResult` | Ask a question |
| `configure(notebook_id, ...)` | `str, ...` | `bool` | Set chat persona |
| `get_history(notebook_id)` | `str` | `list[ConversationTurn]` | Get conversation |

**ask() Parameters:**
```python
async def ask(
    notebook_id: str,
    question: str,
    source_ids: list[str] | None = None,  # Limit to specific sources (None = all)
    conversation_id: str | None = None,   # Continue existing conversation
) -> AskResult
```

**Example:**
```python
# Ask questions (uses all sources)
result = await client.chat.ask(nb_id, "What are the main themes?")
print(result.answer)

# Access source references (cited in answer as [1], [2], etc.)
for ref in result.references:
    print(f"Citation {ref.citation_number}: Source {ref.source_id}")

# Ask using only specific sources
result = await client.chat.ask(
    nb_id,
    "Summarize the key points",
    source_ids=["src_001", "src_002"]
)

# Continue conversation
result = await client.chat.ask(
    nb_id,
    "Can you elaborate on the first point?",
    conversation_id=result.conversation_id
)

# Configure persona
await client.chat.configure(
    nb_id,
    goal=ChatGoal.LEARNING_GUIDE,
    response_length=ChatResponseLength.LONGER,
    custom_prompt="Focus on practical applications"
)
```

---

### ResearchAPI (`client.research`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start(notebook_id, query, source, mode)` | `str, str, str="web", str="fast"` | `dict` | Start research (mode: "fast" or "deep") |
| `poll(notebook_id)` | `str` | `dict` | Check research status |
| `import_sources(notebook_id, task_id, sources)` | `str, str, list` | `list[dict]` | Import findings |

**Method Signatures:**

```python
async def start(
    notebook_id: str,
    query: str,
    source: str = "web",   # "web" or "drive"
    mode: str = "fast",    # "fast" or "deep" (deep only for web)
) -> dict:
    """
    Returns: {"task_id": str, "report_id": str, "notebook_id": str, "query": str, "mode": str}
    Raises: ValueError if source/mode combination is invalid
    """

async def poll(notebook_id: str) -> dict:
    """
    Returns: {"task_id": str, "status": str, "query": str, "sources": list, "summary": str}
    Status is "completed", "in_progress", or "no_research"
    """

async def import_sources(notebook_id: str, task_id: str, sources: list[dict]) -> list[dict]:
    """
    sources: List of dicts with 'url' and 'title' keys
    Returns: List of imported sources with 'id' and 'title'
    """
```

**Example:**
```python
# Start fast web research (default)
result = await client.research.start(nb_id, "AI safety regulations")
task_id = result["task_id"]

# Start deep web research
result = await client.research.start(nb_id, "quantum computing", source="web", mode="deep")
task_id = result["task_id"]

# Start fast Drive research
result = await client.research.start(nb_id, "project docs", source="drive", mode="fast")

# Poll until complete
import asyncio
while True:
    status = await client.research.poll(nb_id)
    if status["status"] == "completed":
        break
    await asyncio.sleep(10)

# Import discovered sources
imported = await client.research.import_sources(nb_id, task_id, status["sources"][:5])
print(f"Imported {len(imported)} sources")
```

---

### NotesAPI (`client.notes`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `list(notebook_id)` | `str` | `list[Note]` | List text notes (excludes mind maps) |
| `create(notebook_id, title="New Note", content="")` | `str, str, str` | `Note` | Create note |
| `get(notebook_id, note_id)` | `str, str` | `Optional[Note]` | Get note by ID |
| `update(notebook_id, note_id, content, title)` | `str, str, str, str` | `None` | Update note content and title |
| `delete(notebook_id, note_id)` | `str, str` | `bool` | Delete note |
| `list_mind_maps(notebook_id)` | `str` | `list[Any]` | List mind maps in the notebook |
| `delete_mind_map(notebook_id, mind_map_id)` | `str, str` | `bool` | Delete a mind map |

**Example:**
```python
# Create and manage notes
note = await client.notes.create(nb_id, title="Meeting Notes", content="Discussion points...")
notes = await client.notes.list(nb_id)

# Update a note
await client.notes.update(nb_id, note.id, "Updated content", "New Title")

# Delete a note
await client.notes.delete(nb_id, note.id)
```

**Mind Maps:**

Mind maps are stored internally using the same structure as notes but contain JSON data with hierarchical node information. The `list()` method excludes mind maps automatically, while `list_mind_maps()` returns only mind maps.

```python
# List all mind maps in a notebook
mind_maps = await client.notes.list_mind_maps(nb_id)
for mm in mind_maps:
    mm_id = mm[0]  # Mind map ID is at index 0
    print(f"Mind map: {mm_id}")

# Delete a mind map
await client.notes.delete_mind_map(nb_id, mind_map_id)
```

**Note:** Mind maps are detected by checking if the content contains `'"children":' or `'"nodes":'` keys, which indicate JSON mind map data structure.

---

### SettingsAPI (`client.settings`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_output_language()` | none | `Optional[str]` | Get current output language setting |
| `set_output_language(language)` | `str` | `Optional[str]` | Set output language for artifact generation |

**Example:**
```python
# Get current language setting
lang = await client.settings.get_output_language()
print(f"Current language: {lang}")  # e.g., "en", "ja", "zh_Hans"

# Set language for artifact generation
result = await client.settings.set_output_language("ja")  # Japanese
print(f"Language set to: {result}")
```

**Important:** Language is a **GLOBAL setting** that affects all notebooks in your account. Supported languages include:
- `en` (English), `ja` (日本語), `zh_Hans` (中文简体), `zh_Hant` (中文繁體)
- `ko` (한국어), `es` (Español), `fr` (Français), `de` (Deutsch), `pt_BR` (Português)
- And [80+ other languages](cli-reference.md#language-commands)

---

### SharingAPI (`client.sharing`)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_status(notebook_id)` | `str` | `ShareStatus` | Get current sharing configuration |
| `set_public(notebook_id, public)` | `str, bool` | `ShareStatus` | Enable/disable public link sharing |
| `set_view_level(notebook_id, level)` | `str, ShareViewLevel` | `None` | Set what viewers can access |
| `add_user(notebook_id, email, permission, notify, welcome_message)` | `str, str, SharePermission, bool, str` | `ShareStatus` | Share with a user |
| `update_user(notebook_id, email, permission)` | `str, str, SharePermission` | `ShareStatus` | Update user's permission |
| `remove_user(notebook_id, email)` | `str, str` | `ShareStatus` | Remove user's access |

**Example:**
```python
from notebooklm import SharePermission, ShareViewLevel

# Get current sharing status
status = await client.sharing.get_status(notebook_id)
print(f"Public: {status.is_public}")
print(f"Users: {[u.email for u in status.shared_users]}")

# Enable public sharing (anyone with link)
status = await client.sharing.set_public(notebook_id, True)
print(f"Share URL: {status.share_url}")

# Set view level (what viewers can access)
await client.sharing.set_view_level(notebook_id, ShareViewLevel.CHAT_ONLY)

# Share with specific users
status = await client.sharing.add_user(
    notebook_id,
    "colleague@example.com",
    SharePermission.VIEWER,
    notify=True,
    welcome_message="Check out my research!"
)

# Update user permission
status = await client.sharing.update_user(
    notebook_id,
    "colleague@example.com",
    SharePermission.EDITOR
)

# Remove user access
status = await client.sharing.remove_user(notebook_id, "colleague@example.com")

# Disable public sharing
status = await client.sharing.set_public(notebook_id, False)
```

**Permission Levels:**
- `SharePermission.OWNER` - Full control (read-only, cannot be assigned)
- `SharePermission.EDITOR` - Can edit notebook content
- `SharePermission.VIEWER` - Read-only access

**View Levels:**
- `ShareViewLevel.FULL_NOTEBOOK` - Viewers can access chat, sources, and notes
- `ShareViewLevel.CHAT_ONLY` - Viewers can only access the chat interface

---

## Data Types

### Notebook

```python
@dataclass
class Notebook:
    id: str
    title: str
    created_at: Optional[datetime]
    sources_count: int
    is_owner: bool
```

### Source

```python
@dataclass
class Source:
    id: str
    title: Optional[str]
    url: Optional[str]
    created_at: Optional[datetime]

    @property
    def kind(self) -> SourceType:
        """Get source type as SourceType enum."""
```

**Type Identification:**

Use the `.kind` property to identify source types. It returns a `SourceType` enum which is also a `str`, enabling both enum and string comparisons:

```python
from notebooklm import SourceType

# Enum comparison (recommended)
if source.kind == SourceType.PDF:
    print("This is a PDF")

# String comparison (also works)
if source.kind == "pdf":
    print("This is a PDF")

# Use in f-strings
print(f"Type: {source.kind}")  # "Type: pdf"
```

### Artifact

```python
@dataclass
class Artifact:
    id: str
    title: str
    status: int                     # 1=processing, 2=pending, 3=completed
    created_at: Optional[datetime]
    url: Optional[str]

    @property
    def kind(self) -> ArtifactType:
        """Get artifact type as ArtifactType enum."""

    @property
    def is_completed(self) -> bool:
        """Check if artifact generation is complete."""

    @property
    def is_quiz(self) -> bool:
        """Check if this is a quiz artifact."""

    @property
    def is_flashcards(self) -> bool:
        """Check if this is a flashcards artifact."""
```

**Type Identification:**

Use the `.kind` property to identify artifact types. It returns an `ArtifactType` enum which is also a `str`:

```python
from notebooklm import ArtifactType

# Enum comparison (recommended)
if artifact.kind == ArtifactType.AUDIO:
    print("This is an audio overview")

# String comparison (also works)
if artifact.kind == "audio":
    print("This is an audio overview")

# Check specific types
if artifact.is_quiz:
    print("This is a quiz")
elif artifact.is_flashcards:
    print("This is a flashcard deck")
```

