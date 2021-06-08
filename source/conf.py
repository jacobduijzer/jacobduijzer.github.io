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

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',
    'sphinx_panels',
    'sphinxcontrib.plantuml',
    'ablog'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'friendly'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_theme_path = pydata_sphinx_theme.get_html_theme_path()

html_context = {                                                                 
    'custom_title' : 'Jacobs Blog'  
} 

html_sidebars = {
    '**': ['side_header.html', 'custom_tagcloud.html', 'custom_archives.html', 'socials.html'],
    # "content/projects": ["me.html"],
    # "content/articles/**": ['postcard.html', 'recentposts.html', 'archives.html'],
    "content/blog": ['side_header.html', 'custom_tagcloud.html', 'custom_archives.html', 'socials.html'],
    "content/blog/**": ['side_header.html', 'postcard.html', 'recentposts.html', 'custom_archives.html', 'socials.html']
}

# html_sidebars = {
#     "index": ['tagcloud.html', 'archives.html'],
#     "content/projects": ["hello.html"],
#     "content/articles/**": ['postcard.html', 'recentposts.html', 'archives.html'],
#     "content/blog": ['tagcloud.html', 'archives.html'],
#     "content/blog/**": ['postcard.html', 'recentposts.html', 'archives.html']
# }

html_show_sourcelink = False

# bootstrap theme options
html_theme_options = {
}

blog_baseurl = "https://duijzer.com"
blog_title = "Jacobs Weblog"
blog_path = "content/blog"
fontawesome_included = True
blog_post_pattern = ["content/articles/*/*", "content/articles/*/*/*"]
post_redirect_refresh = 1
post_auto_image = 0
post_auto_excerpt = 1
disqus_shortname = "blog-duijzer-com"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

### plantuml 
mySourceLocation = os.getcwd()
plantuml = 'java -jar "/usr/local/bin/plantuml.jar" -I/usr/src/plantuml/*'
plantuml_output_format = 'svg'

def setup(app):
    app.add_css_file('css/custom.css')