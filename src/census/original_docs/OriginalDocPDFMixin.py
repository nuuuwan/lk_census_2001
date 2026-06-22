import os

from utils_future import WWW, File, Log

log = Log("OriginalDocPDFMixin")


class OriginalDocPDFMixin:
    DIR_ORIGINAL_DATA = "original_data"
    DIR_ORIGINAL_DATA_PDFS = os.path.join(DIR_ORIGINAL_DATA, "pdfs")

    def download_pdf(self):
        basename = os.path.basename(self.url)
        pdf_path = os.path.join(self.DIR_ORIGINAL_DATA_PDFS, basename)
        if os.path.exists(pdf_path):
            log.debug(f"{File(pdf_path)} exists")
            return pdf_path
        www = WWW(self.url)
        os.makedirs(self.DIR_ORIGINAL_DATA_PDFS, exist_ok=True)
        www.download_binary(pdf_path)
        return pdf_path
