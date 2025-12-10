"""
GitHub Repository Backup Tool
Fetches repository data from GitHub API and creates backups
"""

import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import requests


class GitHubBackup:
    """Main class for GitHub repository backup operations"""

    def __init__(self, username, token=None):
        """
        Initialize GitHub Backup

        Args:
            username (str): GitHub username
            token (str, optional): GitHub personal access token for authentication
        """
        self.username = username
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}

        if token:
            self.headers["Authorization"] = f"token {token}"

    def fetch_repositories(self):
        """
        Fetch all repositories for the user

        Returns:
            list: List of repository dictionaries

        Raises:
            requests.RequestException: If API request fails
        """
        try:
            repos = []
            page = 1
            per_page = 100

            while True:
                url = f"{self.base_url}/users/{self.username}/repos"
                params = {
                    "per_page": per_page,
                    "page": page,
                    "type": "all",
                    "sort": "updated",
                }

                response = requests.get(
                    url, headers=self.headers, params=params, timeout=30
                )

                if response.status_code == 404:
                    raise ValueError(f"User '{self.username}' not found")
                elif response.status_code == 403:
                    raise ValueError(
                        "API rate limit exceeded. Please use a GitHub token."
                    )
                elif response.status_code != 200:
                    raise requests.RequestException(
                        f"API request failed with status {response.status_code}"
                    )

                page_repos = response.json()

                if not page_repos:
                    break

                repos.extend(page_repos)
                page += 1

                # Check if we've reached the last page
                if len(page_repos) < per_page:
                    break

                # Be nice to GitHub API
                time.sleep(0.5)

            return repos

        except requests.Timeout:
            raise requests.RequestException("Request timed out. Please try again.")
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch repositories: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def process_repo_data(self, repos):
        """
        Process and simplify repository data

        Args:
            repos (list): Raw repository data from API

        Returns:
            list: Processed repository data
        """
        processed_repos = []

        for repo in repos:
            processed_repo = {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "url": repo.get("html_url"),
                "clone_url": repo.get("clone_url"),
                "ssh_url": repo.get("ssh_url"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "open_issues": repo.get("open_issues_count", 0),
                "private": repo.get("private", False),
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "size": repo.get("size", 0),
                "default_branch": repo.get("default_branch"),
                "topics": repo.get("topics", []),
                "archived": repo.get("archived", False),
                "disabled": repo.get("disabled", False),
            }
            processed_repos.append(processed_repo)

        return processed_repos

    def save_to_json(self, data, output_dir, filename=None):
        """
        Save repository data to JSON file

        Args:
            data (list): Repository data to save
            output_dir (str): Directory to save the file
            filename (str, optional): Custom filename

        Returns:
            str: Path to saved JSON file
        """
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Generate filename with timestamp
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.username}_repos_{timestamp}.json"

            filepath = os.path.join(output_dir, filename)

            # Save to JSON with pretty formatting
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return filepath

        except IOError as e:
            raise IOError(f"Failed to save JSON file: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while saving: {str(e)}")

    def create_archive(self, source_dir, output_dir, archive_name=None):
        """
        Create a compressed archive of the backup

        Args:
            source_dir (str): Directory to archive
            output_dir (str): Directory to save the archive
            archive_name (str, optional): Custom archive name

        Returns:
            str: Path to created archive
        """
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Generate archive name with timestamp
            if not archive_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"{self.username}_backup_{timestamp}"

            # Remove extension if provided (shutil.make_archive adds it)
            archive_name = archive_name.replace(".zip", "")

            archive_path = os.path.join(output_dir, archive_name)

            # Create zip archive
            archive_file = shutil.make_archive(archive_path, "zip", source_dir)

            return archive_file

        except Exception as e:
            raise Exception(f"Failed to create archive: {str(e)}")

    def create_backup(self, output_dir="backups"):
        """
        Complete backup operation: fetch, save, and archive

        Args:
            output_dir (str): Base directory for backups

        Returns:
            dict: Backup summary with paths and statistics
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(output_dir, f"backup_{timestamp}")

            # Fetch repositories
            repos = self.fetch_repositories()

            if not repos:
                raise ValueError("No repositories found")

            # Process repository data
            processed_repos = self.process_repo_data(repos)

            # Save to JSON
            json_path = self.save_to_json(processed_repos, backup_dir)

            # Create metadata file
            metadata = {
                "username": self.username,
                "backup_date": datetime.now().isoformat(),
                "total_repos": len(processed_repos),
                "public_repos": sum(1 for r in processed_repos if not r["private"]),
                "private_repos": sum(1 for r in processed_repos if r["private"]),
                "total_stars": sum(r["stars"] for r in processed_repos),
                "total_forks": sum(r["forks"] for r in processed_repos),
            }

            metadata_path = os.path.join(backup_dir, "metadata.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            # Create archive
            archive_path = self.create_archive(backup_dir, output_dir)

            # Clean up temporary directory (optional)
            # shutil.rmtree(backup_dir)

            return {
                "success": True,
                "json_path": json_path,
                "metadata_path": metadata_path,
                "archive_path": archive_path,
                "backup_dir": backup_dir,
                "stats": metadata,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}


def get_rate_limit_info(token=None):
    """
    Get GitHub API rate limit information

    Args:
        token (str, optional): GitHub personal access token

    Returns:
        dict: Rate limit information
    """
    try:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"

        response = requests.get(
            "https://api.github.com/rate_limit", headers=headers, timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            core = data.get("rate", {})
            return {
                "limit": core.get("limit"),
                "remaining": core.get("remaining"),
                "reset": datetime.fromtimestamp(core.get("reset", 0)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
    except Exception as e:
        return {"error": str(e)}

    return {"error": "Failed to fetch rate limit"}


if __name__ == "__main__":
    # Example usage
    print("GitHub Repository Backup Tool")
    print("-" * 50)

    username = input("Enter GitHub username: ").strip()
    token = (
        input("Enter GitHub token (optional, press Enter to skip): ").strip() or None
    )

    try:
        backup = GitHubBackup(username, token)
        print(f"\nFetching repositories for {username}...")

        result = backup.create_backup()

        if result["success"]:
            print("\n✓ Backup completed successfully!")
            print(f"  Total repositories: {result['stats']['total_repos']}")
            print(f"  Public: {result['stats']['public_repos']}")
            print(f"  Private: {result['stats']['private_repos']}")
            print(f"  Total stars: {result['stats']['total_stars']}")
            print(f"\n  JSON file: {result['json_path']}")
            print(f"  Archive: {result['archive_path']}")
        else:
            print(f"\n✗ Backup failed: {result['error']}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
