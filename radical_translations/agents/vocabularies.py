from controlled_vocabulary.vocabularies.base_http import VocabularyHTTP


class VocabularyRelatorsScheme(VocabularyHTTP):
    """Relator terms and their associated codes designate the relationship between a
    name and a bibliographic resource. The relator codes are three-character lowercase
    alphabetic strings that serve as identifiers. Either the term or the code may be
    used as controlled values."""

    base_url = "http://id.loc.gov/vocabulary/relators/"
    concept = "wikidata:Q324254:ontology"
    description = "MARC Code List for Relators Scheme"
    label = "Relators Scheme"
    prefix = "relators"
    source = {
        "url": (
            "http://id.loc.gov/search/?q=*{pattern}*"
            "&q=cs%3Ahttp%3A%2F%2Fid.loc.gov%2Fvocabulary%2Frelators&format=json"
        ),
        "minimum_length": 1,
    }

    def parse_search_response(self, res):
        ret = []

        for doc in res:
            if isinstance(doc, list) and doc[0] == "atom:entry":
                href = doc[3][1]["href"]
                ret.append([self._get_clean_id(href), doc[2][2], href])

        return ret

    def _get_clean_id(self, href):
        term_id = href.split("/")[-1]

        return int("".join([str(ord(c)) for c in term_id]))
