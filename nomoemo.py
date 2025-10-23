#!/usr/bin/env python3
"""
nomoemo.py - No Mo' Emoji!

A Python script to seek out and eliminate emojis in code files.
Designed for embedded systems development where emoji-free code is critical.

Author: savan42
Version: 0.0.1
"""

import argparse
import logging
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
import emoji


class NoMoEmo:
    """Main class for emoji detection and elimination."""
    
    def __init__(self, args):
        """Initialize NoMoEmo with command line arguments."""
        self.args = args
        self.logger = self._setup_logging()
        self.emoji_count = 0
        self.files_processed = 0
        self.files_with_emojis = 0
        
        # Character set violation tracking
        self.files_with_charset_violations = 0
        self.charset_violations = []  # List of (file_path, char, codepoint, line, col) tuples
        
        self.emoji_regex = self._build_emoji_regex()
        
    def _build_emoji_regex(self) -> re.Pattern:
        """Build a comprehensive regex pattern for detecting all Unicode emojis."""
        # Sort emoji by length (descending) to match multi-character emojis first
        emojis = sorted(emoji.EMOJI_DATA.keys(), key=len, reverse=True)
        pattern = '(' + '|'.join(re.escape(u) for u in emojis) + ')'
        return re.compile(pattern, re.UNICODE)
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging based on command line arguments."""
        logger = logging.getLogger('nomoemo')
        
        # Set base log level to DEBUG so all messages reach handlers
        logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        
        # Always add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Adjust console handler level based on quiet/verbose flags
        if self.args.quiet:
            console_handler.setLevel(logging.WARNING)
        else:
            console_handler.setLevel(logging.DEBUG if self.args.verbose else logging.INFO)
        
        logger.addHandler(console_handler)
        
        # Add file handler if --log is specified
        if self.args.log:
            try:
                file_handler = logging.FileHandler(self.args.log, mode='w', encoding='utf-8')
                file_handler.setFormatter(formatter)
                file_handler.setLevel(logging.DEBUG)  # Log everything to file
                logger.addHandler(file_handler)
                logger.debug(f"Logging to file: {self.args.log}")
            except (OSError, IOError) as e:
                # If we can't create the log file, warn but continue
                logger.warning(f"Could not create log file '{self.args.log}': {e}")
        
        return logger
    
    def run(self) -> int:
        """Main entry point for the application."""
        try:
            if not self.args.quiet:
                self.logger.info(f"nomoemo.py v.0.0.1 - by savan42")
            
            # Validate arguments
            if not self._validate_arguments():
                return 1
            
            # Process target path
            target_path = Path(self.args.target)
            if not target_path.exists():
                self.logger.error(f"Target path does not exist: {target_path}")
                return 1
            
            # Get list of files to process
            files_to_process = self._get_files_to_process(target_path)
            
            if not files_to_process:
                if not self.args.quiet:
                    self.logger.info("No files found to process.")
                return 0
            
            if not self.args.quiet:
                self.logger.info(f"Scanning for emoji...")
            
            # Process files based on mode
            if self.args.dry_run:
                return self._dry_run_mode(files_to_process)
            elif self.args.remove:
                return self._remove_mode(files_to_process)
            elif self.args.replace:
                return self._replace_mode(files_to_process)
            elif self.args.ascii_only:
                return self._ascii_only_mode(files_to_process)
            elif self.args.latin1_only:
                return self._latin1_only_mode(files_to_process)
            else:
                # Default to dry run if no action specified
                return self._dry_run_mode(files_to_process)
                
        except KeyboardInterrupt:
            if not self.args.quiet:
                self.logger.info("Operation cancelled by user.")
            return 130
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return 1
    
    def _validate_arguments(self) -> bool:
        """Validate command line arguments."""
        # Will be expanded in Task 10
        if self.args.replace and not self.args.replacement:
            self.logger.error("--replace requires --replacement argument")
            return False
        
        if self.args.replacement and not self.args.replace:
            self.logger.error("--replacement can only be used with --replace")
            return False
        
        # Validate replacement character
        if self.args.replacement:
            if len(self.args.replacement) != 1:
                self.logger.error("--replacement must be a single character")
                return False
            
            # Check if replacement character is ASCII
            if not self.args.replacement.isascii():
                self.logger.error("--replacement must be an ASCII character")
                return False
            
            # Check if replacement character is an emoji (would be counterproductive)
            if emoji.emoji_list(self.args.replacement):
                self.logger.error("--replacement cannot be an emoji character")
                return False
        
        return True
    
    def _get_files_to_process(self, target_path: Path) -> List[Path]:
        """Get list of files to process based on target path and options."""
        # Will be implemented in Task 4
        files = []
        
        if target_path.is_file():
            files.append(target_path)
        elif target_path.is_dir():
            if self.args.recursive:
                # Recursive directory traversal
                for file_path in target_path.rglob('*'):
                    if file_path.is_file() and self._should_process_file(file_path):
                        files.append(file_path)
            else:
                # Single directory level
                for file_path in target_path.iterdir():
                    if file_path.is_file() and self._should_process_file(file_path):
                        files.append(file_path)
        
        return files
    
    def _should_process_file(self, file_path: Path) -> bool:
        """Determine if a file should be processed."""
        # Skip files that are obviously not text
        if file_path.suffix.lower() in {'.exe', '.dll', '.so', '.dylib', '.bin', '.jpg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.zip', '.tar', '.gz', '.pdf'}:
            return False
        
        try:
            # Read first 1024 bytes to check for binary content
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                
                # Check for null bytes (common in binary files)
                if b'\x00' in chunk:
                    return False
                
                # Try to decode as UTF-8
                try:
                    chunk.decode('utf-8')
                    return True
                except UnicodeDecodeError:
                    # If it fails UTF-8 decoding, it's likely binary
                    return False
                    
        except (OSError, IOError):
            # Can't read the file, skip it
            return False
    
    def _dry_run_mode(self, files: List[Path]) -> int:
        """Execute dry run mode - scan and report without modifications."""
        if not self.args.quiet:
            self.logger.info("DRY RUN MODE - No files will be modified")
        
        for file_path in files:
            self._scan_file_for_emojis(file_path)
        
        self._print_summary()
        return 0
    
    def _remove_mode(self, files: List[Path]) -> int:
        """Execute remove mode - delete emojis from files."""
        if not self.args.force:
            if not self._confirm_action("Delete Emojis"):
                return 0
        
        # Process files for removal
        if not self.args.quiet:
            self.logger.info("REMOVE MODE - Emojis will be deleted")
        
        files_modified = 0
        total_emojis_removed = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Use emoji library to remove all emojis
                modified_content = emoji.replace_emoji(original_content, replace='')
                
                # Check if any emojis were actually removed
                emojis_removed = len(emoji.emoji_list(original_content))
                if emojis_removed > 0:
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    
                    files_modified += 1
                    total_emojis_removed += emojis_removed
                    
                    if self.args.verbose:
                        self.logger.info(f"[-] Removed {emojis_removed} emoji(s) from {file_path}")
                
                self.files_processed += 1
                
            except UnicodeDecodeError as e:
                self.logger.warning(f"Could not decode {file_path} as UTF-8: {e}")
            except Exception as e:
                self.logger.warning(f"Could not process {file_path}: {e}")
        
        if not self.args.quiet or total_emojis_removed > 0:
            self.logger.info(f"[+] Removed {total_emojis_removed} emojis from {files_modified} files.")
        return 0
    
    def _replace_mode(self, files: List[Path]) -> int:
        """Execute replace mode - replace emojis with specified character."""
        if not self.args.force:
            if not self._confirm_action(f"Replace Emojis with '{self.args.replacement}'"):
                return 0
        
        # Process files for replacement
        if not self.args.quiet:
            self.logger.info(f"REPLACE MODE - Emojis will be replaced with '{self.args.replacement}'")
        
        files_modified = 0
        total_emojis_replaced = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Use emoji library to replace all emojis with the specified character
                modified_content = emoji.replace_emoji(original_content, replace=self.args.replacement)
                
                # Check if any emojis were actually replaced
                emojis_replaced = len(emoji.emoji_list(original_content))
                if emojis_replaced > 0:
                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    
                    files_modified += 1
                    total_emojis_replaced += emojis_replaced
                    
                    if self.args.verbose:
                        self.logger.info(f"[-] Replaced {emojis_replaced} emoji(s) in {file_path}")
                
                self.files_processed += 1
                
            except UnicodeDecodeError as e:
                self.logger.warning(f"Could not decode {file_path} as UTF-8: {e}")
            except Exception as e:
                self.logger.warning(f"Could not process {file_path}: {e}")
        
        if not self.args.quiet or total_emojis_replaced > 0:
            self.logger.info(f"[+] Replaced {total_emojis_replaced} emojis in {files_modified} files.")
        return 0
    
    def _ascii_only_mode(self, files: List[Path]) -> int:
        """Execute ASCII-only mode - scan for non-ASCII characters."""
        if not self.args.quiet:
            self.logger.info("ASCII-ONLY MODE - Scanning for non-ASCII characters (codepoints > 127)")
        
        for file_path in files:
            self._scan_file_for_charset_violations(file_path, 'ascii')
        
        self._print_charset_summary('ascii')
        return 0
    
    def _latin1_only_mode(self, files: List[Path]) -> int:
        """Execute Latin-1-only mode - scan for extended Unicode characters."""
        if not self.args.quiet:
            self.logger.info("LATIN1-ONLY MODE - Scanning for extended Unicode characters (codepoints > 255)")
        
        for file_path in files:
            self._scan_file_for_charset_violations(file_path, 'latin1')
        
        self._print_charset_summary('latin1')
        return 0
    
    def _scan_file_for_emojis(self, file_path: Path):
        """Scan a single file for emojis and catalog findings."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use emoji library to find all emojis in the file
            emoji_matches = emoji.emoji_list(content)
            
            if emoji_matches:
                self.files_with_emojis += 1
                self.emoji_count += len(emoji_matches)
                
                # For dry-run mode, report findings
                if self.args.dry_run:
                    self.logger.info(f"[-] Found {len(emoji_matches)} emoji(s) in {file_path}")
                    
                    # Show details if verbose
                    if self.args.verbose:
                        for match in emoji_matches:
                            # Calculate line and column numbers
                            line_num = content[:match['match_start']].count('\n') + 1
                            line_start = content.rfind('\n', 0, match['match_start']) + 1
                            col_num = match['match_start'] - line_start + 1
                            
                            # Get context around the emoji (avoid printing emoji chars)
                            context_start = max(0, match['match_start'] - 20)
                            context_end = min(len(content), match['match_end'] + 20)
                            context = content[context_start:context_end]
                            # Replace newlines and the emoji itself for clean display
                            context = context.replace('\n', ' ').replace(content[match['match_start']:match['match_end']], '[EMOJI]')
                            
                            self.logger.info(f"  Line {line_num}, Col {col_num}: {context}")
            
            self.files_processed += 1
            
        except UnicodeDecodeError as e:
            self.logger.warning(f"Could not decode {file_path} as UTF-8: {e}")
        except Exception as e:
            self.logger.warning(f"Could not process {file_path}: {e}")
    
    def _scan_file_for_charset_violations(self, file_path: Path, charset: str):
        """Scan a single file for character set violations and catalog findings."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine the codepoint limit based on charset
            if charset == 'ascii':
                max_codepoint = 127
                violation_desc = "non-ASCII"
            elif charset == 'latin1':
                max_codepoint = 255
                violation_desc = "extended Unicode"
            else:
                raise ValueError(f"Unknown charset: {charset}")
            
            violations_found = []
            
            # Scan each character for violations
            for i, char in enumerate(content):
                codepoint = ord(char)
                if codepoint > max_codepoint:
                    # Calculate line and column numbers
                    line_num = content[:i].count('\n') + 1
                    line_start = content.rfind('\n', 0, i) + 1
                    col_num = i - line_start + 1
                    
                    violations_found.append((i, char, codepoint, line_num, col_num))
                    self.charset_violations.append((file_path, char, codepoint, line_num, col_num))
            
            if violations_found:
                self.files_with_charset_violations += 1
                
                # Report findings
                self.logger.info(f"[-] Found {len(violations_found)} {violation_desc} character(s) in {file_path}")
                
                # Show details if verbose
                if self.args.verbose:
                    for i, char, codepoint, line_num, col_num in violations_found:
                        # Get context around the character
                        context_start = max(0, i - 20)
                        context_end = min(len(content), i + 21)  # +1 for the character itself
                        context = content[context_start:context_end]
                        # Replace newlines and the violating character for clean display
                        context = context.replace('\n', ' ').replace(char, f'[U+{codepoint:04X}]')
                        
                        self.logger.info(f"  Line {line_num}, Col {col_num}: U+{codepoint:04X} '{char}' - {context}")
            
            self.files_processed += 1
            
        except UnicodeDecodeError as e:
            self.logger.warning(f"Could not decode {file_path} as UTF-8: {e}")
        except Exception as e:
            self.logger.warning(f"Could not process {file_path}: {e}")
    
    def _confirm_action(self, action: str) -> bool:
        """Prompt user for confirmation of destructive actions."""
        # Will be implemented in Task 8
        try:
            response = input(f"[?] {action}? (y/N) ")
            if response.lower() != 'y':
                return False
            
            response = input("[!] Are you SURE? (y/N) Press Y to confirm! ")
            return response.lower() == 'y'
            
        except (EOFError, KeyboardInterrupt):
            return False
    
    def _print_summary(self):
        """Print operation summary."""
        if not self.args.quiet:
            self.logger.info(f"[+] Total: {self.emoji_count} emojis in {self.files_with_emojis} files.")
            self.logger.info(f"[*] Processed {self.files_processed} files.")
        elif self.emoji_count > 0:
            # In quiet mode, only show summary if emojis were found (use warning level to show)
            self.logger.warning(f"[+] Total: {self.emoji_count} emojis in {self.files_with_emojis} files.")
    
    def _print_charset_summary(self, charset: str):
        """Print character set violation summary."""
        if charset == 'ascii':
            violation_desc = "non-ASCII characters (codepoints > 127)"
            limit_desc = "ASCII-only"
        elif charset == 'latin1':
            violation_desc = "extended Unicode characters (codepoints > 255)"
            limit_desc = "Latin-1-only"
        else:
            raise ValueError(f"Unknown charset: {charset}")
        
        if not self.args.quiet:
            self.logger.info(f"[+] Total: {len(self.charset_violations)} {violation_desc} in {self.files_with_charset_violations} files.")
            self.logger.info(f"[*] Processed {self.files_processed} files.")
            
            # Show character set compliance status
            if self.files_with_charset_violations == 0:
                self.logger.info(f"[✓] All files are {limit_desc} compliant.")
            else:
                self.logger.warning(f"[!] {self.files_with_charset_violations} files contain {violation_desc}.")
        elif len(self.charset_violations) > 0:
            # In quiet mode, only show summary if violations were found (use warning level to show)
            self.logger.warning(f"[+] Total: {len(self.charset_violations)} {violation_desc} in {self.files_with_charset_violations} files.")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="NoMoEmo - Eliminate emojis from code files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  Basic usage:
    nomoemo.py --dry-run file.py                    # Scan single file
    nomoemo.py --dry-run --recursive ./src/        # Scan directory recursively
    nomoemo.py --dry-run --verbose ./project/      # Detailed scan with locations

  Removal operations:
    nomoemo.py --remove file.py                     # Remove with confirmation
    nomoemo.py --remove --force file.py            # Remove without confirmation
    nomoemo.py --remove --recursive ./src/         # Remove from directory tree

  Replacement operations:
    nomoemo.py --replace --replacement "*" file.py # Replace with asterisks
    nomoemo.py --replace --replacement "X" --recursive ./src/  # Replace recursively

  Character set checking:
    nomoemo.py --ascii-only file.py                 # Check for non-ASCII chars
    nomoemo.py --latin1-only --recursive ./src/    # Check for extended Unicode
    nomoemo.py --ascii-only --verbose ./project/   # Detailed non-ASCII scan

  CI/CD and automation:
    nomoemo.py --dry-run --quiet --recursive ./    # Silent scan for CI
    nomoemo.py --remove --force --quiet ./src/     # Silent removal for automation

  Logging and output:
    nomoemo.py --dry-run --log scan.log ./src/     # Log to file
    nomoemo.py --dry-run --verbose ./src/          # Detailed console output
    nomoemo.py --dry-run --quiet ./src/            # Minimal output

EXIT CODES:
  0  Success - no errors, emojis processed as requested
  1  Error - invalid arguments, file access issues, or processing errors
  130  User cancelled - operation aborted by user (Ctrl+C)

NOTES:
  - Default mode is --dry-run if no action is specified
  - Use --force to skip confirmation prompts for destructive operations
  - Binary files are automatically detected and skipped
  - Only UTF-8 encoded text files are processed
  - Hidden files and directories (starting with .) are processed
        """
    )
    
    # Positional argument
    parser.add_argument(
        'target',
        help='File or directory to process'
    )
    
    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--dry-run',
        action='store_true',
        help='Scan and report emojis without modifying files (default mode)'
    )
    mode_group.add_argument(
        '--remove',
        action='store_true',
        help='Remove all emoji characters from files (destructive - prompts for confirmation unless --force is used)'
    )
    mode_group.add_argument(
        '--replace',
        action='store_true',
        help='Replace emojis with specified character (requires --replacement)'
    )
    mode_group.add_argument(
        '--ascii-only',
        action='store_true',
        help='Scan for non-ASCII characters (codepoints > 127) without modifying files'
    )
    mode_group.add_argument(
        '--latin1-only',
        action='store_true',
        help='Scan for extended Unicode characters (codepoints > 255) without modifying files'
    )
    
    # Options
    parser.add_argument(
        '--replacement',
        metavar='CHAR',
        help='Single ASCII character to replace emojis with (required when using --replace)'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Process directories recursively (process all subdirectories)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts for destructive operations (--remove, --replace)'
    )
    
    # Logging options
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress most output (only show warnings and final summary if emojis found)'
    )
    log_group.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output (show detailed progress and emoji locations)'
    )
    
    parser.add_argument(
        '--log',
        metavar='FILE',
        help='Log all output to specified file (in addition to console output)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.0.1'
    )
    
    return parser


def main() -> int:
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Default to dry-run if no mode specified
    if not (args.dry_run or args.remove or args.replace or args.ascii_only or args.latin1_only):
        args.dry_run = True
    
    app = NoMoEmo(args)
    return app.run()


if __name__ == '__main__':
    sys.exit(main())