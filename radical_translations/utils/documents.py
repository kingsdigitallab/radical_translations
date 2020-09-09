from typing import Dict

from django_elasticsearch_dsl import fields


def get_agent_field():
    return fields.NestedField(
        properties={"id": fields.IntegerField(), "name": fields.TextField()}
    )


def get_controlled_term_properties() -> Dict:
    return {"termid": fields.KeywordField(), "label": fields.KeywordField()}


def get_place_properties() -> Dict:
    return {
        "address": fields.TextField(),
        "country": fields.ObjectField(properties={"name": fields.TextField()}),
    }


def get_resource_field():
    return fields.NestedField(
        properties={
            "id": fields.IntegerField(),
            "title": fields.ObjectField(properties={"main_title": fields.TextField()}),
        }
    )
