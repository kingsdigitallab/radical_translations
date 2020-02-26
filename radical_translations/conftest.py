from typing import Dict

import pytest
from django.apps import apps
from django.core import management
from django.test import RequestFactory

from radical_translations.agents.models import Organisation, Person
from radical_translations.agents.tests.factories import (
    OrganisationFactory,
    PersonFactory,
)
from radical_translations.core.models import Resource, Title
from radical_translations.core.tests.factories import ResourceFactory, TitleFactory
from radical_translations.users.models import User
from radical_translations.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
@pytest.mark.django_db
def vocabulary():
    management.call_command("vocab", "init")
    app = apps.get_app_config("controlled_vocabulary")
    app._load_vocabulary_managers()  # type: ignore


@pytest.fixture
def organisation() -> Organisation:
    return OrganisationFactory()


@pytest.fixture
def person() -> Person:
    return PersonFactory()


@pytest.fixture
def resource() -> Resource:
    return ResourceFactory()


@pytest.fixture
def title() -> Title:
    return TitleFactory()


@pytest.fixture
def entry_original() -> Dict[str, Dict[str, str]]:
    return {
        "gsx$title": {"$t": "Les ruines ou Méditation sur les révolutions des Empires"},
        "gsx$authors": {"$t": "Constantin-François Volney"},
        "gsx$status": {"$t": "Original"},
        "gsx$statussource": {"$t": ""},
        "gsx$translationof": {"$t": ""},
        "gsx$editionof": {"$t": ""},
        "gsx$partof": {"$t": ""},
        "gsx$journaltitle": {"$t": ""},
        "gsx$editionnumber": {"$t": ""},
        "gsx$year": {"$t": "1791"},
        "gsx$location": {"$t": "0001: Paris [FR]"},
        "gsx$organisation": {"$t": "Desenne"},
        "gsx$language": {"$t": "French [fr]"},
        "gsx$genre": {"$t": "essay"},
        "gsx$url": {"$t": ""},
        "gsx$libraries": {"$t": ""},
        "gsx$notes": {"$t": ""},
        "gsx$citation": {"$t": ""},
        "gsx$paratextnotes": {"$t": ""},
        "gsx$paratextprefaceby": {"$t": ""},
    }


@pytest.fixture
def entry_translation() -> Dict[str, Dict[str, str]]:
    return {
        "gsx$title": {"$t": "The Ruins: or a Survey of the Revolutions of Empires"},
        "gsx$authors": {"$t": "James Marshall"},
        "gsx$status": {"$t": "Translation: integral"},
        "gsx$statussource": {"$t": ""},
        "gsx$translationof": {
            "$t": "Les ruines ou Méditation sur les révolutions des Empires"
        },
        "gsx$editionof": {"$t": ""},
        "gsx$partof": {"$t": ""},
        "gsx$journaltitle": {"$t": ""},
        "gsx$editionnumber": {"$t": ""},
        "gsx$year": {"$t": "1792"},
        "gsx$isyearfictional": {"$t": "FALSE"},
        "gsx$location": {"$t": "0002: London [UK]"},
        "gsx$islocationfictional": {"$t": "FALSE"},
        "gsx$organisation": {"$t": "J. Johnson"},
        "gsx$language": {"$t": "English [en]"},
        "gsx$genre": {"$t": "essay"},
        "gsx$url": {"$t": ""},
        "gsx$libraries": {"$t": ""},
        "gsx$notes": {"$t": ""},
        "gsx$citation": {"$t": ""},
        "gsx$paratextnotes": {"$t": ""},
        "gsx$paratextprefaceby": {"$t": "author"},
    }


@pytest.fixture
def entry_edition() -> Dict[str, Dict[str, str]]:
    return {
        "gsx$title": {"$t": "Discours sur le gouvernement"},
        "gsx$authors": {"$t": "P.A. Samson"},
        "gsx$status": {"$t": "Translation: integral"},
        "gsx$statussource": {"$t": ""},
        "gsx$translationof": {"$t": "Discourses concerning government"},
        "gsx$editionof": {"$t": "Discours sur le gouvernement"},
        "gsx$partof": {"$t": ""},
        "gsx$journaltitle": {"$t": ""},
        "gsx$editionnumber": {"$t": ""},
        "gsx$year": {"$t": "1794"},
        "gsx$isyearfictional": {"$t": "FALSE"},
        "gsx$location": {"$t": "0001: Paris [FR]"},
        "gsx$islocationfictional": {"$t": "FALSE"},
        "gsx$organisation": {"$t": "Josse"},
        "gsx$language": {"$t": "French [fr]"},
        "gsx$genre": {"$t": "essay"},
        "gsx$theme": {"$t": ""},
        "gsx$subject": {"$t": ""},
        "gsx$url": {
            "$t": "https://gallica.bnf.fr/ark:/12148/bpt6k2054034/f7.image.texteImage"
        },
        "gsx$libraries": {"$t": "BNF"},
        "gsx$notes": {
            "$t": (
                "Extracts in La Décade philosophique vol 3, year III/1, no. 24, p. "
                "537-544; vol 4, ear III/2, n. 26, p. 84-95."
            )
        },
        "gsx$citation": {"$t": ""},
        "gsx$paratextnotes": {"$t": ""},
        "gsx$paratextprefaceby": {"$t": ""},
    }
