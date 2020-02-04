from controlled_vocabulary.vocabularies.base_csv import VocabularyBaseCSV


class VocabularyResourceRelationshipType(VocabularyBaseCSV):
    base_url = "http://id.loc.gov/ontologies/bibframe-category.html#gridTable27"
    concept = "wikidata:Q324254:ontology"
    description = "BIBFRAME Cataloging Resource Relationships"
    label = "Relationship type"
    prefix = "bf-crr"
    source = {
        "url": "http://django:8000/static/vocabularies/resource_relationship_type.csv",
        "delimiter": ",",
    }

    def _get_term_from_csv_line(self, line):
        return [line[0], line[1]]
