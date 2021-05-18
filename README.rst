Radical Translations
====================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT license
.. image:: https://github.com/kingsdigitallab/radical_translations/workflows/CI/badge.svg?branch=master
    :target: https://github.com/kingsdigitallab/radical_translations/actions?query=workflow%3ACI
    :alt: Build status
.. image:: https://coveralls.io/repos/github/kingsdigitallab/radical_translations/badge.svg
    :target: https://coveralls.io/github/kingsdigitallab/radical_translations
    :alt: Coverage status
.. image:: https://readthedocs.org/projects/radical-translations/badge/?version=latest
    :target: https://radical-translations.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation status
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/kingsdigitallab/cookiecutter-django/
    :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black
    :alt: Black code style

TODO: Add Radical Translations description...

Settings
--------

See detailed `cookiecutter-django settings documentation`_.

.. _cookiecutter-django settings documentation: http://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/settings.html

Development
-----------

Local with Docker
^^^^^^^^^^^^^^^^^

See detailed `cookiecutter-django development with Docker documentation`_.

.. _cookiecutter-django development with Docker documentation: https://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/developing-locally-docker.html

Local without Docker
^^^^^^^^^^^^^^^^^^^^

See detailed `cookiecutter-django local development documentation`_.

.. _cookiecutter-django local development documentation: https://cookiecutter-django-kingsdigitallab.readthedocs.io/en/latest/developing-locally.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the
  form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go
  to your console to see a simulated email verification message. Copy the link
  into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your
superuser logged in on Firefox (or similar), so that you can see how the site
behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy radical_translations

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



Custom Bootstrap Compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated CSS is set up with automatic Bootstrap recompilation with
variables of your choice.
Bootstrap v4 is installed using npm and customised by tweaking your variables
in ``static/sass/custom_bootstrap_vars``.

You can find a list of available variables `in the bootstrap source`_, or get
explanations on them in the `Bootstrap docs`_.


Bootstrap's javascript as well as its dependencies is concatenated into a
single file: ``static/js/vendors.js``.


.. _in the bootstrap source: https://github.com/twbs/bootstrap/blob/v4-dev/scss/_variables.scss
.. _Bootstrap docs: https://getbootstrap.com/docs/4.1/getting-started/theming/


