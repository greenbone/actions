# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence
from typing import Dict

import shtab
import time
import subprocess
import os
import re

HIDDEN_MARKERS: Dict[str, str] = {
    # Zero Width Characters
    '\u200B': "Zero Width Space (U+200B)",
    '\u200C': "Zero Width Non-Joiner (U+200C)",
    '\u200D': "Zero Width Joiner (U+200D)",
    '\u2060': "Word Joiner (U+2060)",
    '\uFEFF': "Byte Order Mark (BOM) / Zero Width No-Break Space (U+FEFF)",

    # Common Non-Standard Spaces
    '\u00A0': "Non-Breaking Space (U+00A0)",
    '\u202F': "Narrow No-Break Space (U+202F)",

    # Other Fixed-Width or Special Spaces
    '\u2000': "En Quad (U+2000)",
    '\u2001': "Em Quad (U+2001)",
    '\u2002': "En Space (U+2002)",
    '\u2003': "Em Space (U+2003)",
    '\u2004': "Three-Per-Em Space (U+2004)",
    '\u2005': "Four-Per-Em Space (U+2005)",
    '\u2006': "Six-Per-Em Space (U+2006)",
    '\u2007': "Figure Space (U+2007)",
    '\u2008': "Punctuation Space (U+2008)",
    '\u2009': "Thin Space (U+2009)",
    '\u200A': "Hair Space (U+200A)",
    '\u205F': "Medium Mathematical Space (U+205F)",
    '\u3000': "Ideographic Space (U+3000)",

    # Other Invisible or Control-like Characters
    '\u180E': "Mongolian Vowel Separator (U+180E)",
    '\u034F': "Combining Grapheme Joiner (U+034F)",
    '\u00AD': "Soft Hyphen (U+00AD)",

    # Directional Formatting Characters
    '\u200E': "Left-to-Right Mark (U+200E)",
    '\u200F': "Right-to-Left Mark (U+200F)",
    '\u202A': "Left-to-Right Embedding (U+202A)",
    '\u202B': "Right-to-Left Embedding (U+202B)",
    '\u202C': "Pop Directional Formatting (U+202C)",
    '\u202D': "Left-to-Right Override (U+202D)",
    '\u202E': "Right-to-Left Override (U+202E)",
    '\u2061': "Function Application (U+2061)",
    '\u2062': "Invisible Times (U+2062)",
    '\u2063': "Invisible Separator (U+2063)",
    '\u2064': "Invisible Plus (U+2064)",
    '\u2066': "Left-to-Right Isolate (U+2066)",
    '\u2067': "Right-to-Left Isolate (U+2067)",
    '\u2068': "First Strong Isolate (U+2068)",
    '\u2069': "Pop Directional Isolate (U+2069)",

    # Variation Selectors
    '\uFE00': "Variation Selector-1 (U+FE00)",
    '\uFE01': "Variation Selector-2 (U+FE01)",
    '\uFE02': "Variation Selector-3 (U+FE02)",
    '\uFE03': "Variation Selector-4 (U+FE03)",
    '\uFE04': "Variation Selector-5 (U+FE04)",
    '\uFE05': "Variation Selector-6 (U+FE05)",
    '\uFE06': "Variation Selector-7 (U+FE06)",
    '\uFE07': "Variation Selector-8 (U+FE07)",
    '\uFE08': "Variation Selector-9 (U+FE08)",
    '\uFE09': "Variation Selector-10 (U+FE09)",
    '\uFE0A': "Variation Selector-11 (U+FE0A)",
    '\uFE0B': "Variation Selector-12 (U+FE0B)",
    '\uFE0C': "Variation Selector-13 (U+FE0C)",
    '\uFE0D': "Variation Selector-14 (U+FE0D)",
    '\uFE0E': "Variation Selector-15 (U+FE0E)",
    '\uFE0F': "Variation Selector-16 (U+FE0F)",

    # Mongolian Free Variation Selectors
    '\u180B': "Mongolian Free Variation Selector One (FVS1, U+180B)",
    '\u180C': "Mongolian Free Variation Selector Two (FVS2, U+180C)",
    '\u180D': "Mongolian Free Variation Selector Three (FVS3, U+180D)",
}

HIDDEN_IDEOGRAPHIC_MARKERS: Dict[str, str] = {
    # Ideographic Variation Selectors
    chr(i): f"Ideographic Variation Selector-{17 + (i - 0xE0100)} (VS{17 + (i - 0xE0100)}, U+{i:05X})"
    for i in range(0xE0100, 0xE01EF + 1)
}

HIDDEN_TAG_MARKERS: Dict[str, str] = {
    '\U000E0001': "LANGUAGE TAG (U+E0001)",
    '\U000E0020': "TAG SPACE U+E0020 (U+E0020)",
    '\U000E0021': "TAG EXCLAMATION MARK (U+E0021)",
    '\U000E0022': "TAG QUOTATION MARK (U+E0022)",
    '\U000E0023': "TAG NUMBER SIGN (U+E0023)",
    '\U000E0024': "TAG DOLLAR SIGN (U+E0024)",
    '\U000E0025': "TAG PERCENT SIGN (U+E0025)",
    '\U000E0026': "TAG AMPERSAND (U+E0026)",
    '\U000E0027': "TAG APOSTROPHE (U+E0027)",
    '\U000E0028': "TAG LEFT PARENTHESIS (U+E0028)",
    '\U000E0029': "TAG RIGHT PARENTHESIS (U+E0029)",
    '\U000E002A': "TAG ASTERISK (U+E002A)",
    '\U000E002B': "TAG PLUS SIGN (U+E002B)",
    '\U000E002C': "TAG COMMA (U+E002C)",
    '\U000E002D': "TAG HYPHEN-MINUS (U+E002D)",
    '\U000E002E': "TAG FULL STOP (U+E002E)",
    '\U000E002F': "TAG SOLIDUS (U+E002F)",
    '\U000E0030': "TAG DIGIT ZERO (U+E0030)",
    '\U000E0031': "TAG DIGIT ONE (U+E0031)",
    '\U000E0032': "TAG DIGIT TWO (U+E0032)",
    '\U000E0033': "TAG DIGIT THREE (U+E0033)",
    '\U000E0034': "TAG DIGIT FOUR (U+E0034)",
    '\U000E0035': "TAG DIGIT FIVE (U+E0035)",
    '\U000E0036': "TAG DIGIT SIX (U+E0036)",
    '\U000E0037': "TAG DIGIT SEVEN (U+E0037)",
    '\U000E0038': "TAG DIGIT EIGHT (U+E0038)",
    '\U000E0039': "TAG DIGIT NINE (U+E0039)",
    '\U000E003A': "TAG COLON (U+E003A)",
    '\U000E003B': "TAG SEMICOLON (U+E003B)",
    '\U000E003C': "TAG LESS-THAN SIGN (U+E003C)",
    '\U000E003D': "TAG EQUALS SIGN (U+E003D)",
    '\U000E003E': "TAG GREATER-THAN SIGN (U+E003E)",
    '\U000E003F': "TAG QUESTION MARK (U+E003F)",
    '\U000E0040': "TAG COMMERCIAL AT (U+E0040)",
    '\U000E0041': "TAG LATIN CAPITAL LETTER A (U+E0041)",
    '\U000E0042': "TAG LATIN CAPITAL LETTER B (U+E0042)",
    '\U000E0043': "TAG LATIN CAPITAL LETTER C (U+E0043)",
    '\U000E0044': "TAG LATIN CAPITAL LETTER D (U+E0044)",
    '\U000E0045': "TAG LATIN CAPITAL LETTER E (U+E0045)",
    '\U000E0046': "TAG LATIN CAPITAL LETTER F (U+E0046)",
    '\U000E0047': "TAG LATIN CAPITAL LETTER G (U+E0047)",
    '\U000E0048': "TAG LATIN CAPITAL LETTER H (U+E0048)",
    '\U000E0049': "TAG LATIN CAPITAL LETTER I (U+E0049)",
    '\U000E004A': "TAG LATIN CAPITAL LETTER J (U+E004A)",
    '\U000E004B': "TAG LATIN CAPITAL LETTER K (U+E004B)",
    '\U000E004C': "TAG LATIN CAPITAL LETTER L (U+E004C)",
    '\U000E004D': "TAG LATIN CAPITAL LETTER M (U+E004D)",
    '\U000E004E': "TAG LATIN CAPITAL LETTER N (U+E004E)",
    '\U000E004F': "TAG LATIN CAPITAL LETTER O (U+E004F)",
    '\U000E0050': "TAG LATIN CAPITAL LETTER P (U+E0050)",
    '\U000E0051': "TAG LATIN CAPITAL LETTER Q (U+E0051)",
    '\U000E0052': "TAG LATIN CAPITAL LETTER R (U+E0052)",
    '\U000E0053': "TAG LATIN CAPITAL LETTER S (U+E0053)",
    '\U000E0054': "TAG LATIN CAPITAL LETTER T (U+E0054)",
    '\U000E0055': "TAG LATIN CAPITAL LETTER U (U+E0055)",
    '\U000E0056': "TAG LATIN CAPITAL LETTER V (U+E0056)",
    '\U000E0057': "TAG LATIN CAPITAL LETTER W (U+E0057)",
    '\U000E0058': "TAG LATIN CAPITAL LETTER X (U+E0058)",
    '\U000E0059': "TAG LATIN CAPITAL LETTER Y (U+E0059)",
    '\U000E005A': "TAG LATIN CAPITAL LETTER Z (U+E005A)",
    '\U000E005B': "TAG LEFT SQUARE BRACKET (U+E005B)",
    '\U000E005C': "TAG REVERSE SOLIDUS (U+E005C)",
    '\U000E005D': "TAG RIGHT SQUARE BRACKET (U+E005D)",
    '\U000E005E': "TAG CIRCUMFLEX ACCENT (U+E005E)",
    '\U000E005F': "TAG LOW LINE (U+E005F)",
    '\U000E0060': "TAG GRAVE ACCENT (U+E0060)",
    '\U000E0061': "TAG LATIN SMALL LETTER A (U+E0061)",
    '\U000E0062': "TAG LATIN SMALL LETTER B (U+E0062)",
    '\U000E0063': "TAG LATIN SMALL LETTER C (U+E0063)",
    '\U000E0064': "TAG LATIN SMALL LETTER D (U+E0064)",
    '\U000E0065': "TAG LATIN SMALL LETTER E (U+E0065)",
    '\U000E0066': "TAG LATIN SMALL LETTER F (U+E0066)",
    '\U000E0067': "TAG LATIN SMALL LETTER G (U+E0067)",
    '\U000E0068': "TAG LATIN SMALL LETTER H (U+E0068)",
    '\U000E0069': "TAG LATIN SMALL LETTER I (U+E0069)",
    '\U000E006A': "TAG LATIN SMALL LETTER J (U+E006A)",
    '\U000E006B': "TAG LATIN SMALL LETTER K (U+E006B)",
    '\U000E006C': "TAG LATIN SMALL LETTER L (U+E006C)",
    '\U000E006D': "TAG LATIN SMALL LETTER M (U+E006D)",
    '\U000E006E': "TAG LATIN SMALL LETTER N (U+E006E)",
    '\U000E006F': "TAG LATIN SMALL LETTER O (U+E006F)",
    '\U000E0070': "TAG LATIN SMALL LETTER P (U+E0070)",
    '\U000E0071': "TAG LATIN SMALL LETTER Q (U+E0071)",
    '\U000E0072': "TAG LATIN SMALL LETTER R (U+E0072)",
    '\U000E0073': "TAG LATIN SMALL LETTER S (U+E0073)",
    '\U000E0074': "TAG LATIN SMALL LETTER T (U+E0074)",
    '\U000E0075': "TAG LATIN SMALL LETTER U (U+E0075)",
    '\U000E0076': "TAG LATIN SMALL LETTER V (U+E0076)",
    '\U000E0077': "TAG LATIN SMALL LETTER W (U+E0077)",
    '\U000E0078': "TAG LATIN SMALL LETTER X (U+E0078)",
    '\U000E0079': "TAG LATIN SMALL LETTER Y (U+E0079)",
    '\U000E007A': "TAG LATIN SMALL LETTER Z (U+E007A)",
    '\U000E007B': "TAG LEFT CURLY BRACKET (U+E007B)",
    '\U000E007C': "TAG VERTICAL LINE (U+E007C)",
    '\U000E007D': "TAG RIGHT CURLY BRACKET (U+E007D)",
    '\U000E007E': "TAG TILDE (U+E007E)",
    '\U000E007F': "CANCEL TAG (U+E007F)",
}

def parse_args(args: Optional[Sequence[str]] = None) -> Namespace:
   parser = ArgumentParser()
   shtab.add_argument_to(parser)

   input_group = parser.add_mutually_exclusive_group(required=True)
   input_group.add_argument("repopath", help="Path to local git repository", nargs="?")
   input_group.add_argument("--file", help="Path to a single file to scan", nargs="?")

   parser.add_argument("--filter", help="Regex all changed files are filtered by", default="")
   parser.add_argument("--log_level", help="Configure the logging level", default="WARNING")

   parser.add_argument("--hide_scan_details", action='store_true')

   parsed_args = parser.parse_args(args)

   if parsed_args.filter and not parsed_args.repopath:
       parser.error("--filter can only be used with --repopath")

   if parsed_args.log_level not in ["NONE", "WARNING", "DEBUG"]:
       parser.error("--log_level isn't NONE, WARNING or DEBUG")

   return parsed_args

def get_changed_files_and_apply_filter(args: list[str], commitA: str ="HEAD^1", commitB: str ="HEAD") -> int:
   os.chdir(args.repopath)
   changed_files = subprocess.run(["git", "diff", "--name-only", commitA, commitB, "--", args.repopath], capture_output=True, text=True).stdout.splitlines()

   if args.filter != "":
     regex = re.compile(args.filter)
     changed_files = [ c_file for c_file in changed_files if regex.match(c_file) ]

   return changed_files

def print_and_store(msg: str, pr_comment: list[str]):
  print(f"{msg}")
  pr_comment.append(msg)

def print_marker(pr_comment: list[str], log_level: str, hide_scan_details: bool, desc: str, line_nr: int, column_nr: int, file_path: str, detected_markers: int) -> int:
   if not hide_scan_details:
      if detected_markers == 0:
         print_and_store("```", pr_comment)
      print_and_store(f"{desc}, found at line {line_nr} and column {column_nr} in file {file_path}", pr_comment)
   detected_markers += 1
   return detected_markers

def shrink_pr_comment(pr_comment: list[str]):
   ## Delete until last '## Scan:' or '# Scan:' section
   while True:
      curElement = pr_comment.pop()
      if "## Scan:" in curElement or len(pr_comment) == 1:
         break

def scan_file(pr_comment: list[str], log_level: str, hide_scan_details: bool, file_path: str) -> int:
   start_time = time.perf_counter()
   detected_markers = 0
   line_nr = 0
   column_nr = 0

   with open(file_path, encoding="utf-8") as fileobj:
       for line in fileobj:
           line_nr += 1
           column_nr = 0
           for current_char in line:
               column_nr += 1
               if current_char in HIDDEN_MARKERS:
                   detected_markers = print_marker(pr_comment, log_level, hide_scan_details, HIDDEN_MARKERS[current_char], line_nr, column_nr, file_path, detected_markers)
               elif current_char in HIDDEN_IDEOGRAPHIC_MARKERS:
                   detected_markers = print_marker(pr_comment, log_level, hide_scan_details, HIDDEN_IDEOGRAPHIC_MARKERS[current_char], line_nr, column_nr, file_path, detected_markers)
               elif current_char in HIDDEN_TAG_MARKERS:
                   detected_markers = print_marker(pr_comment, log_level, hide_scan_details, HIDDEN_TAG_MARKERS[current_char], line_nr, column_nr, file_path, detected_markers)

   end_time = time.perf_counter()
   elapsed_time = end_time - start_time

   if detected_markers == 0:
       print_and_store(f"Nothing detected in {file_path}", pr_comment)
   else:
       if not hide_scan_details:
          print_and_store("```", pr_comment)
       print_and_store(f"{detected_markers} hidden markers detected in {file_path}", pr_comment)
   print_and_store(f"Scan took {elapsed_time:.2f} seconds", pr_comment)

   if detected_markers == 0 and log_level == "WARNING":
      shrink_pr_comment(pr_comment)

   return detected_markers

def scan_multiple_changed_files(pr_comment: list[str], log_level: str, hide_scan_details: bool, changed_files: list[str]):
   detected_markers = 0

   print_and_store("# Scanning the following files for hidden unicode:", pr_comment)
   for cur_file in changed_files:
      print_and_store(f"`{cur_file.strip()}`", pr_comment)

   print_and_store("", pr_comment)
   for cur_file in changed_files:
      cur_file = cur_file.strip()
      print_and_store(f"## Scanning the following file for hidden unicode: '{cur_file}'", pr_comment)
      detected_markers += scan_file(pr_comment, log_level, hide_scan_details, cur_file)

   return detected_markers

def scan_single_changed_file(pr_comment: list[str], log_level: str, hide_scan_details: bool, changed_file: str):
   stripped_file = changed_file.strip()
   print_and_store(f"# Scan: '{stripped_file}'", pr_comment)
   return scan_file(pr_comment, log_level, hide_scan_details, stripped_file)

def scan_changed_files(pr_comment: list[str], log_level: str, hide_scan_details: bool, changed_files: list[str]):
   file_count = len(changed_files)

   if file_count > 1:
      return scan_multiple_changed_files(pr_comment, log_level, hide_scan_details, changed_files)

   elif file_count == 1:
      return scan_single_changed_file(pr_comment, log_level, hide_scan_details, changed_files[0])

   return 0

def write_to_file(content: list[str], filename: str):
  with open(filename, "w", encoding="utf-8") as file_opened:
     for line in content:
        file_opened.write(line + "\n")

def main():
   detected_markers = 0
   pr_comment = []

   args = parse_args()

   if args.file:
       detected_markers = scan_file(pr_comment, args.log_level, args.hide_scan_details, args.file)
   else:
       changed_files = get_changed_files_and_apply_filter(args)
       detected_markers = scan_changed_files(pr_comment, args.log_level, args.hide_scan_details, changed_files)

   if (detected_markers != 0 and args.log_level == "WARNING") or args.log_level == "DEBUG":
     write_to_file(pr_comment, "PR_COMMENT.md")

if __name__ == "__main__":
    main()
