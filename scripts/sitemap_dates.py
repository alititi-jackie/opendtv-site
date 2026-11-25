"""Keep lastmod tied to significant page content across scheduled builds."""
from datetime import date, datetime
from hashlib import sha256
from pathlib import Path
import json
import re

from model import ROOT


def fingerprint(markup):
    # Exclude shared navigation, analytics, style and social preview metadata.
    parts = re.findall(r'<title>.*?</title>|<meta name="description"[^>]+>|<main\b.*?</main>|<script type="application/ld\+json">.*?</script>', markup, re.S)
    return sha256('\n'.join(parts).encode()).hexdigest()


def page_path(directory, url):
    return directory / (url.lstrip('/') + ('index.html' if url.endswith('/') else ''))


def dates_for(out, urls):
    baseline = json.loads((ROOT / 'data/sitemap-baseline.json').read_text())
    previous = ROOT / 'health-output/published-dates.json'
    history = json.loads(previous.read_text()) if previous.is_file() else baseline
    today = datetime.now().astimezone().date().isoformat()
    result = {}
    for url in urls:
        digest = fingerprint(page_path(out,url).read_text())
        last = history.get(url) or baseline.get(url)
        modified = today
        if last and last[0] == digest:
            modified = date.fromisoformat(last[1]).isoformat()
        result[url] = [digest, modified]
    (out/'page-dates.json').write_text(json.dumps(result, sort_keys=True))
    return {url: values[1] for url, values in result.items()}
