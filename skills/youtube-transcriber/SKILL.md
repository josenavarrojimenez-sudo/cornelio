---
name: youtube-transcriber
description: Transcribe YouTube videos using agent-browser for caption extraction. Use when you need to summarize, analyze, or extract information from YouTube videos. Triggers: "transcribe youtube", "get transcript", "summarize video", "analyze youtube video"
author: Cornelio
version: 1.0.0
triggers:
  - "transcribe youtube"
  - "get transcript"
  - "summarize video"
  - "analyze youtube video"
  - "ver video youtube"
  - "transcribir video"
metadata: {"clawdbot":{"emoji":"📺"}}
---

# YouTube Transcriber Skill

Extract transcripts from YouTube videos using headless browser automation.

## Method

Uses `agent-browser` to:
1. Open the YouTube video page
2. Click "Show transcript" button
3. Extract the caption/transcript text

## Usage

```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Requirements

- `agent-browser` installed and available in PATH
- Browser automation enabled

## Output

Returns plain text transcript with timestamps (if available)

## Notes

- Works even when YouTube blocks API requests from cloud IPs
- Uses headless Chromium via agent-browser
- Requires JavaScript rendering (not just static HTML)
