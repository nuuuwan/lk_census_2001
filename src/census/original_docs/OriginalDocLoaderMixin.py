class OriginalDocLoaderMixin:
    @classmethod
    def list(cls):
        metadata = cls.read_metadata()
        return [cls(name=item["name"], url=item["url"]) for item in metadata]
