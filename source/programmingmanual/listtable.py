#!/usr/bin/env python
# encoding: utf-8 

#modified from
#https://github.com/rackerlabs/docs-rackspace/blob/master/tools/table.py

#test with
#py.test --doctest-modules listtable.py

"""
Convert RST grid tables to list-tables.
Basic usage
-----------
#. Convert grid tables in a file to list-tables. The result is output
   to stdout::
      $ python tables.py input.rst
#. Convert several files::
      $ python tables.py input1.rst input2.rst
      $ python tables.py *.rst
Options
-------
-j, --join       e.g.002. Join method per column: 0="".join; 1=" ".join; 2="\\n".join

.. important::

    Always build your document and compare the rendered list-table to the
    original rendered grid table. It is very possible that some errors may
    occur that require manual fixes, especially when converting complex tables.

Notes
-----
- The script does not create titles for tables. After conversion, you may
  want to manually add titles.
- The script sets all columns to the same width: ``100 / col_num``. After
  conversion, you may want to manually edit ``:width:``.
- The script automatically uses the first row of the table as a header.
  After conversion, you may want to manually edit ``:header-rows:``.
- The script requires a blank line after each table. If the blank line is at
  the end of the file, you must add an extra line temporarily for the script
  to process the table correctly.
"""

import argparse
from os import path
import re

def tolisttable(
        data, 
        join='012'):
    """convert grid table to list table
    >>> data = ['+---+---+---+','| A | x | 1 |','+===+===+===+','| B | y | 2 |','| C | z | 3 |','+---+---+---+']
    >>> lt=tolisttable(data)
    >>> lt.splitlines()[3]
    ''
    >>> lt.splitlines()[-2].strip()
    '3'
    >>> lt=tolisttable(data,join='001')
    >>> lt.splitlines()[7]
    ''
    >>> lt.splitlines()[-2].strip()
    '- 2 3'
    >>> lt=tolisttable(data,join='0')
    >>> lt.splitlines()[-2].strip()
    '- 23'
    """
    grid = False
    insert = False
    gridtable = []
    content = []
    splitline = lambda line: [x for x in line.split('|') if x and '\n' not in x]
    combine = {
            0:lambda e: [''.join([ee.strip() for ee in e]).strip()],
            1:lambda e: [' '.join([ee.strip() for ee in e]).strip()],
            2:lambda e: [ee[len(re.split('\w',e[0])[0]):].rstrip() for ee in e]
            }
    for line in data:
        if line.startswith('+--') or line.startswith('+=='):
            grid = True
            insert = True
            gridtable.append(line)
        elif grid and line.startswith('|'):
            gridtable.append(line)
        else:
            grid = False
        if grid:
            if insert:
                insert = False
                col_num = gridtable[0].count('+') - 1
                col_width = str(int(100 / col_num))
                col_width = (' ' + col_width) * col_num
                output = []
                output = [combine[int(join[c]if c<len(join)else join[-1])](e) for c,e in enumerate(zip(*[splitline(line) for line in gridtable if not line.startswith('+')]))]
                result = '\n'.join([(('       ' if j else ('     - ' if i else '   * - '))+xx) for i,x in enumerate(output) for j,xx in enumerate(x)]+[''])
                if len(gridtable)==1:
                    newtable = ".. list-table::\n   :widths:{0}\n   :header-rows: 1\n{1}".format(col_width, result)
                else:
                    newtable = result
                content.append(newtable + '\n')
                gridtable = []
    content = ''.join(content)
    return content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="table",
                                     description='''Convert RST grid table
                                     to list-table.''')
    parser.add_argument('INPUT', type=str, nargs='+', help='RST file(s)')
    parser.add_argument('-j', '--join', action='store', default='012',
            help='''e.g.002. Join method per column:
                    0="".join; 1=" ".join; 2="\\n".join''')
    args = parser.parse_args()
    join = args.join
    for infile in args.INPUT:
        infile = path.realpath(infile)
        data=[]
        with open(infile, 'r') as f:
            data = f.readlines()
        print(tolisttable(data, join))

