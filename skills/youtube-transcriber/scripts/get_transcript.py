#!/usr/bin/env python3
"""
YouTube Video Transcriber using agent-browser
Extracts captions/transcripts from YouTube videos even when blocked from cloud IPs.
"""

import sys
import json
import subprocess
import re
import time


def get_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\?/]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def run_agent(cmd):
    """Run agent-browser command and return output."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, timeout=60
    )
    return result.stdout, result.stderr, result.returncode


def get_transcript(video_url):
    """Main function to get transcript from a YouTube video."""
    video_id = get_video_id(video_url)
    if not video_id:
        return {"error": "Could not extract video ID from URL"}
    
    print(f"Opening video {video_id}...", file=sys.stderr)
    
    # Open the video
    stdout, stderr, code = run_agent(f'agent-browser open "{video_url}"')
    if code != 0:
        return {"error": f"Failed to open video: {stderr}"}
    
    time.sleep(3)  # Wait for page load
    
    # Get snapshot to find transcript button
    stdout, _, _ = run_agent('agent-browser snapshot -i --json')
    try:
        snapshot = json.loads(stdout)
    except:
        return {"error": f"Failed to parse snapshot: {stdout[:500]}"}
    
    refs = snapshot.get('data', {}).get('refs', {})
    
    # Find transcript button or "..." more button
    transcript_ref = None
    for ref, info in refs.items():
        name = info.get('name', '').lower()
        if 'transcript' in name:
            transcript_ref = ref
            break
    
    if not transcript_ref:
        # Find "..." button
        for ref, info in refs.items():
            if info.get('role') == 'button' and '...' in info.get('name', ''):
                transcript_ref = ref
                print(f"Found 'more' button: {ref}", file=sys.stderr)
                break
    
    if transcript_ref:
        run_agent(f'agent-browser click @{transcript_ref}')
        time.sleep(2)
        
        # Get updated snapshot
        stdout, _, _ = run_agent('agent-browser snapshot -i --json')
        try:
            snapshot = json.loads(stdout)
            snapshot_text = snapshot.get('data', {}).get('snapshot', '')
            
            # Extract timestamped lines that look like transcript
            lines = snapshot_text.split('\n')
            transcript_lines = []
            for line in lines:
                # Match timestamps like "0:00", "1:23", "12:34"
                if re.match(r'^\d{1,2}:\d{2}', line.strip()):
                    transcript_lines.append(line.strip())
            
            if transcript_lines:
                return {
                    "success": True,
                    "video_id": video_id,
                    "transcript": '\n'.join(transcript_lines)
                }
        except Exception as e:
            return {"error": f"Failed to parse transcript: {e}"}
    
    return {
        "error": "Could not find transcript button. Try manually clicking 'Show transcript'.",
        "video_id": video_id
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_transcript.py <youtube_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = get_transcript(url)
    
    if result.get('error'):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Video ID: {result.get('video_id')}")
    print("\n=== TRANSCRIPT ===\n")
    print(result.get('transcript', 'No transcript found'))


if __name__ == "__main__":
    main()
