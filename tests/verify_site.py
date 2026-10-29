"""Check the static Pages artifact with Python's standard library."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import runpy


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


root = Path(__file__).resolve().parents[1] / "docs"
html = (root / "index.html").read_text(encoding="utf-8")
page = Page()
page.feed(html)
ids = [attrs["id"] for _, attrs in page.elements if "id" in attrs]
assert len(ids) == len(set(ids)), "Duplicate element IDs"
assert sum(tag == "h1" for tag, _ in page.elements) == 1, "Expected one H1"
assert any(tag == "html" and attrs.get("lang") == "en" for tag, attrs in page.elements)
assert any(tag == "html" and attrs.get("data-theme") == "azure-dark" for tag, attrs in page.elements), "Midnight must be the no-script default"
assert (root / ".nojekyll").is_file(), "Missing GitHub Pages marker"

for tag, attrs in page.elements:
    for attribute in ("href", "src"):
        if attribute not in attrs:
            continue
        value = attrs[attribute]
        assert value and value != "#", "Empty link destination"
        url = urlsplit(value)
        if not url.scheme and not url.netloc:
            assert not url.path.startswith("/"), f"Root-relative path breaks project Pages: {value}"
            path = (root / unquote(url.path)).resolve() if url.path else root / "index.html"
            assert path.is_relative_to(root.resolve()) and path.is_file(), f"Missing or escaping file: {value}"
            if url.fragment:
                assert url.fragment in ids, f"Missing anchor: {value}"
        if attrs.get("target") == "_blank":
            assert "noopener" in attrs.get("rel", ""), "External tab needs noopener"
    if tag == "img":
        assert attrs.get("alt") and attrs.get("width") and attrs.get("height"), "Image metadata missing"

assert "mailto:ricardo.mendez@gmail.com" in html
assert "https://play.google.com/store/apps/details?id=com.kimouse" in html
assert "https://play.google.com/store/apps/details?id=com.kiboard.kiboard_app" in html
assert "https://apps.microsoft.com/detail/9MTQZQJ9GDT4" in html
assert "https://www.agroerp.cl/" in html
assert "https://github.com/ricardomendezv" in html
assert {"kimouse-title", "kiboard-title", "agro-title", "agro-website-title"}.issubset(ids)
assert "reverse-work-title" in ids
assert "theme-select" in ids
assert "AgroERP Manager" in html and "AgroERP Website" in html
captures = {"kimouse-touchpad.png", "kimouse-keyboard.png", "kiboard-auto.png", "kiboard-launcher.png", "kiboard-windows-editor.png", "agroerp-manager.jpg", "agroerp-website.jpg"}
assert captures.issubset({Path(attrs.get("src", "")).name for tag, attrs in page.elements if tag == "img"})
assert not re.search(r"outvise\.com/account|portfolio-research|TODO|PLACEHOLDER", html, re.I)
assert [attrs.get("src") for tag, attrs in page.elements if tag == "script"] == ["./theme.js", "./language.js"]
assert (root / "assets/ricardo-mendez-cv-en.pdf").read_bytes().startswith(b"%PDF-")
assert not list(root.rglob("*.md")) and not list(root.rglob("*.json")), "Research files must stay out of docs"
print(f"PASS: {len(ids)} anchors, local assets, project links, CV, and Pages paths checked.")

spanish_html = (root / "es.html").read_text(encoding="utf-8")
spanish = Page()
spanish.feed(spanish_html)
assert any(tag == "html" and attrs.get("lang") == "es" for tag, attrs in spanish.elements)
assert [attrs["id"] for _, attrs in spanish.elements if "id" in attrs] == ids
for attribute in ("href", "src"):
    assert [attrs[attribute] for _, attrs in spanish.elements if attribute in attrs and attrs.get("rel") != "canonical"] == [attrs[attribute] for _, attrs in page.elements if attribute in attrs and attrs.get("rel") != "canonical"], "Both languages must retain assets, links and anchors"
assert any(attrs.get("rel") == "canonical" and attrs.get("href") == "https://ricardomendezv.github.io/" for _, attrs in page.elements)
assert any(attrs.get("rel") == "canonical" and attrs.get("href") == "https://ricardomendezv.github.io/es.html" for _, attrs in spanish.elements)
assert any(attrs.get("property") == "og:url" and attrs.get("content") == "https://ricardomendezv.github.io/es.html" for _, attrs in spanish.elements)
assert html.index('class="profile-card"') < html.index('class="hero-copy"'), "Personal introduction must lead the reading order"
assert html.index('id="experience"') < html.index('id="expertise"') < html.index('id="work"'), "Experience and skills must precede long project cases"
assert "language-select" in ids
assert "Problemas complejos." in spanish_html and "Soluciones que funcionan." in spanish_html
assert "Ingeniería inversa" in spanish_html and "Descargar CV (inglés)" in spanish_html
assert spanish_html.count("Google Play, de principio a fin.") == 2
assert "Electrónica militar legada" in spanish_html
generator = runpy.run_path(str(root.parent / "scripts/build_spanish.py"))
translated = generator["Spanish"]()
translated.feed(html)
assert not translated.missing, f"Untranslated copy: {translated.missing}"
assert "".join(translated.output) == spanish_html, "Regenerate es.html after changing English copy"
print("PASS: English default, complete Spanish copy, accessibility labels, identical project links/assets/anchors.")

gallery = Page()
gallery.feed((root / "themes.html").read_text(encoding="utf-8"))
themes = [attrs["value"] for tag, attrs in gallery.elements if tag == "input"]
assert len(themes) == len(set(themes)) == 10
assert sum(theme.endswith("-light") for theme in themes) == 5
assert sum(theme.endswith("-dark") for theme in themes) == 5
assert [attrs["value"] for tag, attrs in gallery.elements if tag == "input" and "checked" in attrs] == ["azure-dark"]
for tag, attrs in gallery.elements:
    for attribute in ("href", "src"):
        if attribute in attrs:
            url = urlsplit(attrs[attribute])
            assert not url.scheme and not url.netloc and not url.path.startswith("/")
            assert (root / url.path).is_file(), attrs[attribute]
    if attrs.get("target") == "_blank":
        assert "noopener" in attrs.get("rel", "")

def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return sum(c * weight for c, weight in zip(linear, (.2126, .7152, .0722)))

def contrast(first, second):
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + .05) / (low + .05)

css = (root / "themes.css").read_text(encoding="utf-8")
minimum = 21
for theme in themes:
    block = re.search(r'\[data-theme="' + theme + r'"\]\s*\{([^}]+)\}', css).group(1)
    colors = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-f]{6})(?:;|\s)", block))
    pairs = [(text, bg) for text in ("ink", "muted", "accent") for bg in ("paper", "white", "soft", "contact")]
    pairs += [("accent", "accent-soft"), ("stage-ink", "stage"), ("stage-muted", "stage"), ("stage-accent", "stage")]
    for text, bg in pairs:
        ratio = contrast(colors[text], colors[bg])
        minimum = min(minimum, ratio)
        assert ratio >= 4.5, f"Low text contrast: {theme} {text}/{bg}: {ratio:.2f}"
print(f"PASS: 10 unique themes (5 light / 5 dark), gallery paths, text contrast >= {minimum:.2f}:1.")
