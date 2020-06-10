.. :changelog:

Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres to
`Semantic Versioning`_.

.. _Keep a Changelog: https://keepachangelog.com/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

[Unreleased] - yyyy-mm-dd
--------------------

Added
~~~~~
* `Resource` views.
* `Agent` views.
* `Event` views.
* Configuration for `dev`, `stg`, and `liv` instances.

[0.6.3] - 2020-06-08
--------------------

Changed
~~~~~~~
* `Date` display format to include radical date when available.
* Prefix paratext `Resources` with `[paratext]`.
* Replace `Classification` `source` with editorial classification field.

Fixed
~~~~~
* Update Django Controlled Vocabulary app.
* Add missing vocabulary entry for Printing and Publishing Terms.
* Autocomplete for `Event` and `Place` models.
* Issue deleting `Resource` contributions.

[0.6.2] - 2020-06-02
--------------------

Changed
~~~~~~~
* Disable automatic conversion of dates.


[0.6.1] - 2020-06-02
--------------------

Added
~~~~~
* KDL Wagtail People page types.
* Sources and notes fields to `Agent`.

Changed
~~~~~~~
* Do not display French Republican dates by default.
* Domain name, radicaltranslations.org.

Fixed
~~~~~
* Agent search.


[0.6.0] - 2020-06-01
--------------------

Added
~~~~~
* Log entries to the admin interface.
* wagtailmenus app.
* Conversion from Gregorian to French Republican dates.
* Command to import `Resource` URLs from GSX.
* Basic styling and typography.

Changed
~~~~~~~
* Wagtail now serves the root URL.
* Agents admin, add extra search fields and filters.
* Reorganise KDL Wagtail templates.

Fixed
~~~~~
* Add missing Wagtail apps.
* `Resource`, `electronic_locator` import.


[0.5.1] - 2020-05-27
--------------------

Changed
~~~~~~~
* When importing `Resource` check if a resource with the same title and date already
  exists.
* Import `Resource` relationships after all the resources are imported to avoid
  conflicts.


[0.5.0] - 2020-05-27
--------------------

Added
~~~~~
* New tests for `Resource`.
* New tests for `Title`.
* Original as a value for `Classification.edition` vocabulary.
* nginx to serve media files.

Changed
~~~~~~~
* Update vocabularies with values provided by the research team.


[0.4.1] - 2020-05-19
--------------------

Fixed
~~~~~
* `Classification` tests.


[0.4.0] - 2020-05-19
--------------------

Changed
~~~~~~~
* For simplicity the Work/Instance/Item objects have been flattened into Resource.


[0.3.1] - 2020-05-12
--------------------

Fixed
~~~~~
* Constraint on unique titles, it potentially caused duplicate entries under race
conditions.


[0.3.0] - 2020-05-11
--------------------

Added
~~~~~
* Custom vocabulary for ``Classification.edition``.
* Team information to the docs.
* humans.txt (http://humanstxt.org/).
* Place of birth and place of death to Person model.
* Paratext mapping.
* Date field to record dates that are in alternative formats.
* New resource relationship types.
* Editorial classification field to further specify relationships between objects.
* Field for contributions under pseudonyms.
* Chicago: Rare Books and Manuscripts Section controlled vocabulary.

Changed
~~~~~~~
* The import `Resource` command to import `Item` records from GSX.
* Reduce the number of models in the admin interface.
* Allow part of relationships for original works.
* Add counter as `subtitle` to imported `Untitled` and `Translation` titles from GSX.

Fixed
~~~~~
* Production Django Dockerfile: add missing dependencies.
* ``Resource`` import, it was failing to import `Original` works.
* ``Resource`` import, it was creating ``Work`` objects for derivative instances.
* ``Resource`` import, import relationships to multiple ``Work`` objects.

Security
~~~~~~~~
* Upgrade jQuery, https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/
* Upgrade Wagtail, https://docs.wagtail.io/en/stable/releases/2.8.1.html


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
