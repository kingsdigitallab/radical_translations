from django_elasticsearch_dsl import fields


def get_agent_field() -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(
                fields={
                    "raw": fields.KeywordField(),
                    "suggest": fields.CompletionField(),
                }
            ),
        }
    )


def get_controlled_term_field() -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "termid": fields.KeywordField(),
            "label": fields.TextField(fields={"raw": fields.KeywordField()}),
        }
    )


def get_event_field() -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.TextField(fields={"raw": fields.KeywordField()}),
            "place": get_place_field(),
        }
    )


def get_place_field() -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "address": fields.TextField(fields={"raw": fields.KeywordField()}),
            "country": fields.ObjectField(
                properties={
                    "name": fields.TextField(fields={"raw": fields.KeywordField()})
                }
            ),
        }
    )


def get_resource_field() -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.ObjectField(properties={"main_title": fields.TextField()}),
        }
    )
