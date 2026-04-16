#!/usr/bin/env python3
"""Get YouTube video transcript using youtube-transcript-api."""
import sys
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/)([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'embed/([a-zA-Z0-9_-]{11})',
        r'shorts/([a-zA-Z0-9_-]{11})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url.strip()):
        return url.strip()
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_transcript.py <youtube_url>")
        sys.exit(1)

    video_id = extract_video_id(sys.argv[1])
    if not video_id:
        print("Error: Could not extract video ID")
        sys.exit(1)

    # List available transcripts
    available = YouTubeTranscriptApi.list(video_id)
    # Fetch the first available transcript
    transcript = YouTubeTranscriptApi.fetch(
        video_id,
        languages=available.transcript_ids[:1] if available.transcript_ids else None,
    )

    for snippet in transcript.snippets:
        text = snippet.text.replace("\n", " ").strip()
        if text:
            print(text)


if __name__ == "__main__":
    main()
