class OriginalDocBuilderMixin:
    def build(self):
        self.write_metadata()
        self.download_pdf()
        self.build_raw_data()
        self.build_data()
        self.build_tsv()
        self.build_normalized()
        self.build_readme()
