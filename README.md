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
   git clone https://github.com/GodXSpell/lcsync.git
   cd lcsync
   ```
   
   *Note: Replace the URL with your actual repository URL and navigate to your cloned directory*

2. **Platform-specific setup:**

   **Windows (Recommended):**
   ```powershell
   # Run PowerShell as Administrator (optional for global install)
   # Navigate to your cloned directory first
   cd path\to\your\cloned\lcsync
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```

   **Mac/Linux:**
   ```bash
   # Navigate to your cloned directory first
   cd /path/to/your/cloned/lcsync
   chmod +x setup.sh
   ./setup.sh
   ```

   **Manual Setup (All Platforms):**
   ```bash
   # Dependencies will be automatically checked and installed during 'lcsync init'
   # Or install manually if needed:
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   # Windows CMD
   lcsync help
   
   # Windows PowerShell (if execution policy blocks scripts)
   .\lcsync.cmd help
   
   # Universal (works in any directory after cd to project)
   python lcsync.py help
   ```

4. **If commands don't work:**
   - **PowerShell**: Try `.\lcsync.cmd help` (always works)
   - **CMD**: Try `lcsync help` (should work with PATH)
   - **Universal**: `python lcsync.py help` (works everywhere)
   - **For global access**: Restart your terminal after adding to PATH

4. **Ensure Git is installed and configured:**
   ```bash
   git --version
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## Quick Start

### 1. Initialize the Tool
```bash
lcsync init
```
This will:
- Check for required Python dependencies (click, requests)
- Offer to automatically install missing packages
- Set up the lcsync tool (users folder, logs, configuration files)

### 2. Set Up Target Repository
```bash
lcsync user
```
You'll be prompted for:
- Username
- Local GitHub repository path (where your solutions will be stored)
- Commit message (default: "Update LeetCode submissions")

This command will create the `leetcodeProblems/` directory structure in your chosen repository.

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
# Push with automatic commit message
lcsync push

# Push with custom commit message  
lcsync push -m "Added dynamic programming solutions"
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
lcsync/                         # Tool directory
│
├── leetcode_auto_push.py       # Main CLI entry point
├── lcsync.py                  # Short command wrapper
├── commands/                   # Command implementations
│   ├── __init__.py
│   ├── init.py                # Initialize tool
│   ├── set_user.py            # User configuration & target repo setup
│   ├── set_cookie.py          # Cookie management
│   ├── fetch.py               # LeetCode API integration
│   └── git_push.py            # Git operations
├── users/                     # User data (ignored by Git)
│   └── .gitignore             # Protects sensitive data
├── requirements.txt           # Python dependencies
├── leetcode_auto_push.log     # Operation logs
└── README.md                  # This file

your-leetcode-repo/             # Your target repository (separate location)
│
├── leetcodeProblems/          # Your submissions (created by 'lcsync user')
│   ├── easy/                  # Easy difficulty problems
│   ├── medium/                # Medium difficulty problems
│   └── hard/                  # Hard difficulty problems
├── README.md                  # Your repository documentation
└── .git/                      # Your Git repository
```

## Commands Reference

### Short Commands (Recommended)
| Command | Description |
|---------|-------------|
| `lcsync init` | Initialize lcsync tool (dependencies, users folder, logs) |
| `lcsync user` | Set up target repository and create LeetCode directory structure |
| `lcsync cookie` | Update/change LeetCode session cookie |
| `lcsync fetch` | Fetch new accepted submissions from LeetCode |
| `lcsync push` | Bundle git add, commit, and push operations |
| `lcsync push -m "message"` | Push with custom commit message |
| `lcsync help` | Show help and available commands |

### Full Commands (Alternative)
| Command | Description |
|---------|-------------|
| `python leetcode_auto_push.py init` | Initialize lcsync tool (dependencies, users folder, logs) |
| `python leetcode_auto_push.py set-user` | Set up target repository and create LeetCode directory structure |
| `python leetcode_auto_push.py set-cookie` | Update/change LeetCode session cookie |
| `python leetcode_auto_push.py fetch` | Fetch new accepted submissions from LeetCode |
| `python leetcode_auto_push.py git-push` | Bundle git add, commit, and push operations |

## Complete Usage Workflow

### Easy 5-Step Process:
```bash
# Step 1: Initialize the lcsync tool
lcsync init

# Step 2: Set up your target repository
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

# Or with custom commit message
lcsync fetch  
lcsync push -m "Week 3 progress - tree problems completed"
```

## Cross-Platform Usage

### Command Options by Platform

| Platform | Method | Example | Notes |
|----------|--------|---------|-------|
| **Windows CMD** | CMD file | `lcsync help` | Works out of the box |
| **Windows PowerShell** | CMD file | `lcsync help` | Works after adding to PATH |
| **Mac/Linux** | Shell script | `./lcsync.sh help` | Need `chmod +x lcsync.sh` first |
| **Universal** | Direct Python | `python lcsync.py help` | Works on all platforms |

### Detailed Examples

**Windows:**
```cmd
# Command Prompt (CMD) 
cd your_project_path\leetcode_auto_submit
lcsync init
lcsync user
lcsync fetch

# PowerShell (if execution policy blocks scripts)
cd your_project_path\leetcode_auto_submit
lcsync init              # Usually works
.\lcsync.cmd init        # If above fails
python lcsync.py init    # Always works
```

**Mac/Linux:**
```bash
# Terminal (after chmod +x lcsync.sh)
cd your_project_path/leetcode_auto_submit
chmod +x lcsync.sh
./lcsync.sh init
./lcsync.sh user
./lcsync.sh fetch
```

**Universal (any platform):**
```bash
# Works everywhere Python is installed
cd your_project_path/leetcode_auto_submit
python lcsync.py init
python lcsync.py user
python lcsync.py fetch
```
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

1. **"Missing dependencies" during init**
   - The `lcsync init` command will automatically detect and offer to install missing packages
   - If automatic installation fails, run manually: `pip install click requests`
   - Ensure you have Python 3.7+ and pip installed

2. **PowerShell "execution policy" errors**
   - Error: `"running scripts is disabled on this system"`
   - Solution 1: Use `lcsync` (works in PowerShell without policy issues)
   - Solution 2: Use `.\lcsync.cmd` explicitly  
   - Solution 3: Use `python lcsync.py` (always works)
   - Solution 4: Enable scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. **"Session cookie may have expired"**
   - Run `lcsync cookie` to update your cookie
   - Make sure you're logged into LeetCode in your browser

3. **"Git push failed: permission denied"**
   - Check your Git authentication (SSH key or personal access token)
   - Verify your GitHub repository URL with `git remote -v`

4. **"Repository path does not exist"**
   - Ensure the GitHub repository path you provided exists
   - Make sure it's a valid Git repository (contains .git folder)

5. **"No accepted submissions found"**
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