from werkzeug.utils import cached_property
from werkzeug.contrib.securecookie import SecureCookie
from flask import Flask as _Flask, Request as _Request, request, Response


SECRET_KEY = 'SECRET_KEY'


class Request(_Request):

    @cached_property
    def client_session(self):
        return SecureCookie.load_cookie(self, secret_key=SECRET_KEY)


class Flask(_Flask):
    request_class = Request


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


def get_cookie():
    return request.cookies


def get_secure_cookie():
    return request.client_session


def generate_value(cookie):
    try:
        value = int(cookie.get('count'))
    except Exception:
        value = 0
    else:
        value += 1
    return value


@app.route('/')
@app.route('/index')
def index():
    return 'hello flask'


@app.route('/set_cookie')
def set_cookie():
    """设置cookie"""
    cookies = get_cookie()
    print(cookies)

    value = generate_value(cookies)

    response = Response()
    response.set_cookie('count', str(value))

    response.set_data(
        'request cookies:<br>' + str(request.cookies) + '<br><br>' +
        'response header:<br>' + str(response.headers)
    )
    return response


@app.route('/set_secure_cookie')
def set_secure_cookie():
    # get cookies
    cookies = get_cookie()
    print(cookies)

    # get secure cookie
    # default key is 'session'
    secure_cookie = get_secure_cookie()
    print(secure_cookie)  # request secure_cookie

    value = generate_value(secure_cookie)

    secure_cookie['count'] = value  # set secure cookie

    response = Response()
    secure_cookie.save_cookie(response)
    # print(secure_cookie)  # response secure_cookie

    response.set_data(
        'request cookies:<br>' + str(request.cookies) + '<br><br>' +
        'response header:<br>' + str(response.headers)
    )
    return response


@app.route('/delete_cookie')
def delete_cookie():
    """删除cookie"""
    key = request.args.get('key') or 'count'
    cookies = request.cookies
    print(cookies)
    response = Response()
    response.delete_cookie(key)
    response.set_data(
        'request cookies:<br>' + str(request.cookies) + '<br><br>' +
        'response header:<br>' + str(response.headers)
    )
    return response


if __name__ == "__main__":
    app.run(debug=True)
