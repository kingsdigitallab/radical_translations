.. :changelog:

Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres to
`Semantic Versioning`_.

.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html


[Unreleased] - yyyy-mm-dd
--------------------

Added
~~~~~
* Custom vocabulary for ``Classification.edition``.
* Team information to the docs.
* humans.txt (http://humanstxt.org/).

Changed
~~~~~~~
* The import `Resource` command to import `Item` records from GSX.

Fixed
~~~~~
* Production Django Dockerfile.
* ``Resource`` import, it was failing to import `Original` works.


[0.2.2] - 2020-02-12
--------------------

Changed
~~~~~~~
* Change the format of this file to adhere to `Keep a Changelog`_.

Security
~~~~~~~~
* Bump Django from 2.2.9 to 2.2.10 (https://github.com/kingsdigitallab/radical_translations/pull/2)


[0.2.1] - 2020-02-11
--------------------

Fixed
~~~~~
* Import of resources with editions.


[0.2.0] - 2020-02-11
--------------------

Added
~~~~~
* Add command to import ``Event`` records from Google Spreadsheet JSON (GSX).
* Add command to import ``Organisation`` records from GSX.
* Add command to import ``Person`` records from GSX.
* Add command to import ``Resource`` records from GSX.


[0.1.0] - 2020-02-05
--------------------

Added
~~~~~
* Initial data models
