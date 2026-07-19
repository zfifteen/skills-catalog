#!/usr/bin/env python3
"""
youtube_transcript.py — Grok-ported YouTube transcript & metadata extractor.

Original from Codex "youtube" skill. Functional equivalent for Grok environments.

Primary objective (preserved): Obtain the transcript first. All summaries, claims,
or notes must be derived from the actual transcript text, never from metadata alone.

Usage (invoke via run_terminal_cmd in Grok):
  python3 /abs/path/to/skills/ported-from-codex/youtube/scripts/youtube_transcript.py metadata "https://www.youtube.com/watch?v=VIDEOID"
  python3 ... transcript "https://..." [--json] [--languages en,es]

  JSON output for machine consumption; plain for human-readable timestamped transcript.

Dependencies (checked at runtime with helpful install instructions):
  yt-dlp, youtube-transcript-api

The script prefers manually-created captions over auto-generated.
"""

import argparse
import json
import re
import sys
from urllib.parse import parse_qs, urlparse


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


try:
    import yt_dlp
except ImportError:
    fail(
        "Missing dependency: yt-dlp. Install with: "
        "python3 -m pip install --target /tmp/grok-youtube-deps yt-dlp youtube-transcript-api",
        2,
    )

try:
    from youtube_transcript_api import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
        YouTubeTranscriptApi,
    )
except ImportError:
    fail(
        "Missing dependency: youtube-transcript-api. Install with: "
        "python3 -m pip install --target /tmp/grok-youtube-deps yt-dlp youtube-transcript-api",
        2,
    )


def parse_video_id(value: str) -> str:
    value = value.strip()
    if re.fullmatch(r"[\w-]{11}", value):
        return value

    parsed = urlparse(value)
    host = parsed.netloc.lower()
    path = parsed.path

    if host in {"youtu.be", "www.youtu.be"}:
        candidate = path.strip("/").split("/")[0]
        if re.fullmatch(r"[\w-]{11}", candidate):
            return candidate

    if "youtube.com" in host:
        if path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
            if re.fullmatch(r"[\w-]{11}", candidate):
                return candidate
        if path.startswith("/shorts/") or path.startswith("/embed/") or path.startswith("/live/"):
            candidate = path.strip("/").split("/")[1]
            if re.fullmatch(r"[\w-]{11}", candidate):
                return candidate

    fail(f"Could not parse a YouTube video id from: {value}")


def fetch_metadata(target: str) -> dict:
    with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(target, download=False)

    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "channel": info.get("channel"),
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "description": info.get("description"),
        "view_count": info.get("view_count"),
        "webpage_url": info.get("webpage_url"),
    }


def select_transcript(video_id: str, languages: list[str]):
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)

    try:
        return transcript_list.find_manually_created_transcript(languages), "manual"
    except NoTranscriptFound:
        return transcript_list.find_generated_transcript(languages), "auto-generated"


def fetch_transcript(video_id: str, languages: list[str]) -> tuple[list[dict], str]:
    try:
        transcript, transcript_type = select_transcript(video_id, languages)
    except TranscriptsDisabled:
        fail("Transcript extraction failed: transcripts are disabled for this video.", 3)
    except VideoUnavailable:
        fail("Transcript extraction failed: video is unavailable.", 3)
    except NoTranscriptFound:
        fail("Transcript extraction failed: no transcript was found for the requested languages.", 3)

    items = transcript.fetch()
    return [
        {
            "text": item.text.strip(),
            "start": round(item.start, 2),
            "duration": round(item.duration, 2),
        }
        for item in items
        if item.text.strip()
    ], transcript_type


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def print_metadata_plain(metadata: dict) -> None:
    ordered_keys = [
        "id",
        "title",
        "uploader",
        "channel",
        "upload_date",
        "duration",
        "view_count",
        "webpage_url",
    ]
    for key in ordered_keys:
        print(f"{key}: {metadata.get(key)}")


def print_transcript_plain(metadata: dict, transcript_items: list[dict], transcript_type: str) -> None:
    print(f"title: {metadata.get('title')}")
    print(f"uploader: {metadata.get('uploader')}")
    print(f"video_id: {metadata.get('id')}")
    print(f"transcript_type: {transcript_type}")
    print("")
    for item in transcript_items:
        print(f"{format_timestamp(item['start'])}\t{item['text']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract metadata and transcripts from a YouTube video (Grok port).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    metadata_parser = subparsers.add_parser("metadata")
    metadata_parser.add_argument("target")
    metadata_parser.add_argument("--json", action="store_true")

    transcript_parser = subparsers.add_parser("transcript")
    transcript_parser.add_argument("target")
    transcript_parser.add_argument("--json", action="store_true")
    transcript_parser.add_argument(
        "--languages",
        default="en",
        help="Comma-separated preferred languages, default: en",
    )

    args = parser.parse_args()
    video_id = parse_video_id(args.target)
    metadata = fetch_metadata(args.target)

    if args.command == "metadata":
        if args.json:
            print(json.dumps(metadata, ensure_ascii=True, indent=2))
        else:
            print_metadata_plain(metadata)
        return

    languages = [item.strip() for item in args.languages.split(",") if item.strip()]
    transcript_items, transcript_type = fetch_transcript(video_id, languages)

    if args.json:
        print(
            json.dumps(
                {
                    "metadata": metadata,
                    "transcript_type": transcript_type,
                    "transcript": transcript_items,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return

    print_transcript_plain(metadata, transcript_items, transcript_type)


if __name__ == "__main__":
    main()
