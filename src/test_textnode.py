import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node0 = TextNode("This is a text node", TextType.BOLD)
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node0, node1)

    def test_eq_2(self):
        node0 = TextNode("This is a text node", TextType.ITALIC)
        node1 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node0, node1)

    def test_not_eq(self):
        node0 = TextNode("This is a text node", TextType.CODE)
        node1 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node0, node1)

    def test_eq(self):
        node0 = TextNode("This is a text node", TextType.ITALIC, None)
        node1 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node0, node1)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("Hello, world!", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://www.boot.dev")

    def test_image(self):
        node = TextNode("Hello, world!", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://www.boot.dev")

if __name__ == "__main__":
    unittest.main()