from pprint import pprint
import re
from collections import defaultdict


def parse_movable_type_entry(entry_text):
    entry_data = defaultdict(lambda: None)
    # MTフォーマットからTITLE, BODY, EXTENDED BODYを抜き出す
    title_pattern = re.compile(
        r"^TITLE:\s*(.+)$",
        re.MULTILINE
    )
    entry_data['title'] = title_pattern.search(entry_text).group(1)

    body_pattern = re.compile(
        r"^BODY:\s*(.+?)\n-----",
        re.DOTALL | re.MULTILINE
    )
    entry_data['body'] = body_pattern.search(entry_text).group(1)

    extended_body_pattern = re.compile(
        r"^BODY:\s*(.+?)\n-----",
        re.DOTALL | re.MULTILINE
    )
    extended_body_match = extended_body_pattern.search(entry_text).group(1)
    if extended_body_match is not None:
        entry_data['body'] += extended_body_match

    return entry_data


def extract_entries_from_movable_type(movable_type_text):
    entry_texts = re.split(r"(?m)^--------\n", movable_type_text)
    entry_texts.pop()

    entries = [parse_movable_type_entry(entry_text)
               for entry_text in entry_texts]

    return entries


with open('/Users/yuki.shibazaki/Downloads/blog.shibayu36.org.export.txt', "r", encoding="utf-8") as file:
    content = file.read()

entries = extract_entries_from_movable_type(content)
