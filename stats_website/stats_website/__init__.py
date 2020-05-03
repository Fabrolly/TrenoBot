"""
The stats website is a web service based on Flask that uses the backend service to access data from the Trenord APIs.
For the web interface Bootstrap is used for the inteface and Chart.js for the interactive graphs.

A quite standard approach for Flask apps is used for the structure of the project, mostly a lightweight version of the MVC pattern.

Folder structure:

* ``controllers``: controllers of the website
* ``static``: static resources
* ``templates``: Jinja2 templates for HTML
* ``tests``: unit tests
* ``backend_api.py``: a module to interact with the API
* ``stats_website.py``: the entrypoint/main of the project
"""
