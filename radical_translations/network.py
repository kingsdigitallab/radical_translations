import json
from collections import defaultdict

from django.urls import reverse
from django.utils.http import urlencode

from geonames_place.models import Place
from radical_translations.agents.models import Organisation, Person
from radical_translations.core.models import Contribution, Resource, ResourceLanguage


class NetworkObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return super().default(obj)


def network():
    nodes = {}
    edges = []

    for language in ResourceLanguage.objects.values_list(
        "language__label", flat=True
    ).distinct():
        id = language.lower()
        nodes[id] = dict(
            id=id,
            title=language,
            group="language",
            url=(
                f"{reverse('agent-list')}"
                f"?{urlencode(dict(language__term=language))}"
            ),
        )

    for p in Place.objects.all():
        if p.agents.count() > 0 or p.resourceplace_set.count() > 0:
            id = f"place-{p.id}"
            nodes[id] = dict(
                id=f"place-{p.id}",
                title=p.address,
                group="place",
                url=(
                    f"{reverse('agent-list')}"
                    f"?{urlencode(dict(main_place__term=p.address))}"
                ),
            )

    for org in Organisation.objects.exclude(roles__label__in=["archives", "library"]):
        id = f"agent-{org.id}"

        nodes[id] = dict(
            id=id,
            title=org.name,
            group=org.agent_type,
            url=reverse("agent-detail", kwargs={"pk": org.id}),
            meta=defaultdict(set),
        )

        for p in org.based_near.all():
            nodes[id]["meta"]["based_in"].add(p.address)
            edges.append(
                dict(source=id, target=f"place-{p.id}", label="based in (place)")
            )

    for person in Person.objects.all():
        id = f"agent-{person.id}"

        nodes[id] = dict(
            id=id,
            title=person.name,
            group=f"{person.agent_type} ({person.gender})",
            gender=person.gender,
            url=reverse("agent-detail", kwargs={"pk": person.id}),
            meta=defaultdict(set),
        )

        for p in person.based_near.all():
            nodes[id]["meta"]["based_in"].add(p.address)
            edges.append(
                dict(source=id, target=f"place-{p.id}", label="based in (place)")
            )

    for person in Person.objects.all():
        source_id = f"agent-{person.id}"

        for known in person.knows.all():
            target_id = f"agent-{known.id}"

            nodes[source_id]["meta"]["knows"].add(known.name)
            edges.append(dict(source=source_id, target=target_id, label="knows"))

        for org in person.member_of.all():
            target_id = f"agent-{org.id}"

            nodes[source_id]["meta"]["member_of"].add(org.name)
            edges.append(dict(source=source_id, target=target_id, label="member of"))

    for contribution in Contribution.objects.filter(roles__label="translator"):
        agent = contribution.agent
        source_id = f"agent-{agent.id}"

        if contribution.resource and contribution.resource.get_authors_source_text():
            for author in contribution.resource.get_authors_source_text():
                if author != agent:
                    target_id = f"agent-{author.id}"

                    nodes[source_id]["meta"]["translated"].add(author.name)
                    edges.append(
                        dict(source=source_id, target=target_id, label="translated")
                    )

            for rp in contribution.resource.places.all():
                p = rp.place
                if p:
                    nodes[source_id]["meta"]["published_in"].add(p.address)
                    edges.append(
                        dict(
                            source=source_id,
                            target=f"place-{p.id}",
                            label="published in (place)",
                        )
                    )

            for rl in contribution.resource.languages.all():
                nodes[source_id]["meta"]["translated_to"].add(rl.language.label)

    for contribution in Contribution.objects.filter(roles__label="publisher"):
        agent = contribution.agent
        source_id = f"agent-{agent.id}"

        for c in contribution.resource.contributions.filter(
            roles__label__in=["author", "translator"]
        ):
            target = c.agent
            if target != agent:
                target_id = f"agent-{target.id}"

                nodes[source_id]["meta"]["published"].add(target.name)
                edges.append(
                    dict(source=source_id, target=target_id, label="published")
                )

        for rp in contribution.resource.places.all():
            p = rp.place
            if p:
                nodes[source_id]["meta"]["published_in"].add(p.address)
                edges.append(
                    dict(
                        source=source_id,
                        target=f"place-{p.id}",
                        label="published in (place)",
                    )
                )

    for contribution in Contribution.objects.filter(roles__label="editor"):
        agent = contribution.agent
        source_id = f"agent-{agent.id}"

        for c in contribution.resource.contributions.filter(
            roles__label__in=["author", "translator"]
        ):
            target = c.agent
            if target != agent:
                target_id = f"agent-{target.id}"

                nodes[source_id]["meta"]["edited"].add(target.name)
                edges.append(dict(source=source_id, target=target_id, label="edited"))

        for rp in contribution.resource.places.all():
            p = rp.place
            if p:
                nodes[source_id]["meta"]["published_in"].add(p.address)
                edges.append(
                    dict(
                        source=source_id,
                        target=f"place-{p.id}",
                        label="published in (place)",
                    )
                )

    for serial in Resource.objects.filter(subjects__label="Serial publications"):
        id = f"resource-{serial.id}"

        nodes[id] = dict(
            id=id,
            title=str(serial.title),
            group="serial publication",
            url=reverse("resource-detail", kwargs={"pk": serial.id}),
        )

        for contribution in serial.contributions.filter(roles__label="journalist"):
            source_id = f"agent-{contribution.agent.id}"
            edges.append(dict(source=source_id, target=id, label="member of"))

    data = dict(nodes=list(nodes.values()), edges=edges)

    with open("network.json", "w") as f:
        f.write(json.dumps(data, cls=NetworkObjectEncoder, indent=2))
