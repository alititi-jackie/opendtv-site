"""Read individually edited viewing notes and preserve their source links."""
from html import escape
from model import DATA


def records(name):
    rows = {}
    for line in (DATA / 'editorial' / (name + '.txt')).read_text().splitlines():
        key, *fields = line.split('|')
        if key in rows:
            raise ValueError('Duplicate editorial entry: ' + key)
        rows[key] = fields
    return rows


def article(sections):
    return '<article class="reading">' + ''.join(
        '<h2>' + escape(title) + '</h2><p>' + escape(body) + '</p>'
        for title, body in sections
    ) + '</article>'
