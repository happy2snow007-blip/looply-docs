from html.parser import HTMLParser
from pathlib import Path
import unittest


class IndexStructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.modules = []
        self.footer_in_content = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        in_content = any(
            node["id"] == "content" and "container" in node["classes"]
            for node in self.stack
        )
        if tag == "div" and "module-section" in classes:
            self.modules.append((attributes.get("data-module"), in_content))
        if tag == "div" and "footer" in classes:
            self.footer_in_content = in_content
        self.stack.append(
            {"tag": tag, "id": attributes.get("id"), "classes": classes}
        )

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                return


class IndexContainerStructureTest(unittest.TestCase):
    def test_all_modules_share_the_content_container(self):
        parser = IndexStructureParser()
        parser.feed(Path("index.html").read_text(encoding="utf-8"))

        outside = [name for name, in_content in parser.modules if not in_content]
        self.assertEqual(
            [], outside, f"modules outside #content.container: {outside}"
        )
        self.assertEqual(20, len(parser.modules))
        self.assertFalse(parser.footer_in_content)


if __name__ == "__main__":
    unittest.main()
