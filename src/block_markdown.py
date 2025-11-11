from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if (block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        counter = 0
        block_lines = block.splitlines()
        for line in block_lines:
            if line.startswith(">"):
                counter += 1
        if counter == len(block_lines):
            return BlockType.QUOTE

    if block.startswith("- "):
        counter = 0
        block_lines = block.splitlines()
        for line in block_lines:
            if line.startswith("- "):
                counter += 1
        if counter == len(block_lines):
            return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        counter = 0
        block_lines = block.splitlines()
        for i, line in enumerate(block_lines):
            if line.startswith(f"{i+1}. "):
                counter += 1
        if counter == len(block_lines):
            return BlockType.ORDERED_LIST
    else:
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
        list_of_html_nodes.append(text_node_to_html_node(text_node))
    return list_of_html_nodes


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
            pass
        if block_type == BlockType.CODE:
            pass
        if block_type == BlockType.QUOTE:
            pass
        if block_type == BlockType.UNORDERED_LIST:
            pass
        if block_type == BlockType.ORDERED_LIST:
            pass
    parent_node = ParentNode("div", children_nodes)
    return parent_node

md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

node = markdown_to_html_node(md)
# print (node)
html = node.to_html()
print (html)

"""
"<div><p>This is <b>bolded</b> paragraph
text in a p
tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
"""