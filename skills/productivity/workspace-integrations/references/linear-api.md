# Linear GraphQL API Reference

Manage Linear issues, projects, and teams directly via the GraphQL API using `curl` or `scripts/linear_api.py`.

## Setup
1. Get a personal API key from **Linear Settings > Account > Security & access > Personal API keys**.
2. Set `LINEAR_API_KEY` in environment.

## Python Helper Script
`scripts/linear_api.py` provides CLI commands: `whoami`, `list-teams`, `list-projects`, `list-states`, `list-issues`, `get-issue`, `search-issues`, `create-issue`, `update-issue`, `update-status`, `add-comment`, `list-documents`, `get-document`, `search-documents`, `raw`.

## GraphQL API Endpoint
- **Endpoint:** `https://api.linear.app/graphql` (POST)
- **Header:** `Authorization: $LINEAR_API_KEY`
- **Content-Type:** `application/json`

### Workflow States & Priorities
- **States:** `triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled`.
- **Priorities:** 0 = None, 1 = Urgent, 2 = High, 3 = Medium, 4 = Low.

### Common Queries
```bash
# Get viewer
curl -s -X POST https://api.linear.app/graphql -H "Authorization: $LINEAR_API_KEY" -H "Content-Type: application/json" -d '{"query": "{ viewer { id name email } }"}' | jq .

# Search issues
curl -s -X POST https://api.linear.app/graphql -H "Authorization: $LINEAR_API_KEY" -H "Content-Type: application/json" -d '{"query": "{ issueSearch(query: \"bug login\", first: 10) { nodes { identifier title state { name } url } } }"}' | jq .
```
