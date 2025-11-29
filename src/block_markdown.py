from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes, split_nodes_delimiter
from textnode import text_node_to_html_node, TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

'''
function that works for all block types.
It takes a string of text and returns a list of HTMLNodes that represent the inline markdown
using previously created functions (think TextNode -> HTMLNode).
'''
def text_to_children(text):
    list_of_text_nodes = text_to_textnodes(text)
    list_of_html_nodes = []
    for text_node in list_of_text_nodes:
        text_node.text = text_node.text.replace("\n", " ")
        list_of_html_nodes.append(text_node_to_html_node(text_node))
    return list_of_html_nodes

def text_to_olist_items(text):
    items = text.split("\n")
    html_items = []
    for item in items:
        text_item = item [3:]
        children = text_to_children(text_item)
        html_items.append(ParentNode("li", children))
    return html_items

def text_to_ulist_items(text):
    items = text.split("\n")
    html_items = []
    for item in items:
        text_item = item [2:]
        children = text_to_children(text_item)
        html_items.append(ParentNode("li", children))
    return html_items

def text_to_quote_items(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return children

def markdown_to_html_node(markdown):
    # Split the markdown into blocks
    grandchildren_nodes = []
    children_nodes = []
    blocks = markdown_to_blocks(markdown)
    # Loop over each block
    for block in blocks:
        block_type = block_to_block_type(block)
        # Based on the type of block, create a new HTMLNode with the proper data
        if block_type == BlockType.PARAGRAPH:
            leaf_node = text_to_children(block)
            children_nodes.append(ParentNode("p", leaf_node))
        if block_type == BlockType.HEADING:
            i = block.count('#')
            heading_node = text_to_children(block)
            for item in heading_node:
                item.value = item.value.lstrip("#")
                item.value = item.value.lstrip(" ")
            children_nodes.append(ParentNode(f"h{i}", heading_node))
        if block_type == BlockType.CODE:
            text_node = TextNode(block, TextType.CODE)
            text_node.text = text_node.text.strip("```")
            text_node.text = text_node.text.lstrip("\n")
            html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("pre", [html_node])
            children_nodes.append(code_node)
        if block_type == BlockType.QUOTE:
            leaf_node = text_to_quote_items(block)
            children_nodes.append(ParentNode("blockquote", leaf_node))
        if block_type == BlockType.ULIST:
            list_nodes = text_to_ulist_items(block)
            for list_node in list_nodes:
                list_node.value = f"<li>{list_node.value}</li>"
            children_nodes.append(ParentNode("ul", list_nodes))
        if block_type == BlockType.OLIST:
            list_nodes = text_to_olist_items(block)
            for list_node in list_nodes:
                list_node.value = f"<li>{list_node.value}</li>"
            children_nodes.append(ParentNode("ol", list_nodes))
    parent_node = ParentNode("div", children_nodes)
    return parent_node
