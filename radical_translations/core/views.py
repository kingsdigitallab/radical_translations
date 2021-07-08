import igraph as ig

# import pandas as pd
import plotly.graph_objects as go
from django.conf import settings
from django.shortcuts import render
from django.views.generic.detail import DetailView
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
    HighlightBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from plotly.offline import plot

from radical_translations.agents.models import Agent, Person
from radical_translations.core.documents import ResourceDocument
from radical_translations.core.models import (
    Contribution,
    Resource,
    ResourceRelationship,
)
from radical_translations.core.serializers import ResourceDocumentSerializer
from radical_translations.utils.search import PageNumberPagination

ES_FACET_OPTIONS = settings.ES_FACET_OPTIONS
ES_FUZZINESS_OPTIONS = settings.ES_FUZZINESS_OPTIONS


class ResourceDetailView(DetailView):
    model = Resource


def resource_list(request):
    return render(request, "core/resource_list.html")


class ResourceViewSet(DocumentViewSet):
    document = ResourceDocument
    serializer_class = ResourceDocumentSerializer

    filter_backends = [
        FilteringFilterBackend,
        FacetedSearchFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        SearchFilterBackend,
        HighlightBackend,
        # the suggester backend needs to be the last backend
        SuggesterFilterBackend,
    ]

    lookup_field = "id"

    faceted_search_fields = {
        "paratext_forms": {
            "field": "classifications_paratext.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "paratext_functions": {
            "field": "classifications_paratext_functions.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "printing_and_publishing_status": {
            "field": "classifications_printing_publishing.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "translations_status": {
            "field": "classifications_translation.edition.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "contributor": {
            "field": "contributions.agent.name.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "contributor_role": {
            "field": "contributions.roles.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "year": {
            "field": "year",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "language": {
            "field": "languages.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "publication_place": {
            "field": "places.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "publication_country": {
            "field": "places.place.country.name.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "status": {
            "field": "relationships.relationship_type.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "subject": {
            "field": "subjects.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "form_genre": {
            "field": "form_genre.label.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "event": {
            "field": "events.title.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "event_place": {
            "field": "events.place.address.raw",
            "enabled": True,
            "options": ES_FACET_OPTIONS,
        },
        "meta": {"field": "meta", "enabled": True, "options": ES_FACET_OPTIONS},
    }

    filter_fields = {
        "paratext_forms": "classifications_paratext.edition.label.raw",
        "paratext_functions": "classifications_paratext_functions.edition.label.raw",
        "printing_and_publishing_status": (
            "classifications_printing_publishing.edition.label.raw"
        ),
        "translations_status": "classifications_translation.edition.label.raw",
        "contributor": "contributions.agent.name.raw",
        "contributor_role": "contributions.roles.label.raw",
        "year": "year",
        "form_genre": "form_genre.label.raw",
        "language": "languages.label.raw",
        "publication_place": "places.place.address.raw",
        "publication_country": "places.place.country.name.raw",
        "fictional_place_of_publication": "places.fictional_place.raw",
        "status": "relationships.relationship_type.label.raw",
        "subject": "subjects.label.raw",
        "event": "events.title.raw",
        "event_place": "events.place.address.raw",
        "meta": "meta",
    }

    highlight_fields = {
        "title": {
            "enabled": True,
            "options": {
                "number_of_fragments": 0,
                "pre_tags": ["<span class='highlight'>"],
                "post_tags": ["</span>"],
            },
        },
        "content": {
            "enabled": True,
            "options": {
                "fragment_size": 150,
                "number_of_fragments": 3,
                "pre_tags": ["<span class='highlight'>"],
                "post_tags": ["</span>"],
            },
        },
    }

    ordering_fields = {
        "title": "title.sort",
        "year": "year",
    }
    ordering = ["_score", "title.sort", "year"]

    pagination_class = PageNumberPagination

    title_search_options = ES_FUZZINESS_OPTIONS
    title_search_options["boost"] = 4
    author_search_options = ES_FUZZINESS_OPTIONS
    author_search_options["boost"] = 2

    search_fields = {
        "title": title_search_options,
        "authors.person.name": author_search_options,
        "content": ES_FUZZINESS_OPTIONS,
    }

    suggester_fields = {
        "suggest_field": {
            "field": "authors.person.name.suggest",
            "suggesters": [SUGGESTER_COMPLETION, SUGGESTER_PHRASE, SUGGESTER_TERM],
            "default_suggester": SUGGESTER_COMPLETION,
            "options": {"skip_duplicates": True, "size": 20},
        },
    }


def network(request):
    g = ig.Graph(directed=True)

    for resource in Resource.objects.exclude(
        relationships__relationship_type__label="paratext of"
    ):
        group = 2
        title = "Translation: "

        if resource.is_original():
            group = 1
            title = "Source text: "

        title = f"{title}{str(resource)}"

        g.add_vertex(name=f"resource-{resource.id}", title=title, group=group)

    for agent in Agent.objects.exclude(roles__label="library"):
        group = 4 if agent.agent_type == "organisation" else 3
        g.add_vertex(name=f"agent-{agent.id}", title=str(agent), group=group)

    for contribution in Contribution.objects.all():
        resource = contribution.resource
        while resource.is_paratext():
            next_resource = resource.paratext_of()
            if next_resource.id == resource.id:
                resource = None
                break

            resource = next_resource

        if resource:
            for role in contribution.roles.all():
                g.add_edge(
                    f"agent-{contribution.agent.id}",
                    f"resource-{resource.id}",
                    label=role.label,
                )

    for relationship in ResourceRelationship.objects.exclude(
        relationship_type__label="paratext of"
    ):
        resource = relationship.resource
        while resource.is_paratext():
            next_resource = resource.paratext_of()
            if next_resource.id == resource.id:
                resource = None
                break

            resource = next_resource

        related_to = relationship.related_to
        while related_to.is_paratext():
            next_resource = related_to.paratext_of()
            if next_resource.id == related_to.id:
                related_to = None
                break

            related_to = next_resource

        if resource and related_to:
            g.add_edge(
                f"resource-{resource.id}",
                f"resource-{related_to.id}",
                label=relationship.relationship_type.label,
            )

    for person in Person.objects.all():
        for knows in person.knows.all():
            g.add_edge(f"agent-{person.id}", f"agent-{knows.id}", label="knows")

        for org in person.member_of.all():
            g.add_edge(f"agent-{person.id}", f"agent-{org.id}", label="member of")

    node_labels = g.vs["title"]
    node_groups = g.vs["group"]
    edge_labels = g.es["label"]
    # edge_groups = pd.Series(edge_labels).astype("category").cat.codes.values.tolist()

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

    return render(request, "core/network.html", context={"plot_div": plot_div})
