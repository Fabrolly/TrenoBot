"""
This controllers handle requests for site-related mostly static pages.

Put here pages like: index, about, contact.

Don't put here pages like: train stats, authentication.
"""

from flask import render_template
from .. import backend_api


def index():
    """
    .. :quickref: Page; Get Index

    Serve the index page
    """
    stats = backend_api.get_general_stats()
    return render_template("pages/index.html.j2", stats=stats)
