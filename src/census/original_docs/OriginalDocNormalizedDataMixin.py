import os
from functools import cached_property


class OriginalDocNormalizedDataMixin:

    @cached_property
    def normalized_data_path(self):
        return os.path.join(self.dir_data, "normalized_data.json")

    def build_normalized(self):
        data_list = self.get_data_list()
        return data_list
