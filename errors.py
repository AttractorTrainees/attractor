from factory import SessionFactory
from factory import ResponseFactory
from new_template_engine import TemplateEngine
from tempate_engine import render
from settings import TEMPLATES_DIR, database
import os
from settings import CODE_200, OK, TEXT_HTML, CONTENT_TYPE

LOGIN_FAILED_ERROR = 1
EDIT_PERMISSION_DENIED_ERROR = 2
CREATE_PERMISSION_DENIED_ERROR = 3

sessionFactory = SessionFactory()
responseFactory = ResponseFactory()

_blog_codes = {
    LOGIN_FAILED_ERROR: ('Вы ввели неверную комбинацию логина и пароля.'),
    EDIT_PERMISSION_DENIED_ERROR: ('У вас недостаточно прав редактировать эту запись.'),
    CREATE_PERMISSION_DENIED_ERROR: ('У вас недостаточно прав для добавления записи.'),
    4: (),
    5: ()
}


def login_required(error_code):
    def login_checker(handler):
        def login_check(request, id):
            article = database.get_article('id', int(id))
            print(article, id)
            if article:
                user = sessionFactory.createSession(request).find_session()
                print('user->', user)
                if user:
                    if article.author == user:
                        return handler(request, id)
                    else:
                        return valid_error(error_code, user)
                else:
                    return valid_error(error_code, user)
            else:
                return handler_error(request, 404)

        def login_check_add(request):
            user = sessionFactory.createSession(request)
            user = user.find_session()
            if user:
                return handler(request)
            else:
                return valid_error(error_code, user)

        if error_code == 2:
            return login_check
        elif error_code == 3:
            return login_check_add
        else:  # создать exception
            return handler_error(404)

    return login_checker


def valid_error(code, user):
    error = _blog_codes[code]
    context = {'title': error, 'Error': error, 'user': user}
    body = TemplateEngine.render_template('info.html', context)
    response = responseFactory.createResponse(body)
    response.set_header(CONTENT_TYPE, TEXT_HTML)
    response.set_code(CODE_200)
    response.set_status(OK)
    return response


_codes = {

    # Informational.
    100: ('continue',),
    101: ('switching_protocols',),
    102: ('processing',),
    103: ('checkpoint',),
    122: ('uri_too_long', 'request_uri_too_long'),
    200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
    201: ('created',),
    202: ('accepted',),
    203: ('non_authoritative_info', 'non_authoritative_information'),
    204: ('no_content',),
    205: ('reset_content', 'reset'),
    206: ('partial_content', 'partial'),
    207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
    208: ('already_reported',),
    226: ('im_used',),

    # Redirection.
    300: ('multiple_choices',),
    301: ('moved_permanently', 'moved', '\\o-'),
    302: ('found',),
    303: ('see_other', 'other'),
    304: ('not_modified',),
    305: ('use_proxy',),
    306: ('switch_proxy',),
    307: ('temporary_redirect', 'temporary_moved', 'temporary'),
    308: ('permanent_redirect',
          'resume_incomplete', 'resume',),  # These 2 to be removed in 3.0

    # Client Error.
    400: ('bad_request', 'bad'),
    401: ('unauthorized',),
    402: ('payment_required', 'payment'),
    403: ('forbidden',),
    404: ('not_found', '-o-'),
    405: ('method_not_allowed', 'not_allowed'),
    406: ('not_acceptable',),
    407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
    408: ('request_timeout', 'timeout'),
    409: ('conflict',),
    410: ('gone',),
    411: ('length_required',),
    412: ('precondition_failed', 'precondition'),
    413: ('request_entity_too_large',),
    414: ('request_uri_too_large',),
    415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
    416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
    417: ('expectation_failed',),
    418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
    421: ('misdirected_request',),
    422: ('unprocessable_entity', 'unprocessable'),
    423: ('locked',),
    424: ('failed_dependency', 'dependency'),
    425: ('unordered_collection', 'unordered'),
    426: ('upgrade_required', 'upgrade'),
    428: ('precondition_required', 'precondition'),
    429: ('too_many_requests', 'too_many'),
    431: ('header_fields_too_large', 'fields_too_large'),
    444: ('no_response', 'none'),
    449: ('retry_with', 'retry'),
    450: ('blocked_by_windows_parental_controls', 'parental_controls'),
    451: ('unavailable_for_legal_reasons', 'legal_reasons'),
    499: ('client_closed_request',),

    # Server Error.
    500: ('internal_server_error', 'server_error', '/o\\', '✗'),
    501: ('not_implemented',),
    502: ('bad_gateway',),
    503: ('service_unavailable', 'unavailable'),
    504: ('gateway_timeout',),
    505: ('http_version_not_supported', 'http_version'),
    506: ('variant_also_negotiates',),
    507: ('insufficient_storage',),
    509: ('bandwidth_limit_exceeded', 'bandwidth'),
    510: ('not_extended',),
    511: ('network_authentication_required', 'network_auth', 'network_authentication')
}


def handler_error(request=None, *args):
    template = 'error.html'

    code = args[0]

    status_code = str(code)
    status_text = _codes[code][0].upper()
    error = {'title': status_code + status_text, 'code': status_code, 'status': status_text}
    status_code = status_code
    status_text = status_text
    body = render(os.path.join(TEMPLATES_DIR, template), error)
    response = responseFactory.createResponse(body)
    response.set_code(status_code)
    response.set_status(status_text)
    return response

