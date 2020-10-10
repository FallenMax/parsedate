import dateparser
from flask import Flask, request

app = Flask(__name__)

routes = {
    '/': '/',
    '/parse': '/parse',
    '/parse/batch': '/parse/batch',
}


def ok(result):
    return {'ok': True, 'result': result}


def fail(reason):
    return {'ok': False, 'reason': reason}


def get_payload():
    args = request.args.to_dict()
    json = request.get_json()
    if json is None:
        return args
    if len(args) is 0:
        return json
    payload = {
        **args,
        **json
    }
    return payload


def parse_date(text):
    date = dateparser.parse(text)
    if date is None:
        return None
    return date.isoformat()


@app.route(routes['/'])
def index():
    return ok({'api': routes})


@app.route(routes['/parse'], methods=['GET', 'POST'])
def parse():
    payload = get_payload()
    text = payload.get("text")
    if not isinstance(text, str):
        return fail("'text' is expected to be a string")

    date = parse_date(text)

    if date is None:
        return fail("failed to parse")

    return ok({
        'text': text,
        'date': date,
    })


MAX_ITEMS_PER_REQUEST = 100


@app.route(routes['/parse/batch'], methods=['GET', 'POST'])
def batchParse():
    payload = get_payload()
    texts = payload.get("list")
    if not isinstance(texts, list):
        return fail("'list' is expected to be list of strings")

    if len(texts) > MAX_ITEMS_PER_REQUEST:
        return fail("cannot process more than {} items at one time".format(MAX_ITEMS_PER_REQUEST))

    total = len(texts)
    success = 0
    results = []
    for text in texts:
        date = parse_date(text)
        if date is not None:
            success = success+1
        results.append({'text': text, 'date': date})
    return ok(
        {
            'total': total,
            'success': success,
            'results': results
        }
    )


if __name__ == '__main__':
    app.run()
