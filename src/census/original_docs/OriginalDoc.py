from census.original_docs.OriginalDocBase import OriginalDocBase
from census.original_docs.OriginalDocLoaderMixin import OriginalDocLoaderMixin
from census.original_docs.OriginalDocMetadataMixin import (
    OriginalDocMetadataMixin,
)
from census.original_docs.OriginalDocParserMixin import OriginalDocParserMixin
from census.original_docs.OriginalDocPDFMixin import OriginalDocPDFMixin
from census.original_docs.OriginalDocScrapeMixin import OriginalDocScrapeMixin
from utils_future import Log

log = Log("OriginalDoc")


class OriginalDoc(
    OriginalDocBase,
    OriginalDocScrapeMixin,
    OriginalDocPDFMixin,
    OriginalDocParserMixin,
    OriginalDocMetadataMixin,
    OriginalDocLoaderMixin,
):

    pass
