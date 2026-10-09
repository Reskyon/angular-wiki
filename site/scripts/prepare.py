"""Turns the GitHub wiki into the docs/ folder that MkDocs uses.

- Home.md becomes index.md (the site's home page).
- Links between wiki pages have no extension ([text](02-bases#anchor));
  MkDocs needs the file name (02-bases.md#anchor).
- Special wiki pages (_Sidebar, _Footer) are not published.
- The nav: block of mkdocs.yml is rewritten from the wiki pages: fixed pages
  first and last, and every NN-name.md in between, ordered by number and titled
  with its first "# " heading.
"""

import re
import shutil
import sys
from pathlib import Path

wiki = Path(sys.argv[1])
docs = Path(sys.argv[2])
mkdocs_yml = Path(__file__).resolve().parent.parent / 'mkdocs.yml'

pages = {p.stem: p for p in wiki.glob('*.md') if not p.stem.startswith('_')}
target = {name: ('index' if name == 'Home' else name) for name in pages}

# [text](page) or [text](page#anchor); URLs and paths with an extension are left alone.
link = re.compile(r'\]\(([A-Za-z0-9._-]+?)(#[^)\s]*)?\)')


def fix(match: re.Match) -> str:
    name, anchor = match.group(1), match.group(2) or ''
    if name not in target:
        return match.group(0)
    return f']({target[name]}.md{anchor})'


if docs.exists():
    shutil.rmtree(docs)
docs.mkdir(parents=True)

for name, path in pages.items():
    text = link.sub(fix, path.read_text(encoding='utf-8'))
    (docs / f'{target[name]}.md').write_text(text, encoding='utf-8')
    print(f'{path.name} -> {target[name]}.md')


# Fixed pages that open and close the menu.
FIRST = [('Inicio', 'index.md'), ('Guía de estudio', 'study-guide.md')]
LAST = [('Hoja de atajos', 'cheatsheet.md')]
numbered = re.compile(r'\d\d-[a-z0-9-]+')

known = {'Home', 'study-guide', 'cheatsheet'}
unknown = sorted(n for n in pages if n not in known and not numbered.fullmatch(n))
if unknown:
    sys.exit(f'Pages not in the menu (rename to NN-name or add to prepare.py): {unknown}')


def title(name: str) -> str:
    for line in pages[name].read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    sys.exit(f'{name}.md has no "# " heading to use as menu title')



def entry(label: str, file: str) -> str:
    quoted = label.replace("'", "''")
    return f"  - '{quoted}': {file}\n"


parts = [(title(n), f'{n}.md') for n in sorted(pages) if numbered.fullmatch(n)]
nav = 'nav:\n' + ''.join(entry(*e) for e in FIRST + parts + LAST)

config = mkdocs_yml.read_text(encoding='utf-8')
config, count = re.subn(r'^nav:\n(?:[ \t]+.*\n)+', nav, config, count=1, flags=re.M)
if count != 1:
    sys.exit('mkdocs.yml has no nav: block to rewrite')
mkdocs_yml.write_text(config, encoding='utf-8')
print('nav rewritten with', len(parts), 'numbered pages')
