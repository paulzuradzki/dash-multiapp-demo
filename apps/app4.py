# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!

### Markdown Demo
---

# Heading 1
## Heading 2
### Heading 3

Unordered list
* foo
* bar
* yow

[Links (CNN Lite)](https://lite.cnn.com/en)

'''

layout = html.Div([
    dcc.Markdown(children=markdown_text),
    dcc.Link('Go back to home', href='/')
])
