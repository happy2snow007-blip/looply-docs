from html.parser import HTMLParser
from pathlib import Path
import unittest


INDEX_PATH = Path(__file__).resolve().parents[1] / "index.html"


class IndexStructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.content_container_count = 0
        self.modules = []
        self.footers = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        in_content = any(
            node["is_content_container"]
            for node in self.stack
        )
        is_content_container = (
            tag == "div"
            and attributes.get("id") == "content"
            and "container" in classes
        )
        if is_content_container:
            self.content_container_count += 1
        if tag == "div" and "module-section" in classes:
            self.modules.append((attributes.get("data-module"), in_content))
        if tag == "div" and "footer" in classes:
            self.footers.append(in_content)
        self.stack.append(
            {"tag": tag, "is_content_container": is_content_container}
        )

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                return


class IndexContainerStructureTest(unittest.TestCase):
    def test_all_modules_share_the_content_container(self):
        parser = IndexStructureParser()
        parser.feed(INDEX_PATH.read_text(encoding="utf-8"))

        module_names = [name for name, _ in parser.modules]
        outside = [name for name, in_content in parser.modules if not in_content]
        self.assertEqual(1, parser.content_container_count)
        self.assertEqual(
            [], outside, f"modules outside #content.container: {outside}"
        )
        self.assertEqual(20, len(parser.modules))
        self.assertEqual(20, len(set(module_names)))
        self.assertEqual([False], parser.footers)


if __name__ == "__main__":
    unittest.main()
