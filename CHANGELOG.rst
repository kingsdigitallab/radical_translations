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
* Map clustering.
* Docs: data workflow diagram.
* Blog tags navigation.
* Radical markers to `Resource` detail view.
* Radical markers to the search index and search results.
* Add search options to the settings.
* `Place` API view.
* Load analytics setting.
* GitHub action for CI.
* `Agents` search.
* Command to export `Resources` to a CSV file.
* Command to export `Organisations` and `Persons` to CSV files.
* Command to export `Events` to a CSV file.
* Docs: data model fields concordance.
* Command to export `Places` to a CSV file.
* Convert notes and summary URLs into clickable links.
* Badge for related resources that have a paratext.
* Paratext functions vocabulary.
* Radical date filter.

Changed
~~~~~~~
* Add profiles_ to the `pa11y`, `mongo` and `kibana` services in `local.yml`.
* Docs: update data models and architecture diagrams.
* Add paratext term `Revolutionary calendar use` to `Resources` that have a radical date.
* Modal map view uses an API call to get `Place` information rather than loading a Django view.
* Upgrade Wagtail_ to version 2.12.
* `Bump pillow to 7.1`_. 
* Exclude libraries from the list of `Organisations`.
* Exclude radicalism from the subject filter.
* Order/display `Resources` contributor filter by `family name, given name`.
* Order/display of `Contributions`.
* Labels and descriptions of the classification vocabularies.
* Split paratext terms vocabulary in two, paratext forms and paratext functions.

Fixed
~~~~~
* Validation errors in `CHANGELOG`.
* Search results map loading delay.
* Date interval parsing issues.
* Search results map not updating.
* Error when trying to add a map link to a publication place that is only a fictional place.
* The ordering of reverse relationships.

Removed
~~~~~~~
* `Place` detail view.
* Radical marker from dates.
* Radical markers filter from the search.
* Revolutionary calendar used filter from paratext filters.

.. _profiles: https://docs.docker.com/compose/profiles/
.. _Bump pillow to 7.1: https://github.com/kingsdigitallab/radical_translations/pull/5


[1.0.0] - 2021-01-27
--------------------

Added
~~~~~
* Data migration to merge duplicate libraries (`Organisation`).
* Field `radical` to `Agent`.
* Data migration to merge duplicate paratext terms.
* State management to search.
* Help text to both filter types (main and secondary).
* Help text to remove applied filters.
* Map view to the search results.
* Tag to `source text` search results.
* `Paratext` search filter.
* Modal view for `Place` references.

Changed
~~~~~~~
* `is_original` to include resources that are marked both as `original` and `source text`.
* Exclude the original/source text terms from being indexed with the translation terms.
* `Source text` and `translation` moved to top level filters.
* Split filters view into main and secondary.
* Translation facet label to Translation Terms.
* Move year facet to main filters section.
* Order related resources by date, relationship and title.
* Change `Original` to `Source text`.

Fixed
~~~~~
* Reset pagination when filtering by year or updating filters.


[0.10.3] - 2021-01-12
---------------------

Added
~~~~~
* Histogram to range facets.
* Click event to the histogram.


[0.10.2] - 2021-01-05
---------------------

Added
~~~~~
* Slider to range facets.
* Analytics script.


[0.10.1] - 2020-12-08
---------------------

Changed
~~~~~~~
* Reduce the search fuzziness distance to 1.

Fixed
~~~~~
* Do not display notes in bibliography page.


[0.10.0] - 2020-12-07
---------------------

Added
~~~~~
* Elasticsearch_ service.
* Kibana_ service.
* `Resource` search index.
* `Agents` search index.
* `Events` search index.
* `Resource` text search with filters, ordering and pagination of search results.
* `Resource` search tests.
* `Resource` search suggestions.
* Fuzzy_ text search.
* Search results highlighting_.
* Search styling.


[0.9.1] - 2020-12-01
--------------------

Fixed
~~~~~
* Images formatting and alignment.
* Icons display.


[0.9.0] - 2020-11-30
--------------------

Added
~~~~~
* Data migration to copy subjects from the translation resource to the original resource.
* `Pa11y dashboard`_ service.
* Data migration to merge duplicate libraries (`Organisation`).
* Data migration to merge duplicate languages.
* Function to get the date of a `Resource`.

Changed
~~~~~~~
* Truncate breadcrumb to 5 words.
* Truncate metatitle to 10 words.
* Remove unused and duplicate packages.
* Swap the labels for main and other places in the `Agent` detail view.

Fixed
~~~~~
* Do not display tag icon if there are not tags associated with a blog post.

.. _Elasticsearch: https://www.elastic.co/elasticsearch/
.. _Kibana: https://www.elastic.co/kibana/
.. _Fuzzy: https://www.elastic.co/guide/en/elasticsearch/reference/7.x/query-dsl-fuzzy-query.html
.. _highlighting: https://www.elastic.co/guide/en/elasticsearch/reference/7.x/highlighting.html
.. _Pa11y dashboard: https://github.com/pa11y/pa11y-dashboard


[0.8.0] - 2020-11-06
--------------------

Added
~~~~~
* Migration to convert `author` roles to `translator` when the `Resource` is a
  translation.
* Field to record fictional places of publication.
* Helper functions to `Date`, to get the earliest and latest dates for an object.
* Migration to convert Essay term from FAST_ topics to FAST_ forms vocabulary.
* Wagtail_ page type for the home page.
* Wagtail_ page type for biographies.
* Template tag to render breadcrumbs.

Changed
~~~~~~~
* Upgrade `Controlled Vocabulary`_ application.
* Upgrade Wagtail_ to version 2.9.

.. _FAST: https://www.oclc.org/research/areas/data-science/fast.html

[0.7.1] - 2020-07-02
--------------------

Added
~~~~~
* CERL_ vocabulary for `Agent` models.
* `Docker Compose`_ restart policies to the Docker services.
* `Django email`_ configuration.
* Fields `main_places` and `noble` to `Person`.
* New application, `cms`, for Wagtail_ customisations.

Changed
~~~~~~~
* Add date to `Resource` string for better disambiguation.
* Simplify the Fabric_ commands.
* Index page template to display extra information for blog posts.

Removed
~~~~~~~
* Helper script, it has been replaced with the Fabric_ file.
* Anymail integration.
* django-allauth integration.

Fixed
~~~~~
* `TyperError` in `Resource` `__str__`, was preventing the editing of records.
* Error templates.
* Admin favicon.
* Issues with `Controlled Vocabulary`_ application.

.. _CERL: https://data.cerl.org/thesaurus/
.. _Docker Compose: https://docs.docker.com/compose/compose-file/#restart
.. _Django email: https://docs.djangoproject.com/en/3.0/topics/email/
.. _Wagtail: https://wagtail.io/
.. _Controlled Vocabulary: https://github.com/kingsdigitallab/django-controlled-vocabulary/


[0.7.0] - 2020-06-17
--------------------

Added
~~~~~
* `Resource` views.
* `Agent` views.
* `Event` views.
* Configuration for `dev`, `stg`, and `liv` instances.
* Fabric_ script for remote task automation.
* Zotero_ integration_ to harvest bibliographic data from Zotero.

.. _Fabric: https://fabfile.org/
.. _Zotero: https://www.zotero.org/
.. _integration: https://django-kdl-wagtail.readthedocs.io/en/latest/readme.html#features


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


[0.10.0] - 2020-12-07
---------------------

Added
~~~~~
* Elasticsearch_ service.
* Kibana_ service.
* `Resource` search index.
* `Agents` search index.
* `Events` search index.
* `Resource` text search with filters, ordering and pagination of search results.
* `Resource` search tests.
* `Resource` search suggestions.
* Fuzzy_ text search.
* Search results highlighting_.
* Search styling.


[0.9.1] - 2020-12-01
--------------------

Fixed
~~~~~
* Images formatting and alignment.
* Icons display.


[0.9.0] - 2020-11-30
--------------------

Added
~~~~~
* Data migration to copy subjects from the translation resource to the original resource.
* `Pa11y dashboard`_ service.
* Data migration to merge duplicate libraries (`Organisation`).
* Data migration to merge duplicate languages.
* Function to get the date of a `Resource`.

Changed
~~~~~~~
* Truncate breadcrumb to 5 words.
* Truncate metatitle to 10 words.
* Remove unused and duplicate packages.
* Swap the labels for main and other places in the `Agent` detail view.

Fixed
~~~~~
* Do not display tag icon if there are not tags associated with a blog post.

.. _Elasticsearch: https://www.elastic.co/elasticsearch/
.. _Kibana: https://www.elastic.co/kibana/
.. _Fuzzy: https://www.elastic.co/guide/en/elasticsearch/reference/7.x/query-dsl-fuzzy-query.html
.. _highlighting: https://www.elastic.co/guide/en/elasticsearch/reference/7.x/highlighting.html
.. _Pa11y dashboard: https://github.com/pa11y/pa11y-dashboard


[0.8.0] - 2020-11-06
--------------------

Added
~~~~~
* Migration to convert `author` roles to `translator` when the `Resource` is a
  translation.
* Field to record fictional places of publication.
* Helper functions to `Date`, to get the earliest and latest dates for an object.
* Migration to convert Essay term from FAST_ topics to FAST_ forms vocabulary.
* Wagtail_ page type for the home page.
* Wagtail_ page type for biographies.
* Template tag to render breadcrumbs.

Changed
~~~~~~~
* Upgrade `Controlled Vocabulary`_ application.
* Upgrade Wagtail_ to version 2.9.

.. _FAST: https://www.oclc.org/research/areas/data-science/fast.html

[0.7.1] - 2020-07-02
--------------------

Added
~~~~~
* CERL_ vocabulary for `Agent` models.
* `Docker Compose`_ restart policies to the Docker services.
* `Django email`_ configuration.
* Fields `main_places` and `noble` to `Person`.
* New application, `cms`, for Wagtail_ customisations.

Changed
~~~~~~~
* Add date to `Resource` string for better disambiguation.
* Simplify the Fabric_ commands.
* Index page template to display extra information for blog posts.

Removed
~~~~~~~
* Helper script, it has been replaced with the Fabric_ file.
* Anymail integration.
* django-allauth integration.

Fixed
~~~~~
* `TyperError` in `Resource` `__str__`, was preventing the editing of records.
* Error templates.
* Admin favicon.
* Issues with `Controlled Vocabulary`_ application.

.. _CERL: https://data.cerl.org/thesaurus/
.. _Docker Compose: https://docs.docker.com/compose/compose-file/#restart
.. _Django email: https://docs.djangoproject.com/en/3.0/topics/email/
.. _Wagtail: https://wagtail.io/
.. _Controlled Vocabulary: https://github.com/kingsdigitallab/django-controlled-vocabulary/


[0.7.0] - 2020-06-17
--------------------

Added
~~~~~
* `Resource` views.
* `Agent` views.
* `Event` views.
* Configuration for `dev`, `stg`, and `liv` instances.
* Fabric_ script for remote task automation.
* Zotero_ integration_ to harvest bibliographic data from Zotero.

.. _Fabric: https://fabfile.org/
.. _Zotero: https://www.zotero.org/
.. _integration: https://django-kdl-wagtail.readthedocs.io/en/latest/readme.html#features


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
* Constraint on unique titles, it potentially caused duplicate entries under race conditions.


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
