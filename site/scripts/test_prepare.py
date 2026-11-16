"""Check that portfolio content extends the published course navigation."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("prepare.py")


class PortfolioBonusTests(unittest.TestCase):
    def test_bonus_comes_after_new_numbered_chapters(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            wiki = root / "wiki"
            wiki.mkdir()
            for name, title in {
                "Home": "Home",
                "study-guide": "Study guide",
                "cheatsheet": "Cheatsheet",
                "09-teslo-shop": "Teslo Shop",
                "10-new-chapter": "New chapter",
            }.items():
                (wiki / f"{name}.md").write_text(f"# {title}\n", encoding="utf-8")

            scripts = root / "site" / "scripts"
            scripts.mkdir(parents=True)
            script = scripts / SCRIPT.name
            shutil.copyfile(SCRIPT, script)
            config = scripts.parent / "mkdocs.yml"
            config.write_text("nav:\n  - Home: index.md\n", encoding="utf-8")
            docs = scripts.parent / "docs"

            def prepare():
                subprocess.run([sys.executable, str(script), str(wiki), str(docs)],
                               capture_output=True, check=True)
                return config.read_text(encoding="utf-8")

            self.assertNotIn("CV/Portfolio Angular", prepare())

            bonus = scripts.parent / "portfolio-bonus"
            bonus.mkdir()
            (bonus / "index.md").write_text("# Portfolio\n", encoding="utf-8")
            (bonus / "learn-projects.md").write_text("# Projects\n", encoding="utf-8")
            (bonus / "navigation.json").write_text(json.dumps([
                {"title": "Learn", "pages": ["learn-projects"]},
            ]), encoding="utf-8")
            nav = prepare()

            self.assertLess(nav.index("10-new-chapter.md"), nav.index("CV/Portfolio Angular"))
            self.assertLess(nav.index("CV/Portfolio Angular"), nav.index("cheatsheet.md"))
            self.assertIn("portfolio-bonus/index.md", nav)
            self.assertIn("portfolio-bonus/learn-projects.md", nav)
            self.assertEqual((docs / "portfolio-bonus" / "learn-projects.md")
                             .read_text(encoding="utf-8"), "# Projects\n")
            self.assertFalse((docs / "portfolio-bonus" / "navigation.json").exists())
