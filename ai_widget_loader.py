import json
import os
import re
from IPython.display import display, HTML

_WIDGET_DIR = os.path.dirname(os.path.abspath(__file__))
_WIDGET_HTML = os.path.join(_WIDGET_DIR, "ai_widget.html")


def _site_url_from_config() -> str:
    """Derive the GitHub Pages URL from _config.yml repository.url."""
    config_path = os.path.join(_WIDGET_DIR, "_config.yml")
    try:
        with open(config_path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        return ""

    # find repository.url value
    m = re.search(r"repository\s*:\s*\n(?:.*\n)*?\s+url\s*:\s*(\S+)", text)
    if not m:
        return ""

    repo_url = m.group(1).strip()  # e.g. https://github.com/hag007/virtual-pyprog

    # convert https://github.com/{user}/{repo} → https://{user}.github.io/{repo}
    gh = re.match(r"https://github\.com/([^/]+)/([^/\s]+)", repo_url)
    if gh:
        return f"https://{gh.group(1)}.github.io/{gh.group(2)}"

    return repo_url  # fallback: return as-is if not a github.com URL


def load_ai_widget() -> None:
    """Display the AI widget. Site URL is auto-detected from _config.yml."""
    site_url = _site_url_from_config()

    with open(_WIDGET_HTML, encoding="utf-8") as f:
        widget_html = f.read()

    inject = (
        "<script>\n"
        f"window.AI_SITE_URL = {json.dumps(site_url)};\n"
        "</script>\n"
    )

    display(HTML(inject + widget_html))
