from typing import List

from controlled_vocabulary.vocabularies.base_csv import VocabularyBaseList
from controlled_vocabulary.vocabularies.base_http import VocabularyHTTP


class VocabularyPrintingPublishingTerms(VocabularyBaseList):
    base_url = "http://rbms.info/vocabularies/printing-publishing/alphabetical_list.htm"
    concept = "wikidata:Q324254:ontology"
    description = "Printing and Publishing Terms (in addition to FAST topic/forms)"
    label = "Printing and Publishing Terms"
    prefix = "rt-ppt"

    def _get_searchable_terms(self) -> List:
        return [
            [
                "Forgeries",
                "Forgeries",
                (
                    "writings created or altered in fraudulent imitation of an author. "
                    "Use for: Counterfeits, Fakes"
                ),
            ],
            [
                "New edition",
                "New edition",
                (
                    "use for previously published translation reprinted with new "
                    "paratextual materials"
                ),
            ],
            ["Piracies", "Piracies", "use for: Pirated editions"],
            [
                "Privately published books",
                "Privately published books",
                "books published for private distribution only",
            ],
            ["Projected", "Projected", "use for announced translations"],
            ["Re-issues", "Re-issues"],
            [
                "Simultaneous issues",
                "Simultaneous issues",
                (
                    "use for evidence of a book being published in two or more issues "
                    "simultaneously, whether in source language or translation"
                ),
            ],
        ]


class VocabularyAdditionalGenreTerms(VocabularyBaseList):
    base_url = "https://rbms.info/vocabularies/genre/alphabetical_list.htm"
    concept = "wikidata:Q324254:ontology"
    description = "Additional Genre Terms (in addition to FAST topic/forms)"
    label = "Additional Genre Terms"
    prefix = "rt-agt"

    def _get_searchable_terms(self) -> List:

        return [
            [
                "Banned works",
                "Banned works",
                (
                    "works which have been officially prohibited from distribution or "
                    "sale by a legal authority, civil or ecclesiastical"
                ),
            ],
            [
                "Bookseller's advertisements",
                "Bookseller's advertisements",
                (
                    "use this term rather than [Publisher's advertisements] for "
                    "examples appearing before the roles of bookseller and publisher "
                    "were clearly differentiated"
                ),
            ],
            [
                "Bookseller's catalogs",
                "Bookseller's catalogs",
                (
                    "use this term rather than [Publisher's catalogs] for examples "
                    "appearing before the roles of bookseller and publisher were "
                    "clearly differentiated"
                ),
            ],
            [
                "Book prospectuses",
                "Book prospectuses",
                (
                    "printed descriptions or accounts, sometimes incorporating sample "
                    "text or specimen pages, issued separately or as part of books or "
                    "periodicals, to solicit subscription, purchase, or other "
                    "patronage of forthcoming books"
                ),
            ],
            [
                "Censored works",
                "Censored works",
                (
                    "works that have been altered, prohibited, or suppressed because "
                    "of allegedly objectionable content (used for: Censored books, "
                    "Prohibited books/works, Banned books/works, Condemned works, "
                    "Expurgated editions, Bowdlerized books)"
                ),
            ],
            [
                "Underground literature",
                "Underground literature",
                "use for Clandestine publications",
            ],
            [
                "Unfinished works",
                "Unfinished works",
                "works not finished by the author",
            ],
        ]


class VocabularyTranslationTerms(VocabularyBaseList):
    concept = "wikidata:Q324254:ontology"
    description = "Translation terms"
    label = "Translation terms"
    prefix = "rt-tt"

    def _get_searchable_terms(self) -> List:
        return [
            [
                "Abridged",
                "Abridged",
                (
                    "use for: Summarised, Condensed; cases where the translation "
                    "presents itself as covering the whole source text but in fact "
                    "includes ellipses and compressions"
                ),
            ],
            [
                "Adapted",
                "Adapted",
                (
                    "use for evidence of substantial rewriting, source text "
                    "significantly reshaped"
                ),
            ],
            [
                "Compilation",
                "Compilation",
                (
                    "presents texts not originally published together, or parts "
                    "thereof, by the same or different authors (do not use if source "
                    "text is listed a Literary collection under FAST Forms)"
                ),
            ],
            ["Extended", "Extended", "includes additional material, new or translated"],
            [
                "Indirect translation",
                "Indirect translation",
                "translation of a translation",
            ],
            ["Integral", "Integral"],
            ["Source-text", "Source-text"],
            [
                "Partial",
                "Partial",
                (
                    "one or more extracts from source text are translated in their "
                    "entirety (e.g. ‘Profession de foi' from Emile), no attempt to "
                    "render the whole source text"
                ),
            ],
            [
                "Pseudo-translation",
                "Pseudo-translation",
                "original work presented as translation",
            ],
            ["Self-translation", "Self-translation", "use for: Autotranslation"],
            [
                "Simplified",
                "Simplified",
                (
                    "when perceived complexities of language or content are removed "
                    "to make text more comprehensible"
                ),
            ],
            [
                "Retranslation",
                "Retranslation",
                (
                    "new translation of source text already available in target "
                    "language (note for the purposes of this project, re-translation "
                    "differs significantly from re-edition: ‘Whereas re-edition would "
                    "tend to reinforce the validity of the previous translation, "
                    "re-translation strongly challenges that validity [Pym, 83])"
                ),
            ],
            ["Unknown", "Unknown"],
            ["Unpublished", "Unpublished"],
        ]


class VocabularyParatextTerms(VocabularyBaseList):
    concept = "wikidata:Q324254:ontology"
    description = "Paratext terms (adapted from Nottingham-Martin and Batchelor)"
    label = "Paratext terms"
    prefix = "rt-pt"

    def _get_searchable_terms(self) -> List:
        return [
            ["Appendix", "Appendix"],
            [
                "Community-building",
                "Community-building",
                "referencing groups of readers (imaginary or actual)",
            ],
            ["Dedication", "Dedication"],
            ["Epigraph", "Epigraph"],
            ["False imprint date", "False imprint date"],
            ["False imprint", "False imprint"],
            ["Ficticious imprint", "Ficticious imprint"],
            [
                "Hermeneutical",
                "Hermeneutical",
                "presenting an in-depth commentary and interpretation of ST",
            ],
            [
                "Meta-communicative",
                "Meta-communicative",
                (
                    "reflecting on the conditions and constraints of communication "
                    "and translation"
                ),
            ],
            [
                "Misattributed",
                "Misattributed",
                (
                    "elements of paratext attributed to person other than who actually "
                    "wrote them (specify in Notes)"
                ),
            ],
            [
                "New translation",
                "New translation",
                "text translated for the first time in a given target language",
            ],
            ["Notes", "Notes"],
            ["Postface", "Postface"],
            ["Preface", "Preface"],
            [
                "Radical marker on title page",
                "Radical marker on title page",
                "e.g. printer’s motto or marks - specify in Notes",
            ],
            ["Revolutionary calendar used", "Revolutionary calendar used"],
            [
                "Text-activating",
                "Text-activating",
                (
                    "removing epistemic obstacles to the reader’s understanding, "
                    "clarifying culture-specific references, reframing text for "
                    "situated audience"
                ),
            ],
        ]


class VocabularyResourceRelationshipType(VocabularyBaseList):
    base_url = "http://id.loc.gov/ontologies/bibframe-category.html#gridTable27"
    concept = "wikidata:Q324254:ontology"
    description = "BIBFRAME Cataloging Resource Relationships"
    label = "Relationship type"
    prefix = "bf-crr"

    def _get_searchable_terms(self) -> List:
        return [
            [
                "derivativeOf",
                "derivative of",
                "Source work from which the described resource is derived.",
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


class VocabularyCERL(VocabularyHTTP):
    prefix = "cerl"
    label = "CERL"
    base_url = "http://thesaurus.cerl.org/record/"
    concept = "wikidata:Q35120:entity"
    description = """Consortium of European Research Libraries"""

    source = {
        "url": "https://data.cerl.org/thesaurus/_search?format=json&query={pattern}"
    }

    def parse_search_response(self, response):
        ret = []

        for doc in response["rows"]:
            ret.append(
                [doc["id"], doc["name_display_line"], doc["additional_display_line"]]
            )

        return ret
