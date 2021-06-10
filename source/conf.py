# Template + docs
# https://www.errbufferoverfl.me/
# https://www.errbufferoverfl.me/posts/2020/sphinx-blog-part-one/#sphinx-configuration

import pydata_sphinx_theme
import os
from datetime import date

# -- Project information -----------------------------------------------------
project = ''
copyright = f'{date.today().year}, Jacob Duijzer'
author = 'Jacob Duijzer'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_panels',
    'sphinxcontrib.plantuml',
    'sphinxcontrib.gist',
    'ablog'
]

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'friendly'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_theme_path = pydata_sphinx_theme.get_html_theme_path()
html_permalinks = False

html_context = {                                                                 
    'custom_title' : 'Jacobs Blog'  
} 

html_sidebars = {
    '**': ['side_header.html', 'custom_postcard.html', 'custom_tagcloud.html', 'custom_archives.html', 'socials.html'],
}

html_show_sourcelink = False

# bootstrap theme options
html_theme_options = {
}

# googleanalytics_id = "UA-103954361-1"
# googleanalytics_enabled = True
blog_baseurl = "https://duijzer.com"
blog_title = "Jacobs Weblog"
blog_path = "content/blog"
fontawesome_included = True
blog_post_pattern = ["content/articles/*/*", "content/articles/*/*/*"]
post_redirect_refresh = 1
post_auto_image = 0
post_auto_excerpt = 1
disqus_shortname = "blog-duijzer-com"

html_static_path = ['_static']

### plantuml 

sourceLocation = os.getcwd()
plantuml = 'java -jar ' + sourceLocation + '/../plantuml.jar'
# plantuml = '/usr/bin/plantuml'
plantuml_output_format = 'svg'

def setup(app):
    app.add_css_file('css/custom.css')
