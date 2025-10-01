"""
Fetch command implementation
Fetch new accepted submissions from LeetCode using GraphQL API
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Set

import click
import requests

from .set_user import get_user_config

# Language extension mapping
LANGUAGE_EXTENSIONS = {
    "python": ".py",
    "python3": ".py",
    "javascript": ".js",
    "java": ".java",
    "cpp": ".cpp",
    "c": ".c"
}

# Difficulty mapping
DIFFICULTY_FOLDERS = {
    1: "easy",
    2: "medium", 
    3: "hard"
}

class LeetCodeAPI:
    """LeetCode API client for fetching submissions"""
    
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.session = requests.Session()
        self.base_url = "https://leetcode.com/graphql"
        
        # Set up session headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://leetcode.com/",
            "Cookie": f"LEETCODE_SESSION={cookie}",
        })
    
    def get_submission_detail(self, submission_id: str) -> Dict:
        """Get detailed submission info including code"""
        query = """
        query submissionDetails($submissionId: Int!) {
            submissionDetails(submissionId: $submissionId) {
                runtime
                runtimeDisplay
                runtimePercentile
                runtimeDistribution
                memory
                memoryDisplay
                memoryPercentile
                memoryDistribution
                code
                timestamp
                statusCode
                user {
                    username
                    profile {
                        realName
                        userAvatar
                    }
                }
                lang {
                    name
                    verboseName
                }
                question {
                    questionId
                    titleSlug
                    title
                    translatedTitle
                    difficulty
                }
                notes
                flagType
                topicTags {
                    name
                    slug
                }
                runtimeError
                compileError
                lastTestcase
            }
        }
        """
        
        variables = {"submissionId": int(submission_id)}
        payload = {"query": query, "variables": variables}
        
        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        
        return data["data"]["submissionDetails"]

    def fetch_submissions(self, offset: int = 0, limit: int = 50) -> Dict:
        """
        Fetch submissions from LeetCode GraphQL API
        
        Based on research and specification:
        - Uses submissionList query
        - Fetches in batches of 50
        - Returns submissions with required fields
        """
        
        # GraphQL query - corrected based on LeetCode's actual API
        query = """
        query submissionList($offset: Int!, $limit: Int!) {
            submissionList(offset: $offset, limit: $limit) {
                lastKey
                hasNext
                submissions {
                    id
                    title
                    titleSlug
                    status
                    statusDisplay
                    lang
                    runtime
                    timestamp
                    url
                    isPending
                    memory
                    __typename
                }
            }
        }
        """
        
        variables = {
            "offset": offset,
            "limit": limit
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        response = self.session.post(self.base_url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")
        
        return data["data"]["submissionList"]
    
    def fetch_all_accepted_submissions(self) -> List[Dict]:
        """
        Fetch all accepted submissions with pagination
        Only returns submissions with statusDisplay == "Accepted"
        """
        all_submissions = []
        offset = 0
        limit = 20  # Reduce limit to be more conservative
        
        logger = logging.getLogger()
        
        while True:
            try:
                logger.info(f"Fetching submissions: offset={offset}, limit={limit}")
                
                # Retry logic: 3 attempts with 2-second delay
                for attempt in range(3):
                    try:
                        result = self.fetch_submissions(offset, limit)
                        break
                    except Exception as e:
                        if attempt < 2:  # Not the last attempt
                            logger.warning(f"API call failed (attempt {attempt + 1}/3): {e}")
                            time.sleep(2)
                        else:
                            raise
                
                submissions = result.get("submissions", [])
                
                if not submissions:
                    break
                
                # Filter for accepted submissions only
                accepted_submissions = [
                    sub for sub in submissions 
                    if sub.get("statusDisplay") == "Accepted"
                ]
                
                logger.info(f"Found {len(accepted_submissions)} accepted submissions in this batch")
                
                # Get detailed info for each accepted submission (including code)
                detailed_submissions = []
                for submission in accepted_submissions:
                    try:
                        submission_id = submission.get("id")
                        if submission_id:
                            logger.info(f"Fetching details for submission {submission_id}")
                            details = self.get_submission_detail(submission_id)
                            
                            # Merge the basic info with detailed info
                            merged_submission = {
                                **submission,
                                "code": details.get("code", ""),
                                "question": details.get("question", {}),
                                "lang_details": details.get("lang", {})
                            }
                            detailed_submissions.append(merged_submission)
                            
                            # Small delay to be respectful to the API
                            time.sleep(0.5)
                            
                    except Exception as e:
                        logger.warning(f"Failed to get details for submission {submission.get('id')}: {e}")
                        # Continue with basic submission info if details fail
                        detailed_submissions.append(submission)
                
                all_submissions.extend(detailed_submissions)
                
                # Check if there are more submissions
                if not result.get("hasNext", False) or len(submissions) < limit:
                    break
                
                offset += limit
                
                # Rate limiting - be respectful to LeetCode
                time.sleep(2)
                
            except Exception as e:
                if "session" in str(e).lower() or "unauthorized" in str(e).lower() or "401" in str(e):
                    raise Exception("Session cookie may have expired. Please run 'set_cookie' to update.")
                raise
        
        logger.info(f"Total accepted submissions fetched: {len(all_submissions)}")
        return all_submissions

def get_existing_files(repo_dir: Path = None) -> Set[str]:
    """Get set of existing submission files to avoid duplicates"""
    if repo_dir is None:
        repo_dir = Path.cwd()
    
    existing_files = set()
    
    for difficulty in ["easy", "medium", "hard"]:
        difficulty_dir = repo_dir / "leetcodeProblems" / difficulty
        if difficulty_dir.exists():
            for file_path in difficulty_dir.iterdir():
                if file_path.is_file() and file_path.suffix in LANGUAGE_EXTENSIONS.values():
                    # Use filename without extension as identifier
                    existing_files.add(file_path.stem)
    
    return existing_files

def save_submission(submission: Dict, project_root: Path) -> bool:
    """
    Save a submission to the appropriate directory
    Returns True if file was saved, False if skipped
    """
    logger = logging.getLogger()
    
    try:
        # Extract submission data - handle both old and new structure
        title_slug = submission.get("titleSlug", "")
        lang = submission.get("lang", "").lower()
        code = submission.get("code", "")
        
        # Handle different difficulty formats
        question_data = submission.get("question", {})
        difficulty = question_data.get("difficulty")
        
        # Convert difficulty string to number if needed
        if isinstance(difficulty, str):
            difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
            difficulty = difficulty_map.get(difficulty, difficulty)
        
        title = submission.get("title", "") or question_data.get("title", "")
        
        if not all([title_slug, lang, code]):
            logger.warning(f"Missing required fields for submission: {submission.get('id')}")
            logger.warning(f"Fields: title_slug={title_slug}, lang={lang}, code={'present' if code else 'missing'}")
            return False
        
        # Get file extension
        extension = LANGUAGE_EXTENSIONS.get(lang)
        if not extension:
            logger.warning(f"Unsupported language: {lang}")
            return False
        
        # Get difficulty folder - default to medium if unknown
        difficulty_folder = DIFFICULTY_FOLDERS.get(difficulty, "medium")
        
        # Create file path
        filename = f"{title_slug}{extension}"
        file_path = project_root / "leetcodeProblems" / difficulty_folder / filename
        
        # Check if file already exists
        if file_path.exists():
            return False  # Will be handled by duplicate detection
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare code content with header comment
        header_comment = get_header_comment(submission, extension)
        full_content = header_comment + "\n\n" + code
        
        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"Saved submission: {file_path.relative_to(project_root)}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save submission {submission.get('id')}: {e}")
        return False

def get_header_comment(submission: Dict, extension: str) -> str:
    """Generate header comment for the submission file"""
    title = submission.get("title", "") or submission.get("question", {}).get("title", "")
    title_slug = submission.get("titleSlug", "")
    lang = submission.get("lang", "")
    
    # Handle difficulty from different possible sources
    difficulty = submission.get("question", {}).get("difficulty", "")
    if isinstance(difficulty, int):
        difficulty_text = DIFFICULTY_FOLDERS.get(difficulty, str(difficulty))
    else:
        difficulty_text = difficulty.lower() if difficulty else "unknown"
    
    if extension in [".py"]:
        return f'''"""
LeetCode Problem: {title}
Difficulty: {difficulty_text.title()}
Language: {lang}
Link: https://leetcode.com/problems/{title_slug}/

Auto-generated by LeetCode Submission Auto GitHub Push
"""'''
    elif extension in [".js"]:
        return f'''/**
 * LeetCode Problem: {title}
 * Difficulty: {difficulty_text.title()}
 * Language: {lang}
 * Link: https://leetcode.com/problems/{title_slug}/
 * 
 * Auto-generated by LeetCode Submission Auto GitHub Push
 */'''
    elif extension in [".java", ".cpp", ".c"]:
        return f'''/**
 * LeetCode Problem: {title}
 * Difficulty: {difficulty_text.title()}
 * Language: {lang}
 * Link: https://leetcode.com/problems/{title_slug}/
 * 
 * Auto-generated by LeetCode Submission Auto GitHub Push
 */'''
    else:
        return f'''// LeetCode Problem: {title}
// Difficulty: {difficulty_text.title()}
// Language: {lang}
// Link: https://leetcode.com/problems/{title_slug}/
// 
// Auto-generated by LeetCode Submission Auto GitHub Push'''

def handle_duplicates(duplicates: List[Dict], project_root: Path) -> List[Dict]:
    """
    Handle duplicate submissions with user input
    Returns list of submissions to save
    """
    if not duplicates:
        return []
    
    logger = logging.getLogger()
    
    click.echo(f"\n⚠️  {len(duplicates)} files are duplicates:")
    for i, submission in enumerate(duplicates, 1):
        title = submission.get("title", "Unknown")
        lang = submission.get("lang", "unknown")
        difficulty = DIFFICULTY_FOLDERS.get(submission.get("question", {}).get("difficulty", 0), "unknown")
        click.echo(f"  {i}. {title} ({lang}) - {difficulty}")
    
    click.echo()
    click.echo("i = Ignore (keep old code)")
    click.echo("w = Overwrite (replace old code)")
    click.echo()
    click.echo("⚠️  Warning: If code approach changed, Ignore will not update it; Overwrite may delete previous approach.")
    
    choice = click.prompt("Choose action", type=click.Choice(['i', 'w']), default='w')
    
    if choice == 'w':
        logger.info(f"User chose to overwrite {len(duplicates)} duplicate files")
        return duplicates
    else:
        logger.info(f"User chose to ignore {len(duplicates)} duplicate files") 
        return []

def fetch_submissions():
    """Main fetch command - fetch new accepted submissions from LeetCode"""
    logger = logging.getLogger()
    
    try:
        # Get user configuration
        username, config = get_user_config()
        
        leetcode_cookie = config.get("LEETCODE_COOKIE", "")
        if not leetcode_cookie:
            raise click.ClickException("LeetCode cookie not set. Please run 'set_cookie' command first.")
        
        click.echo(f"🚀 Fetching submissions for user: {username}")
        click.echo()
        
        # Initialize API client
        api = LeetCodeAPI(leetcode_cookie)
        
        # Get GitHub repository directory from user config
        github_repo_dir = Path(config["GITHUB_REPO_DIR"])
        
        # Get existing files to detect duplicates
        existing_files = get_existing_files(github_repo_dir)
        click.echo(f"📁 Found {len(existing_files)} existing submission files")
        
        # Fetch all accepted submissions
        click.echo("🔍 Fetching submissions from LeetCode...")
        submissions = api.fetch_all_accepted_submissions()
        
        if not submissions:
            click.echo("ℹ️  No accepted submissions found")
            return
        
        click.echo(f"✅ Fetched {len(submissions)} accepted submissions")
        
        # Separate new and duplicate submissions
        new_submissions = []
        duplicate_submissions = []
        
        for submission in submissions:
            title_slug = submission.get("titleSlug", "")
            if title_slug in existing_files:
                duplicate_submissions.append(submission)
            else:
                new_submissions.append(submission)
        
        click.echo(f"📊 Analysis: {len(new_submissions)} new, {len(duplicate_submissions)} duplicates")
        
        # Handle duplicates if any
        submissions_to_save = new_submissions.copy()
        if duplicate_submissions:
            duplicate_choices = handle_duplicates(duplicate_submissions, github_repo_dir)
            submissions_to_save.extend(duplicate_choices)
        
        # Save submissions to GitHub repository directory
        if submissions_to_save:
            click.echo(f"\n💾 Saving {len(submissions_to_save)} submissions to {github_repo_dir}...")
            saved_count = 0
            
            for submission in submissions_to_save:
                if save_submission(submission, github_repo_dir):
                    saved_count += 1
            
            click.echo(f"✅ Successfully saved {saved_count} submissions")
            logger.info(f"Fetch completed: {saved_count} submissions saved")
            
            if saved_count > 0:
                click.echo()
                click.echo("🚀 Next step: Run 'python leetcode_auto_push.py git_push' to push changes to GitHub")
        else:
            click.echo("ℹ️  No new submissions to save")
        
    except Exception as e:
        error_msg = f"Failed to fetch submissions: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)