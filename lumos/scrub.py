import re

# Common patterns for API keys and tokens
SECRET_REGEXES = [
    re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}"),                     # Slack tokens
    re.compile(r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"), # AWS keys
    re.compile(r"gh[opsubr]_[0-9a-zA-Z]{36,40}"),                      # GitHub tokens
    re.compile(r"ey[a-zA-Z0-9-_]+\.ey[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+"), # JWT tokens
    # Generic assignments like api_key = "..." or password = '...'
    re.compile(r"(?i)(password|passwd|secret|token|api_key|auth_key|private_key)\s*=\s*['\"][^'\"]+['\"]")
]

BLOCKED_PATTERNS = [
    ".env",
    ".pem",
    "id_rsa",
    "git-credentials",
    ".netrc",
    ".pypirc"
]

def should_ignore_path(path_str: str) -> bool:
    """Returns True if the path contains sensitive extensions or names."""
    name = path_str.lower()
    return any(p in name for p in BLOCKED_PATTERNS)

def scrub_string(input_str: str) -> str:
    """Redacts common credentials and secret patterns from strings."""
    scrubbed = input_str
    
    # Redact JWTs, Slack tokens, AWS/GitHub keys
    for regex in SECRET_REGEXES[:4]:
        scrubbed = regex.sub("[REDACTED_SECRET]", scrubbed)
        
    # Redact generic key/password assignments (preserving the key name)
    def assignment_replacer(match):
        # Match groups contain key name
        full_match = match.group(0)
        # Split on '=' to preserve 'password ='
        parts = full_match.split("=", 1)
        return f"{parts[0]}= '[REDACTED_CREDENTIAL]'"
        
    scrubbed = SECRET_REGEXES[4].sub(assignment_replacer, scrubbed)
    return scrubbed

def filter_dirty_files(files_list: list) -> list:
    """Filters out sensitive directories or files from the active file list."""
    return [f for f in files_list if not should_ignore_path(f)]
