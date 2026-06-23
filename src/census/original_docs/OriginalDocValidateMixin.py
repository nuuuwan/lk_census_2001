import os

from utils_future import Log

log = Log("OriginalDocValidateMixin")


class OriginalDocValidateMixin:
    @classmethod
    def validate_status(cls):
        docs = cls.list()
        group_to_doc_id = {}
        for doc in docs:
            if os.path.exists(doc.data_file_path):
                status = "🟢 data"
            elif os.path.exists(doc.raw_data_file_path):
                status = "🟠 raw_data"
            elif os.path.exists(doc.pdf_file_path()):
                status = "🟡 pdf"
            else:
                status = "🔴 no files."

            if status not in group_to_doc_id:
                group_to_doc_id[status] = []

            group_to_doc_id[status].append(doc.doc_id)

        for group, doc_ids in group_to_doc_id.items():
            log.debug(f"{group}: {len(doc_ids)} docs")
            for doc_id in doc_ids:
                log.debug(f"\t{doc_id}")
