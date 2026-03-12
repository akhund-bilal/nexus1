import csv
import json
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
<h3>Findings</h3>
<ul>
{% for finding in findings %}
  <li>[{{ finding.severity }}] {{ finding.title }} - {{ finding.description }}</li>
{% endfor %}
</ul>
"""


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_html_report(output_path: str, payload: dict) -> str:
    content = Template(HTML_TEMPLATE).render(**payload)
    path = Path(output_path)
    _ensure_parent(path)
    path.write_text(content, encoding="utf-8")
    return str(path)


def write_json_report(output_path: str, payload: dict) -> str:
    path = Path(output_path)
    _ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)


def write_csv_report(output_path: str, payload: dict) -> str:
    path = Path(output_path)
    _ensure_parent(path)

    profiles = payload.get("profiles", [])
    findings = payload.get("findings", [])

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["section", "field_a", "field_b", "field_c"])
        for p in profiles:
            writer.writerow(["profile", p.get("platform", ""), p.get("handle", ""), p.get("profile_url", "")])
        for fi in findings:
            writer.writerow(["finding", fi.get("severity", ""), fi.get("title", ""), fi.get("description", "")])

    return str(path)
