from backend.database.model.model_base import ModelBase
from backend.database.sqlite3_base import get_sqlite3_all_column_name


class Consulting(ModelBase):
    _fields = list(get_sqlite3_all_column_name('Consulting'))

    def __init__(self, *args, **kwd):
        super().__init__()

        for name in self._fields:
            setattr(self, name, None)
        self.author = 'Anonymous'

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        if kwd:
            for name in self._fields:
                setattr(self, name, kwd.pop(name, None))
            extra_args = kwd.keys() - self._fields
            for name in extra_args:
                setattr(self, name, kwd.pop(name, None))


class ConsultingReply(ModelBase):
    _fields = list(get_sqlite3_all_column_name('ConsultingReply'))

    def __init__(self, *args, **kwd):
        super().__init__()

        for name in self._fields:
            setattr(self, name, None)
        self.author = 'Anonymous'

        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        if kwd:
            for name in self._fields:
                setattr(self, name, kwd.pop(name, None))
            extra_args = kwd.keys() - self._fields
            for name in extra_args:
                setattr(self, name, kwd.pop(name, None))
