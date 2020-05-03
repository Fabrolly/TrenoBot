import datetime
import os
import sys

sys.path.extend(
    [
        os.path.join(os.path.dirname(__file__), "..", "backend"),
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "backend",
            "venv",
            "lib",
            "python3.8",
            "site-packages",
        ),
        os.path.join(os.path.dirname(__file__), "..", "stats_website"),
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "stats_website",
            "venv",
            "lib",
            "python3.8",
            "site-packages",
        ),
        os.path.join(os.path.dirname(__file__), "..", "telegram-bot"),
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "telegram-bot",
            "venv",
            "lib",
            "python3.8",
            "site-packages",
        ),
    ]
)

project = "TrenoBot"
author = "TrenoBot Team"
version = "1.0"

copyright = "{0}, TrenoBot".format(datetime.datetime.now().year)


extensions = [
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.autosummary",
    "sphinxcontrib.httpdomain",
    "sphinxcontrib.autohttp.flask",
    "sphinxcontrib.autohttp.flaskqref",
    "sphinx.ext.doctest",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

templates_path = ["_templates"]

exclude_patterns = ["_build", "_templates"]

html_theme = "sphinx_rtd_theme"

html_show_sphinx = False
html_show_sourcelink = True

autosummary_generate = True
autodoc_default_flags = ["members"]
napoleon_use_param = True
