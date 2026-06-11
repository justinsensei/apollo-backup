#!/usr/bin/env python3
import os
import sys
import datetime
import subprocess
import json
import re

# --- Constants ---
VAULT_PATH = "/home/justin.guest/vault"
SOURCES_DIR = os.path.join(VAULT_PATH, "Notes", "Sources")
READINGS_DIR = os.path.join(VAULT_PATH, "Inputs", "Readings")

def get_hermes_cli_path():
    """Find the hermes-agent CLI executable."""
    # This is a simple heuristic. A more robust solution might check the PATH.
    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin", "hermes-agent")
    if os.path.exists(local_bin):
        return local_bin
    # Fallback to assuming it's in the standard PATH
    return "hermes-agent"

def generate_summary(text_content):
    """
    Uses a subagent to generate a summary of the given text.
    """
    goal = (
        "You are an expert in synthesizing complex information into concise, insightful summaries. "
        "Read the following text and extract the key points, most interesting arguments, and "
        "most useful insights. The output should be a well-structured summary formatted in Markdown, "
        "suitable for use as a 'reading note' in a personal knowledge management system. "
        "Do not include any preamble, introduction, or concluding remarks. "
        "Output ONLY the summary itself."
    )
    
    hermes_cli = get_hermes_cli_path()

    try:
        # Using the CLI to delegate is more stable than direct imports
        process = subprocess.run(
            [hermes_cli, "delegate-task", "--goal", goal, "--context", text_content, "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=300 
        )
        # The result is a JSON string on a single line, get the last non-empty line
        lines = process.stdout.strip().splitlines()
        if not lines:
            raise ValueError("Subagent returned no output.")
            
        last_line = lines[-1]
        result = json.loads(last_line)
        
        # The actual output is nested
        if "result" in result and "summary" in result["result"]:
             summary = result["result"]["summary"].strip()
             if "No summary available" in summary:
                 raise ValueError("Subagent failed to produce a valid summary.")
             return summary
        else:
            raise KeyError("The key 'summary' was not found in the subagent's JSON response.")

    except FileNotFoundError:
        print(f"Error: The command '{hermes_cli}' was not found.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Subagent process failed with exit code {e.returncode}.", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error: Could not parse summary from subagent output. Details: {e}", file=sys.stderr)
        sys.exit(1)


def create_source_note(reading_path):
    """
    Creates a new Source note from a given Reading note.
    """
    if not os.path.exists(reading_path):
        print(f"Error: Reading file not found at '{reading_path}'", file=sys.stderr)
        return

    try:
        with open(reading_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return

    summary = generate_summary(content)

    # --- Prepare metadata ---
    reading_filename = os.path.basename(reading_path)
    title, _ = os.path.splitext(reading_filename)
    
    # Sanitize title for filename
    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", title)

    now = datetime.datetime.now()
    note_id = now.strftime('%Y%m%d%H%M%S')
    daily_note_str = now.strftime('%Y-%m-%d %A')
    
    # Create a vault-relative path for the wikilink
    reading_relpath = os.path.relpath(reading_path, VAULT_PATH)
    # Ensure forward slashes for wikilinks, even on Windows
    reading_wikilink = reading_relpath.replace(os.sep, '/')


    # --- Assemble the new note ---
    frontmatter = f"""---
id: '{note_id}'
daily_note: "[[{daily_note_str}]]"
category: "[[Sources]]"
reading: "[[{reading_wikilink}]]"
---
"""

    new_note_content = f"{frontmatter}\n# {title}\n\n{summary}\n"
    
    # Per convention: Title ID.md
    new_filename = f"{sanitized_title} {note_id}.md"
    new_filepath = os.path.join(SOURCES_DIR, new_filename)

    try:
        os.makedirs(SOURCES_DIR, exist_ok=True)
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(new_note_content)
        
        print(new_filepath) # Return the path of the new file

    except Exception as e:
        print(f"Error writing new source note: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./create_source_note.py <path_to_reading_note>", file=sys.stderr)
        sys.exit(1)
    
    create_source_note(sys.argv[1])
