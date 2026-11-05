"""Regenerates the shared outputs from the prompt files.

    python3 build.py

- design-partner-all-in-one.md: designer.md plus agents/*.md as Appendices A–C, for tools that
  can't read separate files.
- index.html: the GitHub Pages site (site/template.html with every prompt embedded, with copy buttons).

Edit designer.md, agents/*.md or site/template.html, then run this.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
AGENTS = [
    ("A", "agents/user-research.md", "User research agent"),
    ("B", "agents/requirements.md", "Requirements agent"),
    ("C", "agents/builder.md", "Builder agent"),
]


def all_in_one() -> str:
    d = (HERE / "designer.md").read_text()
    d = d.replace(
        "the `agents/` folder next to this file (for example `design-partner/agents/builder.md`). "
        "Give a subagent the path to its prompt, or paste the prompt in.",
        "Appendices A, B and C below. Give each subagent its appendix as its instructions.",
    )
    for letter, path, _ in AGENTS:
        d = d.replace(f"(`{path}`)", f"(Appendix {letter})")
    leftover = [line for line in d.splitlines() if "agents/" in line]
    assert not leftover, f"designer.md still points at agents/: {leftover}"

    def demote(text: str) -> str:
        """Shift headings down one level so each appendix nests under the main prompt."""
        return re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", text, flags=re.M)

    out = [d.rstrip(), ""]
    for letter, path, title in AGENTS:
        body = re.sub(r"^# .*\n", "", (HERE / path).read_text(), count=1)
        out += ["---", "", f"## Appendix {letter}: {title}", "", demote(body).strip(), ""]
    return "\n".join(out) + "\n"


SITE_TABS = [
    ("all", "All-in-one", "design-partner-all-in-one.md", "Everything in one file. Paste it into a chat assistant, or save it next to your project."),
    ("designer", "Designer", "designer.md", "The main prompt. Your agent follows this one and runs the whole process."),
    ("research", "User research", "agents/user-research.md", "Subagent: turns the interview and shared images into a short research report."),
    ("requirements", "Requirements", "agents/requirements.md", "Subagent: turns the research into numbered requirements and a build plan (PRD)."),
    ("builder", "Builder", "agents/builder.md", "Subagent: builds one milestone at a time on Next.js, shadcn/ui and the AI SDK."),
]


def site() -> str:
    data = {k: (HERE / f).read_text() for k, _, f, _ in SITE_TABS}
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{k}" aria-controls="panel" aria-selected="{"true" if i == 0 else "false"}" '
        f'data-k="{k}" tabindex="{0 if i == 0 else -1}"><span class="tname">{html.escape(n)}</span>'
        f'<span class="tfile">{html.escape(f)}</span></button>'
        for i, (k, n, f, _) in enumerate(SITE_TABS)
    )
    meta = {k: {"file": f, "about": a, "words": len(data[k].split())} for k, _, f, a in SITE_TABS}
    as_js = lambda v: json.dumps(v).replace("</", "<\\/")  # noqa: E731 - keep "</script>" out of the inline script
    return (
        (HERE / "site/template.html").read_text()
        .replace("%%TABS%%", tabs)
        .replace("%%DATA%%", as_js(data))
        .replace("%%META%%", as_js(meta))
        .replace("%%FIRST%%", html.escape(data["all"]))
    )


if __name__ == "__main__":
    (HERE / "design-partner-all-in-one.md").write_text(all_in_one())
    (HERE / "index.html").write_text(site())
    print("wrote design-partner-all-in-one.md and index.html")
