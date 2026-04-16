---
name: youtube-transcript
description: Get YouTube video transcripts using youtube-transcript-api. Works when yt-dlp is blocked by YouTube. Use when: user shares a YouTube URL and wants transcript/summary.
author: Cornelio
version: 1.0.0
triggers:
  - "youtube transcript"
  - "summarize youtube"
  - "ver transcript"
  - "resumir video youtube"
---

# YouTube Transcript

Get transcripts from YouTube videos using the python youtube-transcript-api library.

## Usage

```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Notes
- Uses youtube-transcript-api (v2 API with `fetch` method)
- Falls back to auto-generated subtitles if manual ones aren't available
- If both fail, video has no transcript available (YouTube may block cloud IPs)
- API changed from `get_transcript` to `fetch` in v2
