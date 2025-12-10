"""
Example Usage Script for GitHub Repository Backup Tool
This script demonstrates how to use the github_backup module programmatically
"""

import json
import os

from github_backup import GitHubBackup, get_rate_limit_info


def example_basic_backup():
    """Example 1: Basic backup without token"""
    print("=" * 60)
    print("Example 1: Basic Backup (Public Repositories Only)")
    print("=" * 60)

    username = "octocat"  # Replace with actual username

    try:
        backup = GitHubBackup(username)
        print(f"\nFetching repositories for {username}...")

        result = backup.create_backup()

        if result["success"]:
            print("\n✓ Backup completed successfully!")
            print(f"  Total repositories: {result['stats']['total_repos']}")
            print(f"  Public: {result['stats']['public_repos']}")
            print(f"  Total stars: {result['stats']['total_stars']}")
            print(f"\n  JSON file: {result['json_path']}")
            print(f"  Archive: {result['archive_path']}")
        else:
            print(f"\n✗ Backup failed: {result['error']}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_backup_with_token():
    """Example 2: Backup with authentication token"""
    print("\n" + "=" * 60)
    print("Example 2: Backup with Token (Including Private Repos)")
    print("=" * 60)

    username = "your-username"  # Replace with your username
    token = "ghp_yourtoken"  # Replace with your token

    # Check rate limit before starting
    print("\nChecking API rate limit...")
    rate_info = get_rate_limit_info(token)

    if "error" not in rate_info:
        print(f"  Rate limit: {rate_info['limit']}")
        print(f"  Remaining: {rate_info['remaining']}")
        print(f"  Resets at: {rate_info['reset']}")

    try:
        backup = GitHubBackup(username, token)
        result = backup.create_backup(output_dir="my_backups")

        if result["success"]:
            print("\n✓ Backup completed successfully!")
            stats = result["stats"]
            print(f"  Total: {stats['total_repos']} repos")
            print(f"  Public: {stats['public_repos']}")
            print(f"  Private: {stats['private_repos']}")
        else:
            print(f"\n✗ Backup failed: {result['error']}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_fetch_and_process():
    """Example 3: Fetch repositories and process data manually"""
    print("\n" + "=" * 60)
    print("Example 3: Manual Repository Processing")
    print("=" * 60)

    username = "octocat"

    try:
        backup = GitHubBackup(username)

        # Fetch repositories
        print(f"\nFetching repositories for {username}...")
        repos = backup.fetch_repositories()
        print(f"Found {len(repos)} repositories")

        # Process the data
        processed = backup.process_repo_data(repos)

        # Display top 5 most starred repositories
        print("\n🏆 Top 5 Most Starred Repositories:")
        sorted_repos = sorted(processed, key=lambda x: x["stars"], reverse=True)

        for i, repo in enumerate(sorted_repos[:5], 1):
            print(f"\n{i}. {repo['name']}")
            print(f"   ⭐ Stars: {repo['stars']}")
            print(f"   🍴 Forks: {repo['forks']}")
            print(f"   📝 Language: {repo['language'] or 'N/A'}")
            print(f"   🔗 URL: {repo['url']}")

        # Save to custom location
        json_path = backup.save_to_json(
            processed, "custom_backups", f"{username}_custom.json"
        )
        print(f"\n✓ Data saved to: {json_path}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_analyze_repositories():
    """Example 4: Analyze repository data from backup"""
    print("\n" + "=" * 60)
    print("Example 4: Analyze Repository Statistics")
    print("=" * 60)

    # Assume we have a backup JSON file
    json_file = "backups/backup_latest/octocat_repos.json"

    if not os.path.exists(json_file):
        print(f"\n⚠️ File not found: {json_file}")
        print("Run a backup first to create this file.")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            repos = json.load(f)

        # Calculate statistics
        total_repos = len(repos)
        total_stars = sum(r["stars"] for r in repos)
        total_forks = sum(r["forks"] for r in repos)

        # Language distribution
        languages = [r["language"] for r in repos if r["language"]]
        language_count = {}
        for lang in languages:
            language_count[lang] = language_count.get(lang, 0) + 1

        # Sort by count
        sorted_languages = sorted(
            language_count.items(), key=lambda x: x[1], reverse=True
        )

        print(f"\n📊 Repository Statistics")
        print(f"  Total repositories: {total_repos}")
        print(f"  Total stars: {total_stars}")
        print(f"  Total forks: {total_forks}")
        print(f"  Avg stars per repo: {total_stars / total_repos:.2f}")

        print(f"\n💻 Top Languages:")
        for lang, count in sorted_languages[:5]:
            percentage = (count / len(languages)) * 100
            print(f"  {lang}: {count} repos ({percentage:.1f}%)")

        # Find repositories with most issues
        print(f"\n🐛 Repositories with Most Open Issues:")
        sorted_by_issues = sorted(repos, key=lambda x: x["open_issues"], reverse=True)

        for repo in sorted_by_issues[:3]:
            print(f"  {repo['name']}: {repo['open_issues']} issues")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def example_custom_filtering():
    """Example 5: Filter repositories by criteria"""
    print("\n" + "=" * 60)
    print("Example 5: Custom Repository Filtering")
    print("=" * 60)

    username = "octocat"

    try:
        backup = GitHubBackup(username)
        repos = backup.fetch_repositories()
        processed = backup.process_repo_data(repos)

        # Filter: Python repos with more than 10 stars
        python_repos = [
            r for r in processed if r["language"] == "Python" and r["stars"] > 10
        ]

        print(f"\n🐍 Python repositories with 10+ stars: {len(python_repos)}")
        for repo in python_repos[:5]:
            print(f"  - {repo['name']} (⭐ {repo['stars']})")

        # Filter: Recently updated repos (not archived)
        active_repos = [r for r in processed if not r["archived"] and not r["disabled"]]

        print(f"\n✅ Active repositories: {len(active_repos)}")

        # Filter: Repos with topics
        repos_with_topics = [r for r in processed if r["topics"]]

        print(f"\n🏷️ Repositories with topics: {len(repos_with_topics)}")

        # Get all unique topics
        all_topics = set()
        for repo in repos_with_topics:
            all_topics.update(repo["topics"])

        print(f"  Unique topics: {len(all_topics)}")
        print(f"  Sample topics: {', '.join(list(all_topics)[:10])}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  GitHub Repository Backup Tool - Example Usage Script  ║")
    print("╚" + "=" * 58 + "╝")

    # Run examples (comment out the ones you don't want to run)
    example_basic_backup()

    # Uncomment to run other examples:
    # example_backup_with_token()
    # example_fetch_and_process()
    # example_analyze_repositories()
    # example_custom_filtering()

    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\n💡 Tips:")
    print("  - Replace 'octocat' with your GitHub username")
    print("  - Add your token for private repos and higher limits")
    print("  - Check the 'backups' folder for output files")
    print("\n")


if __name__ == "__main__":
    main()
