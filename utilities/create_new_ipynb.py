import logging
import re
from datetime import datetime
from pathlib import Path

import nbformat as nbf


def main():
    # timestamp for jekyll
    dt = datetime.now()
    title_dt = dt.strftime('%Y-%m-%d')
    header_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f'Timestamp: {dt}')

    # paths
    posts_dir = Path(__file__).parents[1] / '_posts'  # type: Path
    logging.info(f'Posts directory: {posts_dir.resolve()}')

    # ensure year dir exists
    current_year_dir = posts_dir / str(dt.year)
    current_year_dir.mkdir(exist_ok=True)

    # ask for title
    raw_title = input('Notebook title?\n>>>\t')

    # clean non-alphanumeric
    clean_title = re.sub('([^A-Za-z0-9\s])', '', raw_title)
    clean_title = '-'.join(clean_title.split()).lower()

    # create notebook
    header = '\n'.join([
        '---',
        f'title: "{raw_title}"',
        f'date: "{header_dt}"',
        'excerpt: XXX',
        'header:',
        '  teaser: assets/img/stock-photos/nick-hillier-339049.png',
        '  overlay_image: assets/img/stock-photos/nick-hillier-339049.png',
        '  overlay_filter: 0.1',
        'classes: wide',
        'categories:',
        '- X',
        'tags:',
        '- X',
        '---',
        '\n'
    ])

    nb = nbf.v4.new_notebook()
    nb['cells'] = [nbf.v4.new_raw_cell(header), nbf.v4.new_code_cell('')]

    nb_path = current_year_dir / f'{title_dt}-{clean_title}.ipynb'
    logging.info(f'Generating: {nb_path.resolve()}')
    with open(nb_path, 'w') as f:
        nbf.write(nb, f)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
