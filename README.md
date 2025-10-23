# nomoemo

Python Script to seek out and eliminate emojis in code

## No Mo' Emoji!

A comprehensive emoji elimination tool designed for embedded systems development where emoji-free code is critical.

## Installation

### Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

### Setup
```bash
# Clone or download the repository
cd nomoemo/

# Install dependencies
pip install -r requirements.txt

# Or for development setup
python setup_dev.py
```

### Verify Installation
```bash
python nomoemo.py --version
# nomoemo.py 0.0.1
```

### Install Man Page (Optional)
For Unix-like systems, you can install the man page:
```bash
# Copy to system man directory (may require sudo)
cp nomoemo.1 /usr/local/share/man/man1/
# Update man database
mandb

# Then view with:
man nomoemo
```

## Documentation

- **[README.md](README.md)**: Complete installation and usage guide
- **[COMPLETED.md](COMPLETED.md)**: Archive of all completed development tasks
- **[TODO.md](TODO.md)**: Current development progress and remaining tasks
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**: Common issues and solutions
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and development notes

## Features

### Emoji Detection
The tool detects all Unicode emoji including:
- **Simple emojis**: 😀 🌍 ✅ ⚠️
- **Complex sequences**: 👨‍👩‍👧‍👦 (family emoji with ZWJ)
- **Skin tone modifiers**: 👍🏽 🤝🏾
- **Variation selectors**: ⚠️ (text vs emoji presentation)
- **ZWJ sequences**: All compound emoji combinations

### File Processing
- **Single files**: Process individual files
- **Directories**: Process all files in a directory
- **Recursive**: Process entire directory trees with `--recursive`
- **Binary detection**: Automatically skips binary files
- **Encoding support**: Handles UTF-8 files safely

### Operation Modes
- **Dry Run** (`--dry-run`): Scan and report emojis without modification
- **Remove** (`--remove`): Delete all emoji characters from files
- **Replace** (`--replace`): Replace emojis with custom ASCII character
- **ASCII-Only** (`--ascii-only`): Scan for non-ASCII characters (codepoints > 127)
- **Latin-1-Only** (`--latin1-only`): Scan for extended Unicode characters (codepoints > 255)

### Safety Features
- **Confirmation prompts**: Interactive confirmation for destructive operations
- **Force mode**: Bypass confirmations with `--force`
- **Backup awareness**: Works safely with version control
- **Encoding preservation**: Maintains file encoding integrity

## Usage

### Command Line Interface

```bash
python nomoemo.py [OPTIONS] TARGET

TARGET: File or directory to process
```

### Options

- `--dry-run`: Scan and report emojis without modifying files (default)
- `--remove`: Remove all emoji characters from files
- `--replace`: Replace emojis with specified character (requires --replacement)
- `--ascii-only`: Scan for non-ASCII characters (codepoints > 127) without modifying files
- `--latin1-only`: Scan for extended Unicode characters (codepoints > 255) without modifying files
- `--replacement CHAR`: Character to replace emojis with (single ASCII character)
- `--recursive`: Process directories recursively
- `--force`: Skip confirmation prompts for destructive operations
- `--quiet`: Suppress most output
- `--verbose`: Enable detailed output
- `--log FILE`: Log output to file
- `--help`: Show help message
- `--version`: Show version information

### Examples

```bash
# Scan a single file for emojis
python nomoemo.py --dry-run myfile.py

# Scan directory recursively and show detailed output
python nomoemo.py --dry-run --recursive --verbose ./src/

# Remove all emojis from files (with confirmation)
python nomoemo.py --remove --recursive ./project/

# Remove emojis without confirmation
python nomoemo.py --remove --force --recursive ./project/

# Replace emojis with asterisks
python nomoemo.py --replace --replacement "*" --recursive ./docs/

# Check for non-ASCII characters (IDE compatibility)
python nomoemo.py --ascii-only --recursive ./src/

# Check for extended Unicode characters
python nomoemo.py --latin1-only --verbose ./project/

# Quiet mode for CI/CD pipelines
python nomoemo.py --remove --force --quiet --recursive ./src/

# Log output to file
# Log output to file
python nomoemo.py --dry-run --log scan.log --recursive ./project/
```

## GitHub Actions Integration

### Implementing NoMoEmo in Other Projects

To add automated emoji checking to your own projects using GitHub Actions, follow these steps:

#### 1. Copy the Workflow File

Create the directory structure in your project:
```bash
mkdir -p .github/workflows
```

Copy the `emoji-check.yml` workflow from this repository to your project:
```bash
# Download from this repo or copy manually
curl -o .github/workflows/emoji-check.yml \
  https://raw.githubusercontent.com/your-org/nomoemo/main/.github/workflows/emoji-check.yml
```

#### 2. Customize the Workflow (Optional)

Edit `.github/workflows/emoji-check.yml` to match your project's needs:

**File Type Filtering**: Update the `paths` section to include your project's file types:
```yaml
paths:
  - '**/*.py'      # Python files
  - '**/*.js'      # JavaScript files
  - '**/*.ts'      # TypeScript files
  - '**/*.java'    # Java files
  - '**/*.cpp'     # C++ files
  - '**/*.c'       # C files
  - '**/*.h'       # Header files
  - '**/*.rs'      # Rust files
  - '**/*.go'      # Go files
  # Add your project's file extensions here
```

**Branch Names**: Update branch names if different from `main`/`master`/`develop`:
```yaml
on:
  push:
    branches: [ main, master ]  # Your main branches
  pull_request:
    branches: [ main, master ]  # Your main branches
```

**Directory Scanning**: For manual triggers, customize default directories:
```yaml
workflow_dispatch:
  inputs:
    directories:
      description: 'Directories to check'
      default: 'src,lib,app,core'  # Your typical source directories
```

#### 3. Add NoMoEmo to Your Project

**Option A: Direct Copy (Recommended for Small Teams)**
```bash
# Copy the nomoemo.py script to your project root
cp nomoemo.py your-project/
cp requirements.txt your-project/
```

**Option B: Git Submodule (Recommended for Large Teams)**
```bash
# Add as a git submodule
git submodule add https://github.com/your-org/nomoemo.git tools/nomoemo
cd tools/nomoemo
pip install -r requirements.txt
```

**Option C: Install as Package (When Available)**
```bash
# Future: when packaged for PyPI
pip install nomoemo
```

#### 4. Test the Integration

**Local Testing**:
```bash
# Test the workflow locally
python nomoemo.py --dry-run --recursive .

# Test with your file types
python nomoemo.py --dry-run --verbose *.py
```

**GitHub Actions Testing**:
1. Commit and push the workflow file
2. Create a pull request with some emoji-containing code
3. Verify the workflow runs and fails appropriately
4. Check the workflow logs for proper emoji detection

#### 5. Workflow Behavior

**On Pull Requests**:
- Checks only changed files for efficiency
- Fails the PR if emojis are found
- Provides helpful error messages with fix commands

**On Pushes to Main**:
- Performs full codebase scan
- Ensures no emojis slip through

**Manual Triggers**:
- Run on-demand via GitHub Actions UI
- Configurable directory scanning
- Useful for periodic codebase audits

#### 6. Troubleshooting Integration

**Workflow Not Running**:
- Check that `.github/workflows/emoji-check.yml` is committed
- Verify file paths match your project structure
- Ensure Python 3.8+ is available in GitHub Actions

**False Positives**:
- The tool automatically skips binary files
- Check encoding issues with `--verbose` flag
- Review file type filtering in workflow

**Performance Issues**:
- For large codebases, consider excluding certain directories
- Use `--quiet` mode in CI for faster runs
- The workflow caches pip dependencies for speed

#### Example: Minimal Integration

For a basic Python project, you only need:

1. **Copy files**:
   ```
   your-project/
   ├── .github/workflows/emoji-check.yml
   ├── nomoemo.py
   └── requirements.txt
   ```

2. **Basic workflow** (minimal customization needed):
   ```yaml
   name: NoMoEmo - Emoji Check
   on: [push, pull_request]
   jobs:
     emoji-check:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       - uses: actions/setup-python@v4
         with: python-version: '3.8'
       - run: pip install -r requirements.txt
       - run: python nomoemo.py --dry-run --quiet --recursive .
   ```

This provides automated emoji checking with minimal setup!
```

### Example Usage of emoji Library

Example from Repo:

```python
import emoji

# Simple emoji detection
text = "Hello 😀 World 🌍"
emoji_list = emoji.emoji_list(text)
print(emoji_list)  # [{'emoji': '😀', 'match_start': 6, 'match_end': 7}, ...]

# Replace emojis
clean_text = emoji.replace_emoji(text, replace='')
print(clean_text)  # "Hello  World "

# Replace with custom character
custom_text = emoji.replace_emoji(text, replace='*')
print(custom_text)  # "Hello * World *"
```        

