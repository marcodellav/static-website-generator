import os
from block_markdown import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path, base_path):
    print (f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf8') as source:
        md = source.read()
    with open(template_path, 'r', encoding='utf8') as template:
        html_template = template.read()
    node = markdown_to_html_node(md)
    html_node = node.to_html()
    title = extract_title(md)
    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", html_node)
    html_template = html_template.replace('href="/', f'href="{base_path}')
    html_template = html_template.replace('src="/', f'src="{base_path}')
    dest_dir = os.path.dirname(dest_path)

    if not os.path.exists(dest_dir):
        print(f"destination path {dest_path} doesn't exist, creating...")
        os.makedirs(dest_dir)
    with open(dest_path,'w', encoding='utf8') as index:
        index.write(html_template)
