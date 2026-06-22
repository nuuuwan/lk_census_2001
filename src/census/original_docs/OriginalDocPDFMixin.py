import os
from functools import cached_property

from utils_future import WWW, File, Log

log = Log("OriginalDocPDFMixin")


class OriginalDocPDFMixin:
    DIR_ORIGINAL_DATA = "original_data"
    DIR_ORIGINAL_DATA_PDFS = os.path.join(DIR_ORIGINAL_DATA, "pdfs")

    @cached_property
    def pdf_file_path(self):
        return os.path.join(self.dir_data, "original.pdf")

    def download_pdf(self):
        if os.path.exists(self.pdf_file_path):
            log.debug(f"{File(self.pdf_file_path)} exists")
            return self.pdf_file_path
        www = WWW(self.url)
        os.makedirs(self.DIR_ORIGINAL_DATA_PDFS, exist_ok=True)
        www.download_binary(self.pdf_file_path)
        return self.pdf_file_path
