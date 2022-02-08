import igraph as ig
import plotly.graph_objects as go
from django.conf import settings
from django.shortcuts import render
from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SuggesterFilterBackend,
)
from plotly.offline import plot

from radical_translations.agents.documents import AgentDocument
from radical_translations.agents.models import Agent, Organisation, Person
from radical_translations.agents.serializers import AgentDocumentSerializer
from radical_translations.core.views import BaseDetailView, BaseDocumentViewSet
from radical_translations.utils.search import PageNumberPagination

ES_FACET_OPTIONS = settings.ES_FACET_OPTIONS
ES_FUZZINESS_OPTIONS = settings.ES_FUZZINESS_OPTIONS


class AgentDetailView(BaseDetailView):
    model = Agent


def agent_list(request):
    return render(request, "agents/agent_list.html")


class AgentViewSet(BaseDocumentViewSet):
    document = AgentDocument
    serializer_class = AgentDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        # the suggester backend needs to be the last backend
        SuggesterFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "meta": {"field": "meta", "enabled": True, "options": ES_FACET_OPTIONS},
        "year": {
            "field": "year",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "gender": {
            "field": "gender",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "place_birth": {
            "field": "place_birth.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "place_death": {
            "field": "place_death.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "noble": {
            "field": "noble",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "main_place": {
            "field": "based_near.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "other_places": {
            "field": "main_places.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "role": {
            "field": "roles.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "language": {
            "field": "languages.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "anonymous": {
            "field": "anonymous",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
    }

    filter_fields = {
        "meta": "meta",
        "year": "year",
        "gender": "gender",
        "place_birth": "place_birth.address.raw",
        "place_death": "place_death.address.raw",
        "noble": "noble",
        "other_places": "main_places.address.raw",
        "main_place": "based_near.address.raw",
        "role": "roles.label.raw",
        "language": "languages.label.raw",
        "anonymous": "anonymous",
    }

    ordering_fields = {
        "name": "name_sort",
        "year": "year",
    }
    ordering = ["_score", "name_sort", "year"]

    pagination_class = PageNumberPagination

    name_search_options = ES_FUZZINESS_OPTIONS
    name_search_options["boost"] = 2

    search_fields = {
        "name": name_search_options,
        "content": ES_FUZZINESS_OPTIONS,
    }

    suggester_fields = {
        "suggest_field": {
            "field": "name.suggest",
            "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {"skip_duplicates": True, "size": 20},
        },
    }


def network(request):
    g = ig.Graph(directed=True)

    for org in Organisation.objects.exclude(roles__label__in=["archives", "library"]):
        g.add_vertex(name=f"agent-{org.id}", title=str(org), group=1)

    for person in Person.objects.all():
        group = 2

        if person.gender == "m":
            group = 3
        elif person.gender == "u":
            group = 4

        g.add_vertex(name=f"agent-{person.id}", title=str(person), group=group)

    for person in Person.objects.all():
        node_id = f"agent-{person.id}"

        for known in person.knows.all():
            g.add_edge(node_id, f"agent-{known.id}", label="knows")

        for org in person.member_of.all():
            g.add_edge(node_id, f"agent-{org.id}", label="member of")

    node_labels = g.vs["title"]
    node_groups = g.vs["group"]
    edge_labels = g.es["label"]

    layout = g.layout_graphopt()

    # nodes coordinates
    range_n = range(len(node_labels))
    nodes_x = [layout[i][0] for i in range_n]
    nodes_y = [layout[i][1] for i in range_n]

    # edges coordinates
    edges_x = []
    edges_y = []
    for e in g.get_edgelist():
        edges_x += [layout[e[0]][0], layout[e[1]][0], None]
        edges_y += [layout[e[0]][1], layout[e[1]][1], None]

    nodes_scatter = go.Scatter(
        x=nodes_x,
        y=nodes_y,
        mode="markers",
        marker=dict(
            symbol=node_groups,
            size=5,
            color=node_groups,
            colorscale="Viridis",
            line=dict(color="rgb(50,50,50)", width=0.5),
        ),
        text=node_labels,
        hoverinfo="text",
    )

    edges_scatter = go.Scatter(
        x=edges_x,
        y=edges_y,
        mode="lines",
        line=dict(width=1),
        line_shape="spline",
        marker=dict(color="rgb(125,125,125)"),
        text=edge_labels,
        hoverinfo="text",
    )

    axis = dict(
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title="",
    )

    go_layout = go.Layout(
        font=dict(size=12),
        autosize=False,
        width=1000,
        height=1000,
        hovermode="closest",
        xaxis=dict(axis),
        yaxis=dict(axis),
    )

    fig = go.Figure(data=[edges_scatter, nodes_scatter], layout=go_layout)

    plot_div = plot(fig, output_type="div", include_plotlyjs=False)

    return render(request, "agents/network.html", context={"plot_div": plot_div})
