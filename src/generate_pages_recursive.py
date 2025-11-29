import os
from generate_page import generate_page
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    entries = os.listdir (dir_path_content)
    starting_dest_dir_path = dest_dir_path
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path):
            entry_html = entry.replace("md", "html")
            dest_dir_path = os.path.join(dest_dir_path, entry_html)
            generate_page( entry_path, "template.html", dest_dir_path)
        else:
            dest_dir_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, dest_dir_path)
            dest_dir_path = starting_dest_dir_path
