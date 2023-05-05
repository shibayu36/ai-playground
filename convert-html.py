import html2text


def convert_html_to_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # HTMLをテキストに変換
    text_converter = html2text.HTML2Text()
    text_converter.ignore_links = True
    text_content = text_converter.handle(html_content)

    return text_content


# 使用例
html_file_path = "./hoge.html"
text_content = convert_html_to_text(html_file_path)

print(text_content)
