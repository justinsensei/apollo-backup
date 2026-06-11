#!/usr/bin/env python3
import os
import sys
import datetime
import subprocess
import json
import re

# --- Constants ---
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "/home/justin.guest/vault")

def get_hermes_cli_path():
    """Find the hermes-agent CLI executable."""
    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin", "hermes-agent")
    if os.path.exists(local_bin):
        return local_bin
    return "hermes-agent"

def generate_summary(text_content):
    """
    Uses the `hermes-agent prompt` command to generate a summary.
    """
    system_prompt = (
        "You are an expert in synthesizing complex information into concise, insightful summaries. "
        "Read the following text and extract the key points, most interesting arguments, and "
        "most useful insights. The output should be a well-structured summary formatted in Markdown, "
        "suitable for use as a 'reading note' in a personal knowledge management system. "
        "Do not include any preamble, introduction, or concluding remarks. "
        "Output ONLY the summary itself."
    )
    
    hermes_cli = get_hermes_cli_path()

    try:
        process = subprocess.run(
            [hermes_cli, "prompt", "--model", "gemini/gemini-2.5-pro", "--system", system_prompt, text_content],
            capture_output=True,
            text=True,
            check=True,
            timeout=300 
        )
        
        summary = process.stdout.strip()
        if not summary:
            raise ValueError("LLM returned an empty summary.")
        return summary

    except Exception as e:
        print(f"Error during summary generation: {e}", file=sys.stderr)
        sys.exit(1)

def main(reading_path):
    """
    Generates the full content for a new Source note.
    """
    if not os.path.exists(reading_path):
        print(f"Error: Reading file not found at '{reading_path}'", file=sys.stderr)
        sys.exit(1)

    with open(reading_path, 'r', encoding='utf-8') as f:
        content = f.read()

    summary = generate_summary(content)

    reading_filename = os.path.basename(reading_path)
    title, _ = os.path.splitext(reading_filename)
    
    now = datetime.datetime.now()
    note_id = now.strftime('%Y%m%d%H%M%S')
    daily_note_str = now.strftime('%Y-%m-%d %A')
    
    reading_relpath = os.path.relpath(reading_path, VAULT_PATH)
    reading_wikilink = reading_relpath.replace(os.sep, '/')

    frontmatter = f"""---
id: '{note_id}'
daily_note: "[[{daily_note_str}]]"
category: "[[Sources]]"
reading: "[[{reading_wikilink}]]"
---
"""
    new_note_content = f"{frontmatter}\n# {title}\n\n{summary}\n"
    print(new_note_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./generate_source_content.py <path_to_reading_note>", file=sys.stderr)
        sys.exit(1)
    
    main(sys.argv[1])
