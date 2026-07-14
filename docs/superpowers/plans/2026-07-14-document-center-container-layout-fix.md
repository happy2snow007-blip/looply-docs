# Document Center Container Layout Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure every document-center module is rendered inside `#content.container` so all modules receive the shared 32px content gutter.

**Architecture:** Keep the existing single-container layout and correct only its closing boundary. Add a dependency-free Python structural regression test that parses `index.html` and verifies every `.module-section` is inside `#content.container` while the Footer remains outside it.

**Tech Stack:** Static HTML/CSS, Python 3 standard-library `html.parser` and `unittest`, GitHub Pages.

---

### Task 1: Add the structural regression test

**Files:**
- Create: `tests/test_index_container_structure.py`
- Test: `tests/test_index_container_structure.py`

- [ ] **Step 1: Write the failing test**

Create a parser that records whether each `.module-section` and the Footer appears while `#content.container` is on the open-element stack. Assert that all modules are inside the container and the Footer is outside it.

```python
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
        self.stack.append({"tag": tag, "id": attributes.get("id"), "classes": classes})

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
        self.assertEqual([], outside, f"modules outside #content.container: {outside}")
        self.assertEqual(20, len(parser.modules))
        self.assertFalse(parser.footer_in_content)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python3 -m unittest tests/test_index_container_structure.py -v`

Expected: FAIL listing `Favourites`, `收藏与浏览历史`, `shop页`, `Collection管理`, and `社媒分享管理` as outside `#content.container`.

### Task 2: Correct the container boundary

**Files:**
- Modify: `index.html:2673`
- Modify: `index.html:3131`
- Test: `tests/test_index_container_structure.py`

- [ ] **Step 1: Apply the minimal HTML change**

Remove the standalone `</div>` immediately before the Favourites module comment. Add the explicit container close after the social-sharing module and before the Footer:

```html
  <!-- ==================== 社媒分享管理模块 END ==================== -->

</div><!-- .container -->

<div class="footer">
```

- [ ] **Step 2: Run the test and verify GREEN**

Run: `python3 -m unittest tests/test_index_container_structure.py -v`

Expected: one test passes, with no failures or errors.

- [ ] **Step 3: Run repository checks**

Run: `git diff --check && python3 -m unittest discover -s tests -v`

Expected: exit code 0 and one passing test.

- [ ] **Step 4: Review the exact diff**

Run: `git diff -- index.html tests/test_index_container_structure.py`

Expected: only the closing-tag move and the structural regression test.

- [ ] **Step 5: Commit the fix**

```bash
git add index.html tests/test_index_container_structure.py docs/superpowers/plans/2026-07-14-document-center-container-layout-fix.md
git commit -m "fix: 统一文档中心模块正文间距"
```

### Task 3: Publish and verify GitHub Pages

**Files:**
- No additional repository files.

- [ ] **Step 1: Rebase on the latest remote main**

Run: `git pull --rebase origin main`

Expected: current branch is up to date or rebases without conflict.

- [ ] **Step 2: Re-run verification after rebase**

Run: `git diff HEAD~2 --check && python3 -m unittest discover -s tests -v`

Expected: exit code 0 and one passing test.

- [ ] **Step 3: Push main**

Run: `git push origin main`

Expected: remote `main` advances to the fix commit.

- [ ] **Step 4: Verify the deployed DOM**

Open `https://happy2snow007-blip.github.io/looply-docs/` after GitHub Pages updates and inspect the rendered DOM. Confirm all 20 `.module-section` elements have `#content.container` as an ancestor; for `登录注册`, `Favourites`, `收藏与浏览历史`, `Collection管理`, and `社媒分享管理`, confirm their content begins at the same horizontal offset relative to `.main-content`.
