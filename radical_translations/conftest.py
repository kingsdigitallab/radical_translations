import pytest
from django.core import management
from django.test import RequestFactory

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
    management.call_command("vocab", "init", verbosity=0)
