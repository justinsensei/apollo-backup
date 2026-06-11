#!/usr/bin/env python3
import os
import sys
import json
import argparse
import urllib.request
import urllib.error

CACHE_FILE = os.path.expanduser("~/.hermes/processed_linear_brains.json")
API_URL = "https://api.linear.app/graphql"

def load_processed():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_processed(processed):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(processed, f, indent=2)

def run_query(query, variables=None):
    api_key = os.environ.get("LINEAR_API_KEY")
    if not api_key:
        # Try loading from ~/.hermes/.env
        env_path = os.path.expanduser("~/.hermes/.env")
        if os.path.isfile(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("LINEAR_API_KEY=") and "=" in line:
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        os.environ["LINEAR_API_KEY"] = api_key
                        break
    if not api_key:
        sys.stderr.write("Error: LINEAR_API_KEY not set\n")
        sys.exit(3)

    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": api_key,
            "User-Agent": "hermes-agent-linear-brain/1.0"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}\n")
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.stderr.write(f"Network error: {e}\n")
        sys.exit(1)

def get_viewer_id():
    query = "query { viewer { id name email } }"
    res = run_query(query)
    viewer = res.get("data", {}).get("viewer")
    if not viewer:
        sys.stderr.write(f"Error getting viewer ID: {res.get('errors')}\n")
        sys.exit(1)
    return viewer["id"], viewer["name"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mark-processed", help="Mark a comment or update ID as processed")
    args = parser.parse_args()

    if args.mark_processed:
        processed = load_processed()
        if args.mark_processed not in processed:
            processed.append(args.mark_processed)
            save_processed(processed)
            print(json.dumps({"ok": True, "marked": args.mark_processed}))
        else:
            print(json.dumps({"ok": True, "already_processed": args.mark_processed}))
        sys.exit(0)

    # Load cache and get viewer id
    processed = load_processed()
    processed_set = set(processed)
    viewer_id, viewer_name = get_viewer_id()

    # Define reaction filters for the query
    # Match emoji name "obsidian_jg" or customEmojiId "3edcb6ac-42df-4ef3-8bf4-c6a6b21c8124"
    emoji_filter = {
        "reactions": {
            "or": [
                {"emoji": {"eq": "obsidian_jg"}},
                {"customEmojiId": {"eq": "3edcb6ac-42df-4ef3-8bf4-c6a6b21c8124"}}
            ]
        }
    }

    # 1. Fetch Comments
    comments_query = """
    query($filter: CommentFilter) {
      comments(filter: $filter, first: 30, orderBy: updatedAt) {
        nodes {
          id
          body
          createdAt
          url
          user {
            id
            name
            email
          }
          issue {
            id
            identifier
            title
            description
            url
            state { name }
            project { id name description }
            comments(first: 20) {
              nodes {
                id
                body
                createdAt
                user { name }
              }
            }
          }
          project {
            id
            name
            description
            url
            comments(first: 20) {
              nodes {
                id
                body
                createdAt
                user { name }
              }
            }
          }
          projectUpdate {
            id
            body
            url
            project { id name description }
            comments(first: 20) {
              nodes {
                id
                body
                createdAt
                user { name }
              }
            }
          }
          initiative {
            id
            name
            description
            url
          }
          initiativeUpdate {
            id
            body
            url
            initiative { id name description }
            comments(first: 20) {
              nodes {
                id
                body
                createdAt
                user { name }
              }
            }
          }
          documentContent {
            id
            document {
              id
              title
              url
              project { id name }
            }
          }
          reactions {
            emoji
            user { id name }
          }
        }
      }
    }
    """

    res_comments = run_query(comments_query, {"filter": emoji_filter})
    comment_nodes = res_comments.get("data", {}).get("comments", {}).get("nodes", [])

    # 2. Fetch Project Updates
    p_updates_query = """
    query($filter: ProjectUpdateFilter) {
      projectUpdates(filter: $filter, first: 30, orderBy: updatedAt) {
        nodes {
          id
          body
          createdAt
          url
          user {
            id
            name
            email
          }
          project {
            id
            name
            description
            url
          }
          reactions {
            emoji
            user { id name }
          }
          comments(first: 20) {
            nodes {
              id
              body
              createdAt
              user { name }
            }
          }
        }
      }
    }
    """

    res_p_updates = run_query(p_updates_query, {"filter": emoji_filter})
    p_update_nodes = res_p_updates.get("data", {}).get("projectUpdates", {}).get("nodes", [])

    # 3. Fetch Initiative Updates
    i_updates_query = """
    query($filter: InitiativeUpdateFilter) {
      initiativeUpdates(filter: $filter, first: 30, orderBy: updatedAt) {
        nodes {
          id
          body
          createdAt
          url
          user {
            id
            name
            email
          }
          initiative {
            id
            name
            description
            url
          }
          reactions {
            emoji
            user { id name }
          }
          comments(first: 20) {
            nodes {
              id
              body
              createdAt
              user { name }
            }
          }
        }
      }
    }
    """

    res_i_updates = run_query(i_updates_query, {"filter": emoji_filter})
    i_update_nodes = res_i_updates.get("data", {}).get("initiativeUpdates", {}).get("nodes", [])

    # Filter and format results
    new_brains = []

    # Process Comments
    for node in comment_nodes:
        node_id = node["id"]
        if node_id in processed_set:
            continue
        
        # Verify Justin added the reaction
        has_justin_reaction = False
        for rxn in node.get("reactions", []):
            is_obsidian = rxn.get("emoji") == "obsidian_jg"
            is_justin = rxn.get("user", {}).get("id") == viewer_id
            if is_obsidian and is_justin:
                has_justin_reaction = True
                break
        
        if not has_justin_reaction:
            continue

        new_brains.append({
            "type": "Comment",
            "id": node_id,
            "body": node["body"],
            "createdAt": node["createdAt"],
            "url": node["url"],
            "author": node["user"]["name"] if node.get("user") else "Unknown",
            "reactions": node["reactions"],
            "context": {
                "issue": node.get("issue"),
                "project": node.get("project"),
                "projectUpdate": node.get("projectUpdate"),
                "initiative": node.get("initiative"),
                "initiativeUpdate": node.get("initiativeUpdate"),
                "documentContent": node.get("documentContent")
            }
        })

    # Process Project Updates
    for node in p_update_nodes:
        node_id = node["id"]
        if node_id in processed_set:
            continue
        
        # Verify Justin added the reaction
        has_justin_reaction = False
        for rxn in node.get("reactions", []):
            is_obsidian = rxn.get("emoji") == "obsidian_jg"
            is_justin = rxn.get("user", {}).get("id") == viewer_id
            if is_obsidian and is_justin:
                has_justin_reaction = True
                break
        
        if not has_justin_reaction:
            continue

        new_brains.append({
            "type": "ProjectUpdate",
            "id": node_id,
            "body": node["body"],
            "createdAt": node["createdAt"],
            "url": node["url"],
            "author": node["user"]["name"] if node.get("user") else "Unknown",
            "reactions": node["reactions"],
            "context": {
                "project": node.get("project"),
                "comments": node.get("comments", {}).get("nodes", [])
            }
        })

    # Process Initiative Updates
    for node in i_update_nodes:
        node_id = node["id"]
        if node_id in processed_set:
            continue
        
        # Verify Justin added the reaction
        has_justin_reaction = False
        for rxn in node.get("reactions", []):
            is_obsidian = rxn.get("emoji") == "obsidian_jg"
            is_justin = rxn.get("user", {}).get("id") == viewer_id
            if is_obsidian and is_justin:
                has_justin_reaction = True
                break
        
        if not has_justin_reaction:
            continue

        new_brains.append({
            "type": "InitiativeUpdate",
            "id": node_id,
            "body": node["body"],
            "createdAt": node["createdAt"],
            "url": node["url"],
            "author": node["user"]["name"] if node.get("user") else "Unknown",
            "reactions": node["reactions"],
            "context": {
                "initiative": node.get("initiative"),
                "comments": node.get("comments", {}).get("nodes", [])
            }
        })

    print(json.dumps(new_brains, indent=2))

if __name__ == "__main__":
    main()
