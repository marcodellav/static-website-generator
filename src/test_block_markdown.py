import unittest

from block_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node
)

from textnode import TextNode, TextType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\ntext in a p\ntag here",
                "This is another paragraph with _italic_ text and `code` here",
            ],
        )

    def test_block_to_block_type_ordered_list(self):
        block = """1. first line
2. second line
3. third line"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_block_to_block_type_unordered_list(self):
        block = """- first line
- second line
- third line"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_block_to_block_code(self):
        block = """```
python3 src/main.py
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_ordered_list(self):
        md = """1. first line
2. second line
3. third line"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>1. first line</li><li>2. second line</li><li>3. third line</li></ol></div>",
        )
    def test_unordered_list(self):
        md = """- first line
- second line
- third line"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>- first line</li><li>- second line</li><li>- third line</li></ul></div>",
        )
    def test_markdown_to_blocks_2heading(self):
        md = "### Heading H3"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading H3</h3></div>",
        )

if __name__ == "__main__":
    unittest.main()