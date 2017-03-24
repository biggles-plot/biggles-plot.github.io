#!/usr/bin/env python
import glob
import os
from jinja2 import Template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# First pull the examples
os.system('rm -f examples/* && '
          'git clone https://github.com/biggles-plot/biggles.git && '
          'cp -r biggles/examples . && '
          'rm -rf biggles')

# Set the style here.
STYLE = 'rainbow_dash'

# First render examples.
with open('example.template') as fp:
    tex = Template(fp.read())

examples = sorted(glob.glob('examples/*.py'))

example_code = ""
example_indicators = ""
for ind, example in enumerate(examples):
    with open(example, 'r') as fp:
        code = fp.read()

    if ind == 0:
        active = 'active'
        example_indicators \
            += '<li data-target="#carousel-example-generic" data-slide-to="%d" class="active"></li>\n' % ind
    else:
        active = ''
        example_indicators += '<li data-target="#carousel-example-generic" data-slide-to="%d"></li>\n' % ind

    example_code += tex.render(
        active=active,
        code=highlight(code, PythonLexer(), HtmlFormatter(style=STYLE)),
        image="<img src=\"%s\" style='img-responsive center-block'>" % example.replace('.py', '.png'))

    with open(example.replace('.py', '_stripped.py'), 'w') as fp:
        fp.write(code.replace('.show()', ''))

    os.system('cd examples && python %s && rm *.pdf && rm *.eps && rm %s && cd ..' % (
        os.path.split(example.replace('.py', '_stripped.py'))[1],
        os.path.split(example.replace('.py', '_stripped.py'))[1]))

# Now render the quick start code.
with open('quickstart.py', 'r') as fp:
    quickstart = highlight(fp.read(), PythonLexer(), HtmlFormatter(style=STYLE))

# Read in template and render it with each part.
with open('index.template', 'r') as fp:
    t = Template(fp.read())

with open('index.html', 'w') as fp:
    fp.write(t.render(example_indicators=example_indicators,
                      example_code=example_code,
                      quickstart=quickstart))

with open('highlight.css', 'w') as fp:
    fp.write(HtmlFormatter(style=STYLE).get_style_defs('.highlight'))

fnames = glob.glob('examples/*')
for fname in fnames:
    if not fname.endswith('.png'):
        try:
            os.remove(fname)
        except:
            pass
