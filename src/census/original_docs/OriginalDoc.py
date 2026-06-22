from census.original_docs.OriginalDocBase import OriginalDocBase
from census.original_docs.OriginalDocBuilderMixin import (
    OriginalDocBuilderMixin,
)
from census.original_docs.OriginalDocDataMixin import OriginalDocDataMixin
from census.original_docs.OriginalDocLoaderMixin import OriginalDocLoaderMixin
from census.original_docs.OriginalDocPDFMixin import OriginalDocPDFMixin
from census.original_docs.OriginalDocRawDataMixin import (
    OriginalDocRawDataMixin,
)
from census.original_docs.OriginalDocReadmeMixin import OriginalDocReadmeMixin
from census.original_docs.OriginalDocScrapeMixin import OriginalDocScrapeMixin
from census.original_docs.OriginalDocValidateMixin import (
    OriginalDocValidateMixin,
)
from utils_future import Log

log = Log("OriginalDoc")


class OriginalDocTSVMixin:
    def build_tsv(self):
        pass


class OriginalDoc(
    OriginalDocBase,
    OriginalDocLoaderMixin,
    #
    OriginalDocScrapeMixin,
    OriginalDocBuilderMixin,
    OriginalDocPDFMixin,
    OriginalDocRawDataMixin,
    OriginalDocDataMixin,
    OriginalDocTSVMixin,
    OriginalDocReadmeMixin,
    OriginalDocValidateMixin,
    #
):

    pass
