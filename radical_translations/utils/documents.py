from typing import Dict, Optional

from django_elasticsearch_dsl import fields


def get_agent_field(options: Optional[Dict] = {}) -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(
                fields={
                    "raw": fields.KeywordField(),
                    "suggest": fields.CompletionField(),
                },
                **options
            ),
        }
    )


def get_controlled_term_field(options: Optional[Dict] = {}) -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "label": fields.TextField(fields={"raw": fields.KeywordField()}, **options)
        }
    )


def get_event_field(options: Optional[Dict] = {}) -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.TextField(fields={"raw": fields.KeywordField()}, **options),
            "place": get_place_field(),
        }
    )


def get_place_field(options: Optional[Dict] = {}) -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "address": fields.TextField(
                fields={"raw": fields.KeywordField()}, **options
            ),
            "country": fields.ObjectField(
                properties={
                    "name": fields.TextField(
                        fields={"raw": fields.KeywordField()}, **options
                    )
                }
            ),
        }
    )


def get_resource_field(options: Optional[Dict] = {}) -> fields.ObjectField:
    return fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.ObjectField(
                properties={"main_title": fields.TextField(**options)}
            ),
        }
    )
