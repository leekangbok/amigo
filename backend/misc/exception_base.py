from contextlib import contextmanager


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def exception_message(e):
    s, r = getattr(e, 'message', str(e)), getattr(e, 'message', repr(e))
    return s


@contextmanager
def serv_err_handler(resp, log, errmsg):
    try:
        yield
    except Exception as e:
        log.error('Oops! {errmsg}: {e!r}', errmsg=errmsg, e=e)
        resp.result.success = 0
        resp.result.message = exception_message(e)
    else:
        resp.result.success = 1
        resp.result.message = 'good'
