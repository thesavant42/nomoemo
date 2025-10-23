# NoMoEmo Troubleshooting Guide

## Common Issues and Solutions

### File Access Errors

**Problem:** `Permission denied` or `Access is denied` errors
```
[ERROR] Could not decode test_files/simple_emojis.py as UTF-8: Permission denied
```

**Solutions:**
- Ensure you have read/write permissions for the target files
- On Windows, try running as Administrator if accessing system directories
- Check if files are locked by another process

### Encoding Issues

**Problem:** `Could not decode file as UTF-8` errors
```
[WARNING] Could not decode file.py as UTF-8: 'utf-8' codec can't decode byte 0xff in position 0
```

**Solutions:**
- NoMoEmo only supports UTF-8 encoded files
- Convert files to UTF-8 encoding before processing
- Binary files are automatically skipped (this is normal behavior)

### No Files Found

**Problem:** `No files found to process.` message
```
[INFO] No files found to process.
```

**Solutions:**
- Check that the target path exists: `ls -la /path/to/target`
- Ensure you're not trying to process binary files (automatically skipped)
- Hidden files and directories (starting with `.`) are processed
- Use `--recursive` if you want to process subdirectories

### Command Not Found

**Problem:** `python: command not found` or similar
```
python: command not found
```

**Solutions:**
- Ensure Python 3.8+ is installed: `python --version`
- Use `python3` instead of `python`: `python3 nomoemo.py`
- Add Python to your PATH environment variable

### Library Import Errors

**Problem:** `ModuleNotFoundError: No module named 'emoji'`
```
ModuleNotFoundError: No module named 'emoji'
```

**Solutions:**
- Install dependencies: `pip install -r requirements.txt`
- Use virtual environment: `python -m venv venv && source venv/bin/activate`
- Upgrade pip: `pip install --upgrade pip`

### Unexpected Behavior

**Problem:** Tool behaves differently than expected

**Debug Steps:**
1. Enable verbose output: `nomoemo.py --dry-run --verbose target/`
2. Check log file: `nomoemo.py --dry-run --log debug.log target/`
3. Test with simple file: `nomoemo.py --dry-run test_files/simple_emojis.py`
4. Verify emoji detection: `python -c "import emoji; print(emoji.emoji_list('Hello 😀 World 🌍'))"`
5. Test character set compliance: `nomoemo.py --ascii-only --verbose target/`
6. Check for encoding issues: `file target/file.py` (Linux/macOS) or use a text editor

## Performance Issues

### Large Codebases
For very large codebases, consider:
- Use `--quiet` to reduce output overhead
- Process specific directories instead of entire trees
- Run during off-peak hours for CI/CD

### Memory Usage
The tool loads entire files into memory. For extremely large files:
- Split large files into smaller chunks manually
- Process files individually instead of entire directories

## CI/CD Integration Issues

### Exit Codes
- **Exit code 0**: Success, no emojis found or successfully processed
- **Exit code 1**: Error occurred (check logs)
- **Exit code 130**: User cancelled (shouldn't happen in CI/CD)

### GitHub Actions
If using the provided GitHub Action, ensure:
- The workflow has proper permissions to read repository contents
- Python and dependencies are properly installed
- The action runs on appropriate events (pull_request, push)

## Character Set Compliance Issues

### Non-ASCII Characters Detected

**Problem:** `--ascii-only` mode reports non-ASCII characters
```
[WARNING] [!] 1 files contain non-ASCII characters (codepoints > 127).
```

**Solutions:**
- This is normal for files containing accented characters, symbols, or emojis
- Use `--latin1-only` to check for characters beyond Latin-1 (codepoints > 255)
- For embedded systems, consider converting to ASCII-only character sets
- Check if your IDE/editor supports the detected characters

### Extended Unicode Characters

**Problem:** `--latin1-only` mode reports extended Unicode characters
```
[WARNING] [!] 1 files contain extended Unicode characters (codepoints > 255).
```

**Solutions:**
- Characters above codepoint 255 may not display correctly in some IDEs
- Consider replacing with Latin-1 equivalents where possible
- Use `--verbose` to see exactly which characters are causing issues
- For maximum compatibility, aim for ASCII-only (codepoints 0-127)

### Character Set Mode Confusion

**Problem:** Unsure which character set mode to use

**Solutions:**
- `--ascii-only`: Strictest - detects any characters above ASCII (127)
- `--latin1-only`: Moderate - allows Latin-1 but flags extended Unicode (255+)
- Use `--verbose` with either mode to see detailed character information
- Test files with known character sets to understand the boundaries

### IDE Display Issues

**Problem:** Characters display as boxes or question marks in your IDE

**Solutions:**
- Run `--ascii-only` or `--latin1-only` to identify problematic characters
- Convert files to UTF-8 with BOM if your IDE requires it
- Check your IDE's font settings for Unicode support
- Consider using ASCII-only character sets for maximum compatibility

## Platform-Specific Issues

### Windows
- Use PowerShell or Command Prompt (not WSL for file paths)
- Ensure proper permissions for file operations
- Long path names may cause issues (Windows path length limits)

### Linux/macOS
- Ensure proper file permissions (755 for scripts, 644 for files)
- Check available disk space for log files
- Verify locale settings for Unicode support

## Getting Help

1. Check this troubleshooting guide
2. Review the README.md for usage examples
3. Use `--help` for command-line assistance
4. Check existing issues in the project repository
5. Enable verbose logging and include output when reporting bugs
6. For character set issues, try `--ascii-only --verbose` or `--latin1-only --verbose` to get detailed character information

## Emergency Recovery

If files are accidentally modified:
1. Use version control to revert changes: `git checkout -- file.py`
2. Restore from backups if available
3. Use `--dry-run` first on any recovery operations