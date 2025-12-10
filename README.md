# GitHub Repository Backup Tool

A modern, user-friendly Python application for backing up your GitHub repositories. Features both a beautiful Streamlit web interface and a powerful command-line tool for creating comprehensive backups of your GitHub repository metadata.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.39.0+-red.svg)

## ✨ Features

- 🌐 **Dual Interface**: Beautiful Streamlit web UI and robust CLI tool
- 🔒 **Secure Authentication**: Optional GitHub token support for private repositories
- 📊 **Comprehensive Data**: Captures repository metadata, statistics, and details
- 📦 **Auto-Archiving**: Creates timestamped ZIP archives of backups
- 🎨 **Modern UI**: Clean, minimalist design with real-time progress tracking
- 📈 **Statistics Dashboard**: View repository analytics and insights
- 🚀 **API Rate Limit Monitoring**: Built-in rate limit tracking
- 🔍 **Advanced Filtering**: Filter repositories by language, stars, and more
- 📝 **Detailed Metadata**: Captures stars, forks, languages, topics, and more

## 📋 Prerequisites

- Python 3.7 or higher
- GitHub account
- GitHub Personal Access Token (optional, for private repos and higher rate limits)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/github-backup-tool.git
   cd github-backup-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings** (optional)
   ```bash
   cp config.example.json config.json
   # Edit config.json with your preferences
   ```

## 🎯 Usage

### Web Interface (Streamlit)

Launch the interactive web application:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501` and:
1. Enter your GitHub username
2. (Optional) Add your personal access token
3. Click "Fetch Repositories"
4. Review and download your backup

### Command Line Interface

**Basic backup (public repositories only):**
```bash
python github_backup.py
```

**Programmatic usage:**
```python
from github_backup import GitHubBackup

# Initialize backup
backup = GitHubBackup(username="octocat", token="your_token_here")

# Create complete backup
result = backup.create_backup(output_dir="my_backups")

if result["success"]:
    print(f"Backup saved to: {result['archive_path']}")
    print(f"Total repos: {result['stats']['total_repos']}")
```

### Example Scripts

Check out `example_usage.py` for detailed examples:
- Basic backups
- Authenticated backups
- Custom data processing
- Repository analytics
- Advanced filtering

Run examples:
```bash
python example_usage.py
```

## 🔑 Getting a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `public_repo` (for public repositories)
   - `repo` (for private repositories)
4. Generate and copy your token
5. Keep it secure - never commit tokens to version control!

## 📁 Output Structure

```
backups/
├── backup_20240115_143022/
│   ├── username_repos_20240115_143022.json
│   └── metadata.json
└── username_backup_20240115_143022.zip
```

### Backup Data Includes:
- Repository name and full name
- Description and URL
- Clone URLs (HTTPS & SSH)
- Primary language
- Star, fork, and issue counts
- Public/private status
- Creation and update timestamps
- Repository size
- Default branch
- Topics/tags
- Archived and disabled status

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "backup": {
    "output_directory": "backups",
    "create_archive": true,
    "archive_format": "zip"
  },
  "api": {
    "timeout": 30,
    "per_page": 100
  },
  "filters": {
    "include_private": true,
    "include_public": true,
    "min_stars": 0
  }
}
```

## 📊 Features Overview

### Web Interface
- 🎨 Modern, minimalist design
- 📱 Responsive layout
- 🔄 Real-time repository fetching
- 📈 Visual statistics and charts
- 💾 One-click download
- 🎯 Interactive repository browser
- 🚦 Rate limit indicator

### Core Library
- 🔌 RESTful GitHub API integration
- 🔄 Automatic pagination
- ⏱️ Rate limit handling
- 🛡️ Error handling and validation
- 📦 Automatic archiving
- 🏷️ Metadata generation
- 🔍 Repository processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Issues

- API rate limits: Without authentication, GitHub limits you to 60 requests/hour
- Large repositories: Processing accounts with hundreds of repos may take time

## 🔮 Future Enhancements

- [ ] Clone actual repository code (not just metadata)
- [ ] Support for GitHub Organizations
- [ ] Export to multiple formats (CSV, Excel, Markdown)
- [ ] Repository comparison over time
- [ ] Automated scheduled backups
- [ ] README content backup
- [ ] Contributor information export
- [ ] Release and tag information

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [GitHub REST API](https://docs.github.com/en/rest)
- Uses the [requests](https://requests.readthedocs.io/) library

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for the GitHub community
