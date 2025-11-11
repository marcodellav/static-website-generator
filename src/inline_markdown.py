import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue
        if delimiter not in n.text:
            new_nodes.append(n)
            continue
        parts = n.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception ("invalid markdown, missing closing delimiter")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # If there are no images or links respectively, just return a list with the original TextNode in it
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Don't append any TextNodes that have empty text to the final list
        if old_node.text == "":
            continue
        images = []
        sections = []
        remaining_text = old_node.text
        for i, image in enumerate(extract_markdown_images(old_node.text)):
            image_alt = image[0]
            image_link = image[1]
            if remaining_text.split(f"![{image_alt}]({image_link})", 1)[0] == "":
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            else:
                new_nodes.append(TextNode(remaining_text.split(f"![{image_alt}]({image_link})", 1)[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            remaining_text = (remaining_text.split(f"![{image_alt}]({image_link})", 1)[1])
        if len(remaining_text) != 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # If there are no images or links respectively, just return a list with the original TextNode in it
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Don't append any TextNodes that have empty text to the final list
        if old_node.text == "":
            continue
        images = []
        sections = []
        remaining_text = old_node.text
        for i, link in enumerate(extract_markdown_links(old_node.text)):
            link_text = link[0]
            link_link = link[1]
            if remaining_text.split(f"[{link_text}]({link_link})", 1)[0] == "":
                new_nodes.append(TextNode(link_text, TextType.LINK, link_link))
            else:
                new_nodes.append(TextNode(remaining_text.split(f"[{link_text}]({link_link})", 1)[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_link))
            remaining_text = (remaining_text.split(f"[{link_text}]({link_link})", 1)[1])
        if len(remaining_text) != 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
