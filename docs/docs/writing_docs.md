# Writing Docs

To write technical documentation [Sphinx](https://www.sphinx-doc.org/en/master/) is used. Sphinx allows to write general docs in RsT and Markdown format and also to generate docs from the docstrings inside the code.

The preferred docstring format is the [Google Style Python Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

## Publishing the Docs

Docs are automatically built by the GitLab pipeline whenever a change is detected to `master` or `sprintN` and published to a GitLab Pages instance.

The current url for accessing the docs is: https://laboratorio-di-progettazione-trenobot.gitlab.io/trenobot-laboratorio-di-progettazione/

## Building Locally


After changing the docs it is possible to build them locally and see the end result via the command

```sphinx-build docs/ build/docs```

assuming that the project-root-level `requirements.txt` was installed.

The built docs will be into the `build/docs` folder.



