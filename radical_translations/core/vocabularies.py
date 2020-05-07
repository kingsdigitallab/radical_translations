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


class VocabularyRbmscv(VocabularyBaseList):
    base_url = "http://id.loc.gov/vocabulary/genreFormSchemes/rbmscv"
    concept = "wikidata:Q324254:ontology"
    description = (
        "Chicago: Rare Books and Manuscripts Section, Association of College and "
        "Research Libraries"
    )
    label = "RBMS controlled vocabularies"
    prefix = "rbmscv"

    def _get_searchable_terms(self):
        return [
            ["False imprint dates", "False imprint dates"],
            [
                "Forgeries",
                "Forgeries",
                (
                    "writings created or altered in fraudulent imitation of an author. "
                    "Use for: Counterfeits, Fakes"
                ),
            ],
            [
                "Imprint dates style",
                "Imprint dates style",
                "use for: Calendar styles, Dating styles (for revolutionary calendars)",
            ],
            ["Inserted text leaves", "Inserted text leaves"],
            ["Insertions", "Insertions"],
            [
                "Parts (Publishing)",
                "Parts (Publishing)",
                (
                    "the individually-published instalments of a work intended to be "
                    "bound together when complete. Use for: Fascicles, Installments"
                ),
            ],
            ["Piracies", "Piracies", "use for: Pirated editions"],
            [
                "Printer’s devices",
                "Printer’s devices",
                "use for: Publisher’s devices, Printer’s marks",
            ],
            [
                "Printer’s mottoes",
                "Printer’s mottoes",
                "use for: Publisher’s mottoes (for radical publishers)",
            ],
            [
                "Privately published books",
                "Privately published books",
                "books published for private distribution only",
            ],
            ["Series", "Series", "use for: Publisher’s series"],
            [
                "Banned works",
                "Banned works",
                (
                    "works which have been officially prohibited from distribution or "
                    "sale by a legal authority, civil or ecclesiastical"
                ),
            ],
            [
                "Bookseller’s advertisements",
                "Bookseller’s advertisements",
                (
                    "use this term rather than [Publisher’s advertisements] for "
                    "examples appearing before the roles of bookseller and publisher "
                    "were clearly differentiated"
                ),
            ],
            [
                "Bookseller’s catalogs",
                "Bookseller’s catalogs",
                (
                    "use this term rather than [Publisher’s catalogs] for examples "
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
