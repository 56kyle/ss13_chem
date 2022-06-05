
import click

from analyze import (
    get_reagent_group,
    get_reagent_group_dict,
    get_dispensable_group,
    get_dispensable_group_dict,
)
from automate import enter_recipes

from bs4 import BeautifulSoup


if __name__ == '__main__':
    soup = BeautifulSoup(open('data/test.html'), 'html.parser')
    code = soup.find_all('code')
    lines = [c.text for c in code]
    with open('test.txt', 'w') as f:
        f.write('\n'.join(lines))


