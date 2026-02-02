### https://github.com/teng-lin/notebooklm-py?tab=readme-ov-file


# Installation

# Basic installation
pip install notebooklm-py

# With browser login support (required for first-time setup)
pip install "notebooklm-py[browser]"
playwright install chromium

# 1. Authenticate (opens browser)
notebooklm login

# 2. Create a notebook and add sources
notebooklm create "My Research"
notebooklm use <notebook_id>
notebooklm source add "https://en.wikipedia.org/wiki/Artificial_intelligence"
notebooklm source add "./paper.pdf"

# 3. Chat with your sources
notebooklm ask "What are the key themes?"

# 4. Generate content
notebooklm generate audio "make it engaging" --wait
notebooklm generate video --style whiteboard --wait
notebooklm generate quiz --difficulty hard
notebooklm generate flashcards --quantity more
notebooklm generate slide-deck
notebooklm generate infographic --orientation portrait
notebooklm generate mind-map
notebooklm generate data-table "compare key concepts"

# 5. Download artifacts
notebooklm download audio ./podcast.mp3
notebooklm download video ./overview.mp4
notebooklm download quiz --format markdown ./quiz.md
notebooklm download flashcards --format json ./cards.json
notebooklm download slide-deck ./slides.pdf
notebooklm download mind-map ./mindmap.json
notebooklm download data-table ./data.csv