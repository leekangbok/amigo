class ModelBase:
    def __init__(self):
        self.uid = ''
        self.mod_date = 0
        self.reg_date = 0


class ModelResult:
    def __init__(self):
        self.success = 0
        self.message = ''
        self.count = 0
        self.total = 0
        self.params = {}


class ModelResponse:
    def __init__(self, item_cls, *args, **kwd):
        self.items = []
        self.item_cls = item_cls
        self.item_cls_args = args
        self.item_cls_kwd = kwd
        self.result = ModelResult()

    def add(self):
        n = self.item_cls(*self.item_cls_args, **self.item_cls_kwd)
        self.items.append(n)
        return n


class ModelRequest:
    _fields = ['page', 'rowsPerPage', 'sortBy', 'descending']

    def __init__(self, *args, item=None):
        self.item = item
        self.page = 0
        self.rowsPerPage = 9000000
        self.sortBy = ''
        self.descending = False

        for name, value in zip(self._fields, args):
            setattr(self, name, value)


class ModelDeleteRequest:
    def __init__(self, uids):
        if isinstance(uids, (str, bytes)):
            self.items = [uids]
        else:
            self.items = list(uids)


class TwistedRequestWrapper:
    def __init__(self):
        self.args = {}


def get_model_request_args(args):
    page = int(args.get('page', [0])[0])
    rowsPerPage = int(args.get('rowsPerPage', [9999999])[0])
    sortBy = args.get('sortBy', [''])[0]
    descending = args.get('descending', [False])[0]
    return page, rowsPerPage, sortBy, descending
