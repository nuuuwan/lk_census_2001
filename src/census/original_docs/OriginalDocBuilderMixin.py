class OriginalDocBuilderMixin:
    def build(self):
        self.write_metadata()
        self.download_pdf()
        self.parse_pdf()
        self.parse_raw_data()
