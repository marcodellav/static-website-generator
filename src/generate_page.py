import os
from block_markdown import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf8') as source:
        md = source.read()
    with open(template_path, 'r', encoding='utf8') as template:
        html_template = template.read()
    node = markdown_to_html_node(md)
    html_node = node.to_html()
    title = extract_title(md)
    html_page_with_title = html_template.replace("{{ Title }}", title)
    html_page_with_title_and_content = html_page_with_title.replace("{{ Content }}", html_node)
    dest_dir = os.path.dirname(dest_path)

    if not os.path.exists(dest_dir):
        print(f"destination path {dest_path} doesn't exist, creating...")
        os.makedirs(dest_dir)
    with open(dest_path,'w', encoding='utf8') as index:
        index.write(html_page_with_title_and_content)
