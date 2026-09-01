"""Check project documentation and method records using Python 3.10+.
No network, datasets, model execution or third-party dependencies.
Does not validate research claims, external URLs, licenses or permissions.
"""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "upstream", "node_modules", "__pycache__"}
REQUIRED = [
    "README.md", "CONTRIBUTING.md", ".gitignore",
    "docs/project_overview.md", "docs/research_map.md", "docs/roadmap.md",
    "docs/status.md", "docs/source_audit.md", "docs/source_manifest.json",
    "literature/search_protocol.md", "data/schema.md", "data/annotation.md",
    "methods/catalog.json", "benchmarks/README.md",
    "governance/README.md", "templates/README.md",
    ".github/PULL_REQUEST_TEMPLATE.md", ".github/workflows/check.yml",
]
errors = []
def check_file(target, origin):
    path = (ROOT / target).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        errors.append(f"{origin}: invalid or missing local file: {target}")

for name in REQUIRED:
    check_file(name, "required")
documents = sorted(
    p for p in ROOT.rglob("*.md")
    if not SKIP.intersection(p.relative_to(ROOT).parts)
)
link_count = 0
for document in documents:
    content = document.read_text(encoding="utf-8")
    if "\ufffd" in content:
        errors.append(f"{document.relative_to(ROOT)}: encoding replacement character")
    content = re.sub(r"(?ms)^[ \t]*```.*?^[ \t]*```[^\n]*", "", content)
    for match in re.finditer(r"\[[^\]\n]*\]\(([^\n]*?)\)", content):
        target = match.group(1).strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        link_count += 1
        path = (document.parent / unquote(parts.path)).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            errors.append(f"{document.relative_to(ROOT)}: missing or invalid link: {target}")

try:
    catalog = json.loads((ROOT / "methods/catalog.json").read_text(encoding="utf-8"))
    statuses = set(catalog["status_definitions"])
    ids = set()
    for method in catalog["methods"]:
        name = method["id"]
        if name in ids:
            errors.append("Duplicate method id: " + name)
        ids.add(name)
        check_file(method["readme"], name)
        if method["status"] not in statuses:
            errors.append("Unknown status: " + name)
        if method["status"] == "source_pinned":
            upstream = method["upstream"]
            if not re.fullmatch(r"[a-f0-9]{40}", upstream["commit"]):
                errors.append("Invalid upstream commit: " + name)
            for field in ("repository", "code_license", "license_url", "checked_at"):
                if not upstream.get(field):
                    errors.append(f"{name}: missing upstream {field}")
        records = method["run_records"]
        if method["status"] in {"example_runs", "evaluated", "independently_verified"} and not records:
            errors.append("Run status requires a record: " + name)
        for record in records:
            check_file(record, name)
    manifest = json.loads((ROOT / "docs/source_manifest.json").read_text(encoding="utf-8"))
    for source in manifest["attachments"]:
        if not re.fullmatch(r"[a-f0-9]{64}", source["sha256"]):
            errors.append("Invalid attachment hash: " + source["filename"])
except (OSError, ValueError, KeyError, TypeError) as exc:
    errors.append("Invalid registry: " + str(exc))

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(documents)} Markdown files; {link_count} local links; {len(ids)} method records.")
print("Research execution, factual claims and remote access settings are outside this check.")
