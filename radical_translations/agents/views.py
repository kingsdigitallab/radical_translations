from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from radical_translations.agents.models import Agent, Organisation, Person


class AgentDetailView(DetailView):
    model = Agent


class OrganisationListView(ListView):
    model = Organisation
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Organisations"
        return context


class PersonListView(ListView):
    model = Person
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Persons"
        return context
