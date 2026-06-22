class OriginalDocLoaderMixin:
    @classmethod
    def list(cls):
        metadata = cls.read_metadata()
        return [cls(**item) for item in metadata]
