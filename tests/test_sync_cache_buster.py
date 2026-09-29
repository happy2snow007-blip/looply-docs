import tempfile
import unittest
from pathlib import Path

import sync


class PrototypeConfigCacheBusterTest(unittest.TestCase):
    def test_updates_index_and_admin_script_urls_with_current_sync_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("index.html", "admin.html"):
                (root / name).write_text(
                    '<head><script src="prototype-config.js?v=old"></script></head>',
                    encoding="utf-8",
                )

            original_repo_dir = sync.REPO_DIR
            sync.REPO_DIR = str(root)
            try:
                sync.update_prototype_config_cache_buster("202609291405")
            finally:
                sync.REPO_DIR = original_repo_dir

            for name in ("index.html", "admin.html"):
                content = (root / name).read_text(encoding="utf-8")
                self.assertIn('src="prototype-config.js?v=202609291405"', content)
                self.assertNotIn("v=old", content)


if __name__ == "__main__":
    unittest.main()
