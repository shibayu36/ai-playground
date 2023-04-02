import html2text
from pathlib import Path
from pprint import pprint
from llama_index import GPTSimpleVectorIndex, download_loader
from dotenv import load_dotenv

load_dotenv()

MarkdownReader = download_loader("MarkdownReader")

loader = MarkdownReader()
documents = loader.load_data(
    file=Path('./README.md'), extra_info={'path': './README.md'})

pprint(documents, indent=2, width=30, depth=None, sort_dicts=False)

index = GPTSimpleVectorIndex.from_documents(documents)
response = index.query("aaaとは何？")
pprint(response.source_nodes[0])
