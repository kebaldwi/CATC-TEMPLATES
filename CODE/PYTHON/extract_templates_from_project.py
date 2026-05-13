#!/usr/bin/env python3
"""Extract individual template files from a DNAC/Catalyst Center project JSON export.

Usage:
    python extract_templates_from_project.py <project.json> [<output_dir>]

The input JSON is expected to be a list of project objects, each with a
`templates` array. Each template has a `name` and `templateContent` field, and
may optionally carry a non-empty `containingTemplates` array describing the
children of a composite template. For composites, only the children are
emitted (the parent has no real content of its own).

Each extracted template is written as `<sanitized name>.j2` to the output
directory. Existing files with the same name are overwritten (a warning is
printed). If two templates in the same run resolve to the same output name,
the first one wins and subsequent occurrences are skipped with a warning.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("CODE/TEMPLATES/JINJA2/DAYN/J2")
INVALID_CHARS = '/\\:*?"<>|'


def sanitize(name: str) -> str:
    cleaned = (name or "").strip()
    for ch in INVALID_CHARS:
        cleaned = cleaned.replace(ch, "_")
    return cleaned


def iter_templates(projects):
    """Yield (template_name, template_content, template_params) tuples.

    For composite templates (non-empty `containingTemplates`), yield each
    child instead of the parent.
    """
    for project in projects:
        for tmpl in project.get("templates", []) or []:
            children = tmpl.get("containingTemplates") or []
            if children:
                for child in children:
                    yield (
                        child.get("name", ""),
                        child.get("templateContent", ""),
                        child.get("templateParams") or [],
                    )
            else:
                yield (
                    tmpl.get("name", ""),
                    tmpl.get("templateContent", ""),
                    tmpl.get("templateParams") or [],
                )


def build_params_comment(params):
    """Return a Jinja2 {# ... #} comment block describing bind variables.

    Returns an empty string when there are no parameters.
    """
    if not params:
        return ""

    lines = ["{#", "  Template Parameters (bind variables):"]
    for p in params:
        name = p.get("parameterName") or "(unnamed)"
        attrs = []
        dtype = p.get("dataType")
        if dtype:
            attrs.append(str(dtype))
        if p.get("required"):
            attrs.append("required")
        if p.get("sensitiveField"):
            attrs.append("sensitive")
        if p.get("paramArray"):
            attrs.append("array")
        default = p.get("defaultValue")
        if default not in (None, ""):
            attrs.append(f"default={default!r}")
        binding = p.get("binding")
        if binding:
            attrs.append(f"binding={binding!r}")
        attr_str = f" ({', '.join(attrs)})" if attrs else ""
        line = f"    - {name}{attr_str}"
        desc = p.get("description")
        if desc:
            line += f" - {desc}"
        lines.append(line)
    lines.append("#}")
    return "\n".join(lines) + "\n"


def iter_composites(projects):
    """Yield composite template dicts (those with a non-empty `containingTemplates`)."""
    for project in projects:
        project_name = project.get("name", "")
        for tmpl in project.get("templates", []) or []:
            children = tmpl.get("containingTemplates") or []
            if children:
                yield project_name, tmpl, children


def _yaml_escape(value):
    """Return a YAML-safe scalar representation of `value` (string/bool/None)."""
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    s = str(value)
    if s == "":
        return '""'
    # Quote if it contains characters that could confuse a YAML parser.
    needs_quote = any(c in s for c in ":#\n\"'&*!|>%@`,[]{}") or s.strip() != s
    if needs_quote:
        escaped = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return s


def build_composite_yaml(project_name, composite, children):
    """Return YAML text describing the composite template and its ordered children."""
    name = composite.get("name", "")
    description = composite.get("description", "") or ""
    language = composite.get("language", "") or ""
    failure_policy = composite.get("failurePolicy", "") or ""

    lines = [
        "# ---------------------------------------------------------------------------",
        f"# Composite template manifest: {name}",
        "#",
        "# This file lists the child templates that make up the composite template",
        f"# '{name}' as exported from the DNAC/Catalyst Center project",
        f"# '{project_name}'. The `templates` list below preserves the execution",
        "# order recorded in the composite. Each entry corresponds to an individual",
        "# .j2 file in this same folder (matched by `name`).",
        "# ---------------------------------------------------------------------------",
        f"composite: {_yaml_escape(name)}",
        f"project: {_yaml_escape(project_name)}",
        f"language: {_yaml_escape(language)}",
        f"failurePolicy: {_yaml_escape(failure_policy)}",
        f"description: {_yaml_escape(description)}",
        "templates:",
    ]
    for idx, child in enumerate(children, start=1):
        child_name = child.get("name", "")
        child_lang = child.get("language", "") or ""
        child_desc = child.get("description", "") or ""
        lines.append(f"  - order: {idx}")
        lines.append(f"    name: {_yaml_escape(child_name)}")
        lines.append(f"    file: {_yaml_escape(sanitize(child_name) + '.j2')}")
        lines.append(f"    language: {_yaml_escape(child_lang)}")
        lines.append(f"    description: {_yaml_escape(child_desc)}")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) < 2 or len(argv) > 3:
        print(__doc__, file=sys.stderr)
        return 2

    input_path = Path(argv[1])
    output_dir = Path(argv[2]) if len(argv) == 3 else DEFAULT_OUTPUT_DIR

    if not input_path.is_file():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("ERROR: expected top-level JSON array of project objects", file=sys.stderr)
        return 1

    discovered = 0
    written = 0
    overwrites = 0
    duplicates_skipped = 0
    written_names: set[str] = set()

    empty_skipped = 0
    for name, content, params in iter_templates(data):
        discovered += 1
        if not name:
            print("WARN: template with empty name encountered, skipping", file=sys.stderr)
            continue
        if not (content or "").strip():
            # Composite children often appear as empty references to a
            # standalone top-level template; skip so the real content wins.
            print(f"INFO: empty content for '{name}', skipping", file=sys.stderr)
            empty_skipped += 1
            continue

        filename = f"{sanitize(name)}.j2"
        if filename in written_names:
            print(
                f"WARN: duplicate name '{filename}' within run, skipping subsequent occurrence",
                file=sys.stderr,
            )
            duplicates_skipped += 1
            continue

        target = output_dir / filename
        if target.exists():
            print(f"WARN: overwriting {target}", file=sys.stderr)
            overwrites += 1

        header = build_params_comment(params)
        target.write_text(header + (content or ""), encoding="utf-8")
        written_names.add(filename)
        written += 1

    # Emit a YAML manifest for each composite template describing the ordered
    # child templates that make it up.
    composites_written = 0
    for project_name, composite, children in iter_composites(data):
        comp_name = composite.get("name", "")
        if not comp_name:
            print("WARN: composite with empty name encountered, skipping yaml", file=sys.stderr)
            continue
        yaml_filename = f"{sanitize(comp_name)}.yml"
        yaml_target = output_dir / yaml_filename
        if yaml_target.exists():
            print(f"WARN: overwriting {yaml_target}", file=sys.stderr)
        yaml_target.write_text(
            build_composite_yaml(project_name, composite, children),
            encoding="utf-8",
        )
        composites_written += 1

    print(
        f"Done. discovered={discovered} written={written} "
        f"overwrites={overwrites} duplicates_skipped={duplicates_skipped} "
        f"empty_skipped={empty_skipped} composites_written={composites_written}"
    )
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
