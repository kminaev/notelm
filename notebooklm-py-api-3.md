
### AskResult

```python
@dataclass
class AskResult:
    answer: str                        # The answer text with inline citations [1], [2], etc.
    conversation_id: str               # ID for follow-up questions
    turn_number: int                   # Turn number in conversation
    is_follow_up: bool                 # Whether this was a follow-up question
    references: list[ChatReference]    # Source references cited in the answer
    raw_response: str                  # First 1000 chars of raw API response

@dataclass
class ChatReference:
    source_id: str                     # UUID of the source
    citation_number: int | None        # Citation number in answer (1, 2, etc.)
    cited_text: str | None             # Actual text passage being cited
    start_char: int | None             # Start position in source content
    end_char: int | None               # End position in source content
    chunk_id: str | None               # Internal chunk ID (for debugging)
```

**Important:** The `cited_text` field often contains only a snippet or section header, not the full quoted passage. The `start_char`/`end_char` positions reference NotebookLM's internal chunked index, which does not directly correspond to positions in the raw fulltext returned by `get_fulltext()`.

Use `SourceFulltext.find_citation_context()` to locate citations in the fulltext:

```python
fulltext = await client.sources.get_fulltext(notebook_id, ref.source_id)
matches = fulltext.find_citation_context(ref.cited_text)  # Returns list[(context, position)]

if matches:
    context, pos = matches[0]  # First match
    if len(matches) > 1:
        print(f"Warning: {len(matches)} matches found, using first")
else:
    context = None  # Not found - may occur if source was modified
```

**Tip:** Cache `fulltext` when processing multiple citations from the same source to avoid repeated API calls.

### ShareStatus

```python
@dataclass
class ShareStatus:
    notebook_id: str                   # The notebook ID
    is_public: bool                    # Whether publicly accessible
    access: ShareAccess                # RESTRICTED or ANYONE_WITH_LINK
    view_level: ShareViewLevel         # FULL_NOTEBOOK or CHAT_ONLY
    shared_users: list[SharedUser]     # List of users with access
    share_url: str | None              # Public URL if is_public=True
```

### SharedUser

```python
@dataclass
class SharedUser:
    email: str                         # User's email address
    permission: SharePermission        # OWNER, EDITOR, or VIEWER
    display_name: str | None           # User's display name
    avatar_url: str | None             # URL to user's avatar image
```

### SourceFulltext

```python
@dataclass
class SourceFulltext:
    source_id: str                     # UUID of the source
    title: str                         # Source title
    content: str                       # Full indexed text content
    url: str | None                    # Original URL (if applicable)
    char_count: int                    # Character count

    @property
    def kind(self) -> SourceType:
        """Get source type as SourceType enum."""

    def find_citation_context(
        self,
        cited_text: str,
        context_chars: int = 200,
    ) -> list[tuple[str, int]]:
        """Search for citation text, return list of (context, position) tuples."""
```

**Type Identification:**

Like `Source`, use the `.kind` property to get the source type:

```python
fulltext = await client.sources.get_fulltext(nb_id, source_id)
print(f"Content type: {fulltext.kind}")  # "pdf", "web_page", etc.
```

---

## Enums

### Audio Generation

```python
class AudioFormat(Enum):
    DEEP_DIVE = 1   # In-depth discussion
    BRIEF = 2       # Quick summary
    CRITIQUE = 3    # Critical analysis
    DEBATE = 4      # Two-sided debate

class AudioLength(Enum):
    SHORT = 1
    DEFAULT = 2
    LONG = 3
```

### Video Generation

```python
class VideoFormat(Enum):
    EXPLAINER = 1
    BRIEF = 2

class VideoStyle(Enum):
    AUTO_SELECT = 1
    CUSTOM = 2
    CLASSIC = 3
    WHITEBOARD = 4
    KAWAII = 5
    ANIME = 6
    WATERCOLOR = 7
    RETRO_PRINT = 8
    HERITAGE = 9
    PAPER_CRAFT = 10
```

### Quiz/Flashcards

```python
class QuizQuantity(Enum):
    FEWER = 1
    STANDARD = 2

class QuizDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
```

### Reports

```python
class ReportFormat(Enum):
    BRIEFING_DOC = 1
    STUDY_GUIDE = 2
    BLOG_POST = 3
    CUSTOM = 4
```

### Infographics

```python
class InfographicOrientation(Enum):
    LANDSCAPE = 1
    PORTRAIT = 2
    SQUARE = 3

class InfographicDetail(Enum):
    CONCISE = 1
    STANDARD = 2
    DETAILED = 3
```

### Slide Decks

```python
class SlideDeckFormat(Enum):
    DETAILED_DECK = 1
    PRESENTER_SLIDES = 2

class SlideDeckLength(Enum):
    DEFAULT = 1
    SHORT = 2
```

### Export

```python
class ExportType(Enum):
    DOCS = 1    # Export to Google Docs
    SHEETS = 2  # Export to Google Sheets
```

### Sharing

```python
class ShareAccess(Enum):
    RESTRICTED = 0        # Only explicitly shared users
    ANYONE_WITH_LINK = 1  # Public link access

class ShareViewLevel(Enum):
    FULL_NOTEBOOK = 0     # Chat + sources + notes
    CHAT_ONLY = 1         # Chat interface only

class SharePermission(Enum):
    OWNER = 1             # Full control (read-only, cannot assign)
    EDITOR = 2            # Can edit notebook
    VIEWER = 3            # Read-only access
```

### Source and Artifact Types

```python
class SourceType(str, Enum):
    """Source types - use with source.kind property.

    This is a str enum, enabling both enum and string comparisons:
        source.kind == SourceType.PDF   # True
        source.kind == "pdf"            # Also True
    """
    GOOGLE_DOCS = "google_docs"
    GOOGLE_SLIDES = "google_slides"
    GOOGLE_SPREADSHEET = "google_spreadsheet"
    PDF = "pdf"
    PASTED_TEXT = "pasted_text"
    WEB_PAGE = "web_page"
    YOUTUBE = "youtube"
    MARKDOWN = "markdown"
    DOCX = "docx"
    CSV = "csv"
    IMAGE = "image"
    MEDIA = "media"
    UNKNOWN = "unknown"

class ArtifactType(str, Enum):
    """Artifact types - use with artifact.kind property.

    This is a str enum that hides internal variant complexity.
    Quizzes and flashcards are distinguished automatically.
    """
    AUDIO = "audio"
    VIDEO = "video"
    REPORT = "report"
    QUIZ = "quiz"
    FLASHCARDS = "flashcards"
    MIND_MAP = "mind_map"
    INFOGRAPHIC = "infographic"
    SLIDE_DECK = "slide_deck"
    DATA_TABLE = "data_table"
    UNKNOWN = "unknown"

class SourceStatus(Enum):
    PROCESSING = 1  # Source is being processed (indexing content)
    READY = 2       # Source is ready for use
    ERROR = 3       # Source processing failed
    PREPARING = 5   # Source is being prepared/uploaded (pre-processing stage)
```

**Usage Example:**
```python
from notebooklm import SourceType, ArtifactType

# List sources by type using .kind property
sources = await client.sources.list(nb_id)
for src in sources:
    if src.kind == SourceType.PDF:
        print(f"PDF: {src.title}")
    elif src.kind == SourceType.MEDIA:
        print(f"Audio/Video: {src.title}")
    elif src.kind == SourceType.IMAGE:
        print(f"Image (OCR'd): {src.title}")
    elif src.kind == SourceType.UNKNOWN:
        print(f"Unknown type: {src.title}")

# List artifacts by type using .kind property
artifacts = await client.artifacts.list(nb_id)
for art in artifacts:
    if art.kind == ArtifactType.AUDIO:
        print(f"Audio: {art.title}")
    elif art.kind == ArtifactType.VIDEO:
        print(f"Video: {art.title}")
    elif art.kind == ArtifactType.QUIZ:
        print(f"Quiz: {art.title}")
```

### Chat Configuration

```python
class ChatGoal(Enum):
    DEFAULT = 1        # General purpose
    CUSTOM = 2         # Uses custom_prompt
    LEARNING_GUIDE = 3 # Educational focus

class ChatResponseLength(Enum):
    DEFAULT = 1
    LONGER = 4
    SHORTER = 5

class ChatMode(Enum):
    """Predefined chat modes for common use cases (service-level enum)."""
    DEFAULT = "default"          # General purpose
    LEARNING_GUIDE = "learning_guide"  # Educational focus
    CONCISE = "concise"          # Brief responses
    DETAILED = "detailed"        # Verbose responses
```

**ChatGoal vs ChatMode:**
- `ChatGoal` is an RPC-level enum used with `client.chat.configure()` for low-level API configuration
- `ChatMode` is a service-level enum providing predefined configurations for common use cases

---

## Advanced Usage

### Custom RPC Calls

For undocumented features, you can make raw RPC calls:

```python
from notebooklm.rpc import RPCMethod

async with await NotebookLMClient.from_storage() as client:
    # Access the core client for raw RPC
    result = await client._core.rpc_call(
        RPCMethod.SOME_METHOD,
        params=[...],
        source_path="/notebook/123"
    )
```

### Handling Rate Limits

Google rate limits aggressive API usage:

```python
import asyncio
from notebooklm import RPCError

async def safe_create_notebooks(client, titles):
    for title in titles:
        try:
            await client.notebooks.create(title)
        except RPCError:
            # Wait and retry on rate limit
            await asyncio.sleep(10)
            await client.notebooks.create(title)
        # Add delay between operations
        await asyncio.sleep(2)
```

### Streaming Chat Responses

The chat endpoint supports streaming (internal implementation):

```python
# Standard (non-streaming) - recommended
result = await client.chat.ask(nb_id, "Question")
print(result.answer)

# Streaming is handled internally by the library
# The ask() method returns the complete response
```