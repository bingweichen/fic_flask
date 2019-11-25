from flask import request
from flask import g
from functools import wraps
from common.responses import internal_error
from common.errors import DataRetrievalFailureException, \
    NotMatchOrUserDoesNotExistsError, UserAlreadyExistError
from common.responses import not_found, bad_request
from flask_records.decorators import query
from common.errors import DataRetrievalFailureException


def arguments_parser(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        post_data = request.json
        get_data = request.args
        g.args = post_data if post_data else {}
        _args_get = get_data if get_data else {}
        g.args.update(_args_get)
        return func(*args, **kwargs)

    return decorated


def catch_error(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DataRetrievalFailureException as e:
            return not_found(e.message)
        except NotMatchOrUserDoesNotExistsError as e:
            return not_found(e.message)
        except UserAlreadyExistError as e:
            return bad_request(e.message)

    return _wrapper


# not used
# def kylin_get(sql=None):
#     if not sql:
#         raise Exception('No sql provided')
#
#     @query(sql)
#     def _get():
#         pass
#
#     rows = _get()
#     # result = pd.DataFrame(_get().as_dict())
#     result = rows.export('df')
#     # todo: if df is empty
#     if len(result) == 0:
#         raise DataRetrievalFailureException
#
#     return result
