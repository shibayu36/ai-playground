import pdb
from http.client import HTTPConnection  # py3
import logging
from pprint import pprint
import re
from collections import defaultdict
from html2text import html2text
from llama_index import Document, GPTSimpleVectorIndex, download_loader
from dotenv import load_dotenv


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
    entry_texts.pop()  # Delete last empty entry

    entries = [parse_movable_type_entry(entry_text)
               for entry_text in entry_texts]

    return entries


load_dotenv()

with open('/Users/yuki.shibazaki/Downloads/blog.shibayu36.org.export.txt', "r", encoding="utf-8") as file:
    content = file.read()

entries = extract_entries_from_movable_type(content)


log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)

# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# print statements from `http.client.HTTPConnection` to console/stdout
HTTPConnection.debuglevel = 1

# index = GPTSimpleVectorIndex.load_from_disk('index.json')
# for entry in entries:
#     print(entry['title'])
#     doc = Document(
#         html2text(entry['body']),
#         extra_info={'title': entry['title']}
#     )
#     index.insert(doc)
#     index.save_to_disk('index.json')

index = GPTSimpleVectorIndex.load_from_disk('index.json')
pdb.set_trace()
response = index.query("YAPCとは何？")
print(response)
for node in response.source_nodes:
    print(node.node.extra_info['title'])
