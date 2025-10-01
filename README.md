# LeetCode Submission Auto GitHub Push

A professional CLI tool to automatically fetch and organize your LeetCode submissions, then optionally push them to a GitHub repository.

## Features

- 🚀 **Automated Fetching**: Automatically fetch your latest accepted LeetCode submissions
- 📁 **Smart Organization**: Organize submissions by difficulty (easy, medium, hard) and programming language
- 🔐 **Privacy First**: Store sensitive cookies and user data separately (never pushed to Git)
- 🔄 **Duplicate Handling**: Intelligent duplicate detection with user choice to ignore or overwrite
- 📝 **Comprehensive Logging**: Detailed logging of all operations and errors
- 🌐 **Cross-platform**: Works on Windows, Mac, and Linux
- 🎯 **Multiple Languages**: Supports Python, JavaScript, Java, C++, and C

## Installation

1. **Clone or download this project:**
   ```bash
   git clone <your-repo-url>
   cd leetcode_auto_submit
   ```

2. **Platform-specific setup:**

   **Windows (Recommended):**
   ```powershell
   # Run PowerShell as Administrator (optional for global install)
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```

   **Mac/Linux:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   **Manual Setup (All Platforms):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   # Windows
   lcsync help
   
   # Mac/Linux  
   ./lcsync help
   
   # Universal
   python lcsync.py help
   ```

4. **Ensure Git is installed and configured:**
   ```bash
   git --version
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## Quick Start

### 1. Initialize the Project
```bash
lcsync init
```
This creates the necessary folder structure and configuration files.

### 2. Set Up User Configuration
```bash
lcsync user
```
You'll be prompted for:
- Username
- Local GitHub repository path
- Commit message (default: "Update LeetCode submissions")

### 3. Set Your LeetCode Session Cookie
```bash
lcsync cookie
```

**How to get your LeetCode session cookie:**
1. Go to [leetcode.com](https://leetcode.com) and log in
2. Open browser developer tools (F12)
3. Go to Application/Storage > Cookies > https://leetcode.com
4. Find the 'LEETCODE_SESSION' cookie and copy its value
5. Paste the entire cookie string when prompted

### 4. Fetch Your Submissions
```bash
lcsync fetch
```
This will:
- Fetch all your accepted submissions from LeetCode
- Save them in organized folders by difficulty
- Handle duplicates with your input
- Add header comments with problem information

### 5. Push to GitHub (Optional)
```bash
lcsync push
```
This runs: `git add .`, `git commit`, and `git push` in sequence.

## Alternative Commands

If you prefer the full command names, you can still use:
```bash
python leetcode_auto_push.py init
python leetcode_auto_push.py set-user
python leetcode_auto_push.py set-cookie
python leetcode_auto_push.py fetch
python leetcode_auto_push.py git-push
```

## Project Structure

```
leetcode_auto_submit/
│
├── leetcode_auto_push.py       # Main CLI entry point
├── commands/                   # Command implementations
│   ├── __init__.py
│   ├── init.py                # Initialize project
│   ├── set_user.py            # User configuration
│   ├── set_cookie.py          # Cookie management
│   ├── fetch.py               # LeetCode API integration
│   └── git_push.py            # Git operations
├── users/                     # User data (ignored by Git)
│   └── .gitignore             # Protects sensitive data
├── leetcodeProblems/          # Your submissions
│   ├── easy/                  # Easy difficulty problems
│   ├── medium/                # Medium difficulty problems
│   └── hard/                  # Hard difficulty problems
├── requirements.txt           # Python dependencies
├── leetcode_auto_push.log     # Operation logs
└── README.md                  # This file
```

## Commands Reference

### Short Commands (Recommended)
| Command | Description |
|---------|-------------|
| `lcsync init` | Initialize project folders and .gitignore |
| `lcsync user` | One-time user setup (username, repo path, commit message) |
| `lcsync cookie` | Update/change LeetCode session cookie |
| `lcsync fetch` | Fetch new accepted submissions from LeetCode |
| `lcsync push` | Bundle git add, commit, and push operations |
| `lcsync help` | Show help and available commands |

### Full Commands (Alternative)
| Command | Description |
|---------|-------------|
| `python leetcode_auto_push.py init` | Initialize project folders and .gitignore |
| `python leetcode_auto_push.py set-user` | One-time user setup (username, repo path, commit message) |
| `python leetcode_auto_push.py set-cookie` | Update/change LeetCode session cookie |
| `python leetcode_auto_push.py fetch` | Fetch new accepted submissions from LeetCode |
| `python leetcode_auto_push.py git-push` | Bundle git add, commit, and push operations |

## Complete Usage Workflow

### Easy 5-Step Process:
```bash
# Step 1: Initialize project
lcsync init

# Step 2: Set up user configuration  
lcsync user
   
# Step 3: Add LeetCode session cookie
lcsync cookie
   
# Step 4: Fetch submissions
lcsync fetch
   
# Step 5: Push to GitHub
lcsync push
```

### For Future Updates:
```bash
# Get new submissions and push to GitHub
lcsync fetch
lcsync push
```

## Cross-Platform Usage

### Command Options by Platform

| Platform | Method | Example | Notes |
|----------|--------|---------|-------|
| **Windows CMD** | Batch file | `lcsync help` | Easiest, works out of the box |
| **Windows PowerShell** | PS1 script | `.\lcsync.ps1 help` | Good for PowerShell users |
| **Mac/Linux** | Shell script | `./lcsync help` | Need `chmod +x lcsync` first |
| **Universal** | Direct Python | `python lcsync.py help` | Works on all platforms |

### Detailed Examples

**Windows:**
```cmd
# Command Prompt (CMD)
cd d:\leetcode_auto_submit
lcsync init
lcsync user
lcsync fetch

# PowerShell
cd d:\leetcode_auto_submit  
.\lcsync.ps1 init
.\lcsync.ps1 user
.\lcsync.ps1 fetch
```

**Mac/Linux:**
```bash
# Terminal
cd /path/to/leetcode_auto_submit
chmod +x lcsync        # First time only
./lcsync init
./lcsync user
./lcsync fetch
```

**Universal (All Platforms):**
```bash
# Works everywhere Python is installed
python lcsync.py init
python lcsync.py user
python lcsync.py cookie
python lcsync.py fetch
python lcsync.py push
```

## File Naming Convention

Submissions are saved as:
- **Filename**: `{problem-slug}.{extension}`
- **Extensions**: `.py`, `.js`, `.java`, `.cpp`, `.c`
- **Location**: `leetcodeProblems/{difficulty}/`

Example: `two-sum.py` in `leetcodeProblems/easy/`

## Duplicate Handling

When duplicate submissions are found, you'll be prompted:
```
⚠️ 5 files are duplicates:
  1. Two Sum (python) - easy
  2. Add Two Numbers (java) - medium
  ...

i = Ignore (keep old code)
w = Overwrite (replace old code)

Choose action [w]: 
```

**Warning**: If your code approach changed, "Ignore" will not update it; "Overwrite" may delete your previous approach.

## Configuration Files

User configurations are stored in `users/{username}.json`:
```json
{
  "LEETCODE_COOKIE": "your_session_cookie_here",
  "GITHUB_REPO_DIR": "/path/to/your/github/repo",
  "GITHUB_COMMIT_MESSAGE": "Update LeetCode submissions"
}
```

## Logging

All operations are logged to `leetcode_auto_push.log` with timestamps:
```
2025-10-01 12:00:00,123 - INFO - Created user configuration for: john_doe
2025-10-01 12:05:15,456 - INFO - Fetched 25 accepted submissions
2025-10-01 12:05:30,789 - INFO - Saved submission: leetcodeProblems/easy/two-sum.py
```

## Troubleshooting

### Common Issues

1. **"Session cookie may have expired"**
   - Run `python leetcode_auto_push.py set_cookie` to update your cookie
   - Make sure you're logged into LeetCode in your browser

2. **"Git push failed: permission denied"**
   - Check your Git authentication (SSH key or personal access token)
   - Verify your GitHub repository URL with `git remote -v`

3. **"Repository path does not exist"**
   - Ensure the GitHub repository path you provided exists
   - Make sure it's a valid Git repository (contains .git folder)

4. **"No accepted submissions found"**
   - Make sure you have solved problems on LeetCode
   - Check that your session cookie is valid
   - Verify you're logged into the correct LeetCode account

### API Rate Limiting

The tool includes built-in rate limiting and retry logic:
- Fetches submissions in batches of 50
- 1-second delay between API calls
- 3 retry attempts with 2-second delays on failure

### Multiple Users

You can manage multiple LeetCode accounts:
- Run `set_user` for each account
- The tool will prompt you to select which user when multiple configs exist
- Each user has their own cookie and repository configuration

## Security & Privacy

- **Sensitive data protection**: All cookies and user data stored in `users/` directory
- **Git ignore**: `users/` directory is automatically ignored by Git
- **No data exposure**: Sensitive information never pushed to GitHub
- **Local storage**: All user configurations stored locally only

## Contributing

This project follows professional development practices:
- Modular command structure
- Comprehensive error handling
- Detailed logging
- Type hints and documentation
- Cross-platform compatibility

## License

This project is provided as-is for educational and personal use.

---

**Happy coding! 🚀**