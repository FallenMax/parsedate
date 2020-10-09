import dateparser
from flask import Flask, request

app = Flask(__name__)

routes = {
    '/': '/',
    '/parse': '/parse'
}


def ok(result):
    return {'ok': True, 'result': result}


def fail(reason):
    return {'ok': False, 'reason': reason}


@app.route(routes['/'])
def home():
    return ok(routes)


@app.route(routes['/parse'])
def parse():
    text = request.args.get("text")
    if text is None:
        return fail("'text' required")

    date = dateparser.parse(text)
    if date is None:
        return fail("failed to parse: {}".format(text))

    return ok({
        'text': text,
        'date': date.isoformat(),
        'timestamp': date.timestamp()
    })


if __name__ == '__main__':
    app.run()
