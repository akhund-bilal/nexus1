from pathlib import Path

from jinja2 import Template

HTML_TEMPLATE = """
<h1>OSINT Investigation Report</h1>
<h2>Case: {{ case_name }}</h2>
<p>{{ description }}</p>
<h3>Profiles</h3>
<ul>
{% for profile in profiles %}
  <li>{{ profile.platform }} - {{ profile.handle }} - {{ profile.profile_url }}</li>
{% endfor %}
</ul>
<h3>Risk</h3>
<p>Identity confidence: {{ risk.identity_confidence }} | Risk level: {{ risk.risk_level }}</p>
"""


def write_html_report(output_path: str, payload: dict) -> str:
    content = Template(HTML_TEMPLATE).render(**payload)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path)
