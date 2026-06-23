---
name: content-curation-and-feeds
description: Track, monitor, and reformat content from public feeds and video platforms. Integrates RSS/Atom blog tracking (blogwatcher-cli) and YouTube transcript extraction/summarization.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [content, curation, RSS, feed-reader, blogs, youtube, transcript, summary, monitoring]
    related_skills: [google-workspace, obsidian]
---

# Content Curation & Feed Monitoring

This skill covers tracking, monitoring, and reformatting incoming public content feeds (blogs, RSS/Atom feeds) and public video transcripts (YouTube) to build summaries, knowledge base notes, or social media threads.

---

## 1. Blog & RSS Monitoring (blogwatcher)

Track blog and RSS/Atom feed updates using the `blogwatcher-cli` tool. Supports feed auto-discovery, HTML scraping fallback, OPML imports, and read/unread article management.

### Prerequisites
`blogwatcher-cli` installed. Database path defaults to `~/.blogwatcher-cli/blogwatcher-cli.db` (persistent Docker volume: `-v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db`).

### Common Commands
- **Add Blog:** `blogwatcher-cli add "My Blog" https://example.com`
- **List Tracked Blogs:** `blogwatcher-cli blogs`
- **Scan Feeds:** `blogwatcher-cli scan`
- **List Unread Articles:** `blogwatcher-cli articles`
- **Mark Article Read:** `blogwatcher-cli read <ID>`
- **Mark All Read:** `blogwatcher-cli read-all`

---

## 2. YouTube Content Parsing (youtube-content)

Extract transcripts from YouTube videos (standard URLs, shorts, embeds, or raw 11-char IDs) and reformat them into structured summaries, chapters, blog posts, or social media threads.

### Prerequisites
```bash
pip install youtube-transcript-api
```

### CLI Transcript Extraction
- **JSON with metadata:** `python3 ~/.hermes/skills/media/content-curation-and-feeds/scripts/fetch_transcript.py "URL"`
- **Plain text only:** `python3 ~/.hermes/skills/media/content-curation-and-feeds/scripts/fetch_transcript.py "URL" --text-only`
- **With timestamps:** `python3 ~/.hermes/skills/media/content-curation-and-feeds/scripts/fetch_transcript.py "URL" --timestamps`

### Synthesis & Output Formats
After fetching a transcript, transform it into one of these desired shapes:
- **Chapters:** Chronological list of topics with timestamps.
- **Summary:** Concise 5-10 sentence overview of the video.
- **Twitter Thread:** Numbered posts (each under 280 characters).
- **Blog Post:** Clean markdown article with headers, sections, and takeaways.

---

## Guidelines & Error Handling

- **Large Transcripts:** If a video transcript exceeds 50K characters, split it into overlapping chunks (~40K chars, 2K overlap), summarize each chunk, and synthesize the summaries.
- **Scanned/No Transcript:** If transcripts are disabled or unavailable, notify the user.
- **Database Backups:** Keep the blogwatcher SQLite database backed up regularly if monitoring high-value feeds.
