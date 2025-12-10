"""
GitHub Repository Backup Tool - Streamlit UI
Interactive web interface for backing up GitHub repositories
"""

import json
import os
from datetime import datetime

import streamlit as st

from github_backup import GitHubBackup, get_rate_limit_info

# Page configuration
st.set_page_config(
    page_title="GitHub Backup Tool",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling
st.markdown(
    """
    <style>
    /* Modern Minimalist Theme - Inspired by Card Design */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Main background */
    .main {
        background: #f9fafb;
        padding: 2rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Content container */
    .block-container {
        background: #ffffff;
        border-radius: 24px;
        padding: 2.5rem;
        max-width: 1200px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 30px rgba(0, 0, 0, 0.03);
    }

    /* Header styling */
    h1 {
        color: #000000;
        font-weight: 500;
        text-align: left;
        margin-bottom: 0.5rem;
        font-size: 2.5rem !important;
        letter-spacing: -0.8px;
        border-bottom: none;
        padding-bottom: 0.5rem;
    }

    h2 {
        color: #4b5563;
        font-weight: 500;
        border-bottom: none;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.5rem !important;
        letter-spacing: -0.5px;
    }

    h3 {
        color: #000000;
        font-weight: 500;
        font-size: 1.2rem !important;
        margin-top: 1rem;
        letter-spacing: -0.3px;
    }

    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: none;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.03);
    }

    .css-1d391kg .element-container, [data-testid="stSidebar"] .element-container {
        color: #000000;
    }

    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #000000;
        border-bottom: none;
        font-weight: 500;
    }

    /* Button styling - Rounded like card */
    .stButton>button {
        background: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #000000;
        border-radius: 9999px;
        padding: 0.625rem 1.5rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 200ms ease;
        width: 100%;
        text-transform: none;
        letter-spacing: normal;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    .stButton>button:hover {
        background: transparent !important;
        color: #000000 !important;
        border: 2px solid #000000;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stButton>button p {
        color: inherit !important;
    }

    /* Input fields - Rounded */
    .stTextInput>div>div>input {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.625rem 1rem;
        background: #ffffff;
        color: #000000;
        transition: all 200ms ease;
        font-size: 0.875rem;
    }

    .stTextInput>div>div>input:focus {
        border: 2px solid #000000;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
        outline: none;
    }

    /* Success/Error messages - Rounded with soft backgrounds */
    .stSuccess {
        background-color: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #000000;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .stError {
        background-color: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #000000;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Info boxes - Rounded */
    .stInfo {
        background-color: #f9fafb;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #000000;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Warning boxes - Rounded */
    .stWarning {
        background-color: #f9fafb;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem 1.5rem;
        color: #000000;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Metrics styling - Like card price */
    [data-testid="stMetricValue"] {
        color: #000000;
        font-weight: 300;
        font-size: 3rem !important;
        letter-spacing: -1.5px;
    }

    [data-testid="stMetricLabel"] {
        color: #6b7280;
        font-size: 0.875rem;
        text-transform: none;
        letter-spacing: normal;
        font-weight: 500;
    }

    /* Card styling - Rounded white cards */
    .repo-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        border: 1px solid #e5e7eb;
        transition: all 200ms ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .repo-card:hover {
        background: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
        border-color: #d1d5db;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: #000000;
        border-radius: 9999px;
    }

    /* Expander - Rounded */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        font-weight: 500;
        color: #000000;
        padding: 0.75rem 1rem;
        transition: all 200ms ease;
    }

    .streamlit-expanderHeader:hover {
        background-color: #f9fafb;
        border-color: #d1d5db;
    }

    /* Download button - Rounded like card */
    .stDownloadButton>button {
        background: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #000000;
        border-radius: 9999px;
        padding: 0.625rem 1.5rem;
        font-weight: 500;
        text-transform: none;
        letter-spacing: normal;
        transition: all 200ms ease;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    .stDownloadButton>button:hover {
        background: transparent !important;
        color: #000000 !important;
        border: 2px solid #000000;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stDownloadButton>button p {
        color: inherit !important;
    }

    /* Tabs - Rounded */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: none;
        background: #f9fafb;
        padding: 0.5rem;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #6b7280;
        border: none;
        padding: 0.625rem 1.5rem;
        font-weight: 500;
        text-transform: none;
        letter-spacing: normal;
        font-size: 0.875rem;
        border-radius: 8px;
        transition: all 200ms ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .stTabs [aria-selected="true"] p {
        color: #ffffff !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #6b7280;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
        font-size: 0.875rem;
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 2rem 0;
    }

    /* Links */
    a {
        color: #000000;
        text-decoration: none;
        font-weight: 500;
        transition: all 200ms ease;
    }

    a:hover {
        color: #4b5563;
        text-decoration: underline;
    }

    /* Code blocks - Rounded */
    code {
        background-color: #f9fafb;
        color: #000000;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 0.2rem 0.5rem;
        font-size: 0.875rem;
    }

    /* General text - exclude buttons and tabs */
    .element-container p:not(.stButton p):not(.stDownloadButton p):not(.stTabs p),
    .element-container span,
    .element-container div {
        color: #000000;
    }

    /* Force button text color */
    .stButton button,
    .stButton button *,
    .stButton button p,
    .stButton button span {
        color: #ffffff !important;
    }

    .stButton button:hover,
    .stButton button:hover *,
    .stButton button:hover p,
    .stButton button:hover span {
        color: #000000 !important;
    }

    /* Force download button text color */
    .stDownloadButton button,
    .stDownloadButton button *,
    .stDownloadButton button p,
    .stDownloadButton button span {
        color: #ffffff !important;
    }

    .stDownloadButton button:hover,
    .stDownloadButton button:hover *,
    .stDownloadButton button:hover p,
    .stDownloadButton button:hover span {
        color: #000000 !important;
    }

    /* Force active tab text color */
    .stTabs [aria-selected="true"],
    .stTabs [aria-selected="true"] *,
    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {
        color: #ffffff !important;
    }

    /* Inactive tab text color */
    .stTabs [aria-selected="false"],
    .stTabs [aria-selected="false"] *,
    .stTabs [aria-selected="false"] p,
    .stTabs [aria-selected="false"] span {
        color: #6b7280 !important;
    }

    /* Smaller secondary text */
    .text-sm {
        font-size: 0.875rem;
        color: #6b7280;
    }

    /* Remove colorful backgrounds */
    .element-container {
        background: transparent;
    }

    /* Metric container styling */
    [data-testid="metric-container"] {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def display_header():
    """Display the application header"""
    st.markdown("# GitHub Repository Backup Tool")
    st.markdown(
        "<p style='text-align: left; color: #6b7280; font-size: 0.875rem; margin-top: 0.5rem; font-weight: 400;'>"
        "Backup and archive your GitHub repositories with detailed metadata"
        "</p>",
        unsafe_allow_html=True,
    )


def display_rate_limit(token=None):
    """Display GitHub API rate limit information"""
    rate_info = get_rate_limit_info(token)

    if "error" not in rate_info:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rate Limit", rate_info.get("limit", "N/A"))
        with col2:
            st.metric("Remaining", rate_info.get("remaining", "N/A"))
        with col3:
            st.metric("Resets At", rate_info.get("reset", "N/A"))
    else:
        st.warning("⚠️ Unable to fetch rate limit information")


def display_repo_list(repos):
    """Display repository list in an organized manner"""
    st.markdown("## Repository List")

    # Summary statistics
    total_stars = sum(r["stars"] for r in repos)
    total_forks = sum(r["forks"] for r in repos)
    languages = [r["language"] for r in repos if r["language"]]
    unique_languages = len(set(languages))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Repos", len(repos))
    with col2:
        st.metric("Total Stars", total_stars)
    with col3:
        st.metric("Total Forks", total_forks)
    with col4:
        st.metric("Languages", unique_languages)

    st.markdown("---")

    # Search and filter
    search_term = st.text_input("Search repositories", "")

    # Filter repos
    filtered_repos = repos
    if search_term:
        filtered_repos = [
            r
            for r in repos
            if search_term.lower() in r["name"].lower()
            or (r["description"] and search_term.lower() in r["description"].lower())
        ]

    st.markdown(
        f"<p style='color: #6b7280; font-size: 0.875rem; margin: 1rem 0;'>Showing {len(filtered_repos)} repositories</p>",
        unsafe_allow_html=True,
    )

    # Display repos
    for repo in filtered_repos[:20]:  # Limit to 20 for performance
        with st.expander(f"{repo['name']}"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"<span style='color: #6b7280; font-size: 0.875rem;'>{repo['description'] or 'No description'}</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<a href='{repo['url']}' style='color: #000000; font-size: 0.875rem; font-weight: 500;'>{repo['url']}</a>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<span style='color: #6b7280; font-size: 0.875rem;'>Language: {repo['language'] or 'Not specified'}</span>",
                    unsafe_allow_html=True,
                )
                if repo["topics"]:
                    topics = ", ".join(repo["topics"])
                    st.markdown(
                        f"<span style='color: #6b7280; font-size: 0.875rem;'>Topics: {topics}</span>",
                        unsafe_allow_html=True,
                    )

            with col2:
                st.metric("Stars", repo["stars"])
                st.metric("Forks", repo["forks"])
                st.metric("Issues", repo["open_issues"])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"<span style='color: #6b7280; font-size: 0.75rem;'>Created: {repo['created_at'][:10]}</span>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f"<span style='color: #6b7280; font-size: 0.75rem;'>Updated: {repo['updated_at'][:10]}</span>",
                    unsafe_allow_html=True,
                )
            with col3:
                status = "Private" if repo["private"] else "Public"
                st.markdown(
                    f"<span style='color: #6b7280; font-size: 0.75rem;'>{status}</span>",
                    unsafe_allow_html=True,
                )

    if len(filtered_repos) > 20:
        st.info(f"Showing first 20 of {len(filtered_repos)} repositories")


def main():
    """Main application function"""
    display_header()

    # Sidebar
    with st.sidebar:
        st.markdown("## Configuration")

        st.markdown(
            "<p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem;'>GitHub Username</p>",
            unsafe_allow_html=True,
        )
        username = st.text_input(
            "GitHub Username *",
            placeholder="Enter username",
            help="The GitHub username to backup repositories from",
            label_visibility="collapsed",
        )

        st.markdown(
            "<p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; margin-top: 1rem;'>GitHub Token (Optional)</p>",
            unsafe_allow_html=True,
        )
        token = st.text_input(
            "GitHub Token (Optional)",
            type="password",
            placeholder="ghp_xxxxxxxxxxxx",
            help="Personal access token for higher rate limits and private repos",
            label_visibility="collapsed",
        )

        st.markdown(
            "<p style='color: #6b7280; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; margin-top: 1rem;'>Output Directory</p>",
            unsafe_allow_html=True,
        )
        output_dir = st.text_input(
            "Output Directory",
            value="backups",
            help="Directory where backups will be saved",
            label_visibility="collapsed",
        )

        if token:
            st.markdown("### API Rate Limit")
            display_rate_limit(token)

        st.markdown("### Information")
        st.info(
            "• Use a token for higher rate limits\n"
            "• Tokens are required for private repos\n"
            "• Create tokens at: github.com/settings/tokens"
        )

    # Main content area
    if not username:
        st.info("Enter a GitHub username in the sidebar to get started")

        # Display instructions
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("## How to Use")
            st.markdown(
                """
                1. **Enter Username**: Provide the GitHub username in the sidebar
                2. **Add Token** (Optional): Add a personal access token for better access
                3. **Start Backup**: Click the backup button to fetch repositories
                4. **Download**: Get your backup as a JSON file or ZIP archive
                """
            )

        with col2:
            st.markdown("## Features")
            st.markdown(
                """
                - Fetch all user repositories
                - Save as formatted JSON
                - Create compressed ZIP archives
                - View detailed statistics
                - Search and filter repos
                - Real-time API rate limit tracking
                """
            )

    else:
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Backup", "Statistics", "About"])

        with tab1:
            st.markdown("## Create Backup")

            backup_button = st.button("Start Backup", use_container_width=True)

            if backup_button:
                try:
                    with st.spinner(f"Fetching repositories for {username}..."):
                        backup = GitHubBackup(username, token or None)
                        result = backup.create_backup(output_dir)

                    if result["success"]:
                        st.success("Backup completed successfully")

                        # Display statistics
                        stats = result["stats"]
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Total Repos", stats["total_repos"])
                        with col2:
                            st.metric("Public", stats["public_repos"])
                        with col3:
                            st.metric("Private", stats["private_repos"])
                        with col4:
                            st.metric("Total Stars", stats["total_stars"])

                        st.markdown("---")

                        # Display file paths
                        st.markdown("### Backup Files")
                        st.markdown(
                            f"<div style='background: #f9fafb; padding: 1rem; border-radius: 12px; border: 1px solid #e5e7eb; margin: 0.5rem 0;'><code style='color: #000000; font-size: 0.875rem;'>JSON: {result['json_path']}</code></div>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"<div style='background: #f9fafb; padding: 1rem; border-radius: 12px; border: 1px solid #e5e7eb; margin: 0.5rem 0;'><code style='color: #000000; font-size: 0.875rem;'>Archive: {result['archive_path']}</code></div>",
                            unsafe_allow_html=True,
                        )

                        # Download buttons
                        col1, col2 = st.columns(2)

                        with col1:
                            if os.path.exists(result["json_path"]):
                                with open(
                                    result["json_path"], "r", encoding="utf-8"
                                ) as f:
                                    json_data = f.read()
                                st.download_button(
                                    label="Download JSON",
                                    data=json_data,
                                    file_name=f"{username}_repos.json",
                                    mime="application/json",
                                    use_container_width=True,
                                )

                        with col2:
                            if os.path.exists(result["archive_path"]):
                                with open(result["archive_path"], "rb") as f:
                                    zip_data = f.read()
                                st.download_button(
                                    label="Download ZIP",
                                    data=zip_data,
                                    file_name=f"{username}_backup.zip",
                                    mime="application/zip",
                                    use_container_width=True,
                                )

                        # Load and display repos
                        with open(result["json_path"], "r", encoding="utf-8") as f:
                            repos = json.load(f)

                        st.session_state["repos"] = repos
                        st.session_state["stats"] = stats

                        st.markdown("---")
                        display_repo_list(repos)

                    else:
                        st.error(f"Backup failed: {result['error']}")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

            # Display previously loaded repos if available
            elif "repos" in st.session_state:
                display_repo_list(st.session_state["repos"])

        with tab2:
            st.markdown("## Statistics")

            if "stats" in st.session_state:
                stats = st.session_state["stats"]

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### Repository Metrics")
                    st.metric("Total Repositories", stats["total_repos"])
                    st.metric("Public Repositories", stats["public_repos"])
                    st.metric("Private Repositories", stats["private_repos"])

                with col2:
                    st.markdown("### Engagement Metrics")
                    st.metric("Total Stars", stats["total_stars"])
                    st.metric("Total Forks", stats["total_forks"])
                    st.metric("Backup Date", stats["backup_date"][:10])

                if "repos" in st.session_state:
                    repos = st.session_state["repos"]

                    st.markdown("---")
                    st.markdown("### Top Repositories")

                    # Top starred repos
                    top_starred = sorted(repos, key=lambda x: x["stars"], reverse=True)[
                        :5
                    ]

                    for i, repo in enumerate(top_starred, 1):
                        st.markdown(
                            f"<p style='color: #000000; font-size: 0.875rem; margin: 0.5rem 0;'>{i}. <strong>{repo['name']}</strong> <span style='color: #6b7280;'>— {repo['stars']} stars</span></p>",
                            unsafe_allow_html=True,
                        )

            else:
                st.info("Run a backup first to see statistics")

        with tab3:
            st.markdown("## About This Tool")

            st.markdown(
                """
                ### GitHub Repository Backup Tool

                This tool helps you create comprehensive backups of GitHub repositories,
                including all metadata and statistics.

                **Key Features:**
                - Fetch repository data via GitHub API
                - Save data as formatted JSON
                - Create compressed ZIP archives
                - Interactive data visualization
                - Search and filter capabilities
                - API rate limit monitoring

                **Technologies Used:**
                - Python 3.x
                - Streamlit (UI Framework)
                - Requests (HTTP Library)
                - Built-in modules: json, os, shutil

                **Created by:** Your Dev Journey
                **Version:** 1.0.0
                """
            )

            st.markdown("---")
            st.markdown(
                """
                ### Security & Privacy

                - Tokens are never stored permanently
                - All data is processed locally
                - No external servers involved
                - Your data remains on your machine
                """
            )

    # Footer
    st.markdown(
        """
        <div class='footer'>
            <p>GitHub Backup Tool · Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
