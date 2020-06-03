from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from radical_translations.core.models import Resource


class ResourceDetailView(DetailView):
    model = Resource


class ResourceListView(ListView):
    model = Resource
    paginate_by = 50
    queryset = Resource.objects.exclude(
        relationships__relationship_type__label="paratext of"
    )
