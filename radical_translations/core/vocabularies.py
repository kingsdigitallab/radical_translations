from controlled_vocabulary.vocabularies.base_csv import VocabularyBaseList


class VocabularyClassificationEdition(VocabularyBaseList):
    base_url = "http://id.loc.gov/ontologies/bibframe.html#p_edition"
    concept = "wikidata:Q324254:ontology"
    description = "BIBFRAME Classification scheme edition"
    label = "Classification scheme edition"
    prefix = "bf-cse"

    def _get_searchable_terms(self):
        return [
            ["abridged", "abridged"],
            ["adaptation", "adaptation"],
            ["announced", "announced"],
            ["extended", "extended"],
            ["integral", "integral"],
            ["partial", "partial"],
            ["pseudo-translation", "pseudo-translation"],
            ["self-translation", "self-translation"],
            ["summarised", "summarised"],
            ["unpublished", "unpublished"],
        ]


class VocabularyResourceRelationshipType(VocabularyBaseList):
    base_url = "http://id.loc.gov/ontologies/bibframe-category.html#gridTable27"
    concept = "wikidata:Q324254:ontology"
    description = "BIBFRAME Cataloging Resource Relationships"
    label = "Relationship type"
    prefix = "bf-crr"

    def _get_searchable_terms(self):
        return [
            [
                "derivativeOf",
                "derivative of",
                "Source work from which the described resource is derived.",
            ],
            [
                "instanceOf",
                "instance of",
                (
                    "Work the Instance described instantiates or manifests. For use to "
                    "connect Instances to Works in the BIBFRAME structure."
                ),
            ],
            [
                "itemOf",
                "item of",
                "Instance for which the described Item is an example.",
            ],
            [
                "otherEdition",
                "other edition",
                (
                    "Resource has other available editions, for example simultaneously "
                    "published language editions or reprints."
                ),
            ],
            [
                "paratextOf",
                "paratext of",
                (
                    "Resource in which the described resource is a paratext physically "
                    " or logically contained."
                ),
            ],
            [
                "partOf",
                "part of",
                (
                    "Resource in which the described resource is physically or "
                    "logically contained."
                ),
            ],
            [
                "relatedTo",
                "related to",
                "Any relationship between Work, Instance, and Item resources.",
            ],
            [
                "references",
                "references",
                "Resource that is referenced by the described resource.",
            ],
            [
                "translationOf",
                "translation of",
                (
                    "Resource that has been translated, i.e., the text is expressed in "
                    "a language different from that of the original resource."
                ),
            ],
        ]
