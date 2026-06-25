# Claude Tag Repository Access Limitation & Workaround

## Issue Summary
When setting up **Claude Tag** in Slack, administrators might try to grant access to a personal GitHub repository (e.g., `github.com/Username/Repo-Name`). However, Claude Tag's access bundles interface (available under `claude.ai/admin-settings/claude-in-slack`) only supports organization-level connections. It does not provide an option to connect or authenticate personal GitHub accounts.

Attempting to clone or interact with a personal repository via Claude Tag results in a **403 Forbidden** error:
> Claude doesn't have GitHub access to username/repo-name for your organization. An org admin can install the Claude GitHub App... or reconnect GitHub...

## Workaround: Transfer to Org Account
To resolve this limitation and grant Claude Tag access without setting up manual SSH key/token access:

1. **Transfer Repository Ownership:**
   - In GitHub, navigate to the personal repository's **Settings** tab.
   - Scroll down to the **Danger Zone** and select **Transfer ownership**.
   - Set the destination to your team's GitHub organization (e.g., `TeamSignLab`).
2. **Access Propagation:**
   - Since the team's Claude Tag access bundle is usually configured for "All repos" under that organization, the repository (now `TeamSignLab/Repo-Name`) will automatically become reachable by the agent with no further configuration.
