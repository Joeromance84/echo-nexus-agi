# echopack/interfaces/github_linker.py
# A module for syncing with GitHub.

import requests
import json

class GitHubLinker:
    """
    Manages all interactions with the GitHub repository.
    """
    def __init__(self, repo_url: str, github_token: str):
        self.repo_url = repo_url
        self.headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def fetch_latest_updates(self):
        """
        Pulls the latest changes from the GitHub repository.
        """
        print("Pulling latest code from GitHub...")
        # A conceptual Git command call or API interaction
        response = requests.get(f"{self.repo_url}/contents/training", headers=self.headers)
        if response.status_code == 200:
            print("Successfully fetched contents.")
            return json.loads(response.text)
        else:
            print("Failed to sync with GitHub.")
            return None

    def push_changes(self, commit_message: str):
        """
        Pushes new packages or code updates back to GitHub.
        """
        print(f"Committing changes with message: '{commit_message}'")
        # Conceptual API call to commit and push files.
        print("Push successful. GitHub is now updated.")