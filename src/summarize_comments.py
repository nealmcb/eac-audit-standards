"""Summarize public comments: top themes and representative excerpts."""

from __future__ import annotations

import collections
import logging
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import pandas as pd

from utils import DATA_PROCESSED, DATA_SUMMARIES, ensure_dirs

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Common English stop words to exclude from theme analysis.
STOP_WORDS = frozenset(
    """
    a about above after again against all also am an and any are aren't as at
    be because been before being below between both but by can't cannot could
    couldn't did didn't do does doesn't doing don't down during each few for
    from further get got had hadn't has hasn't have haven't having he he'd he'll
    he's her here here's hers herself him himself his how how's i i'd i'll i'm
    i've if in into is isn't it it's its itself let's me more most mustn't my
    myself no nor not of off on once only or other ought our ours ourselves out
    over own same shan't she she'd she'll she's should shouldn't so some such
    than that that's the their theirs them themselves then there there's these
    they they'd they'll they're they've this those through to too under until up
    very was wasn't we we'd we'll we're we've were weren't what what's when
    when's where where's which while who who's whom why why's will with won't
    would wouldn't you you'd you'll you're you've your yours yourself yourselves
    also comment comments public standard standards draft election audit
    """.split()
)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z]{3,}", text.lower())


def top_words(texts: list[str], n: int = 20) -> list[tuple[str, int]]:
    counter: collections.Counter[str] = collections.Counter()
    for text in texts:
        for word in tokenize(text):
            if word not in STOP_WORDS:
                counter[word] += 1
    return counter.most_common(n)


def find_excerpt(texts: list[str], keyword: str, max_len: int = 220) -> str:
    for text in sorted(texts, key=len, reverse=True):
        if keyword.lower() in text.lower():
            idx = text.lower().index(keyword.lower())
            start = max(0, idx - 60)
            end = min(len(text), idx + max_len)
            excerpt = text[start:end].strip()
            if start > 0:
                excerpt = "..." + excerpt
            if end < len(text):
                excerpt += "..."
            return excerpt
    return ""


def build_summary(df: pd.DataFrame) -> str:
    lines = ["# Public Comments Summary", ""]
    lines.append(f"**Total comments:** {len(df)}")

    active = df[~df["withdrawn"].astype(bool)]
    lines.append(f"**Active (non-withdrawn) comments:** {len(active)}")

    with_org = active[active["organization"].fillna("").str.strip().astype(bool)]
    lines.append(f"**From organizations:** {len(with_org)}")
    lines.append(f"**From individuals:** {len(active) - len(with_org)}")
    lines.append("")

    if not with_org.empty:
        lines.append("## Top Organizations")
        top_orgs = with_org["organization"].value_counts().head(10)
        for org, cnt in top_orgs.items():
            plural = "s" if cnt > 1 else ""
            lines.append(f"- **{org}** ({cnt} comment{plural})")
        lines.append("")

    comment_texts = [t for t in active["comment_text"].dropna().tolist() if str(t).strip()]

    if comment_texts:
        lines.append("## Top Themes (word frequency, stop words removed)")
        themes = top_words(comment_texts, n=15)
        for word, count in themes:
            lines.append(f"- `{word}` — {count} occurrence{'s' if count > 1 else ''}")
        lines.append("")

        lines.append("## Representative Excerpts by Theme")
        for word, _ in themes[:5]:
            excerpt = find_excerpt(comment_texts, word)
            if excerpt:
                lines.append(f"\n### Theme: `{word}`")
                lines.append(f"> {excerpt}")
        lines.append("")

        lines.append("## Most Detailed Comments")
        detailed = (
            active.assign(text_len=active["comment_text"].str.len())
            .nlargest(3, "text_len")
        )
        for _, row in detailed.iterrows():
            first = "" if str(row.get("first_name") or "") in ("", "nan") else str(row["first_name"]).strip()
            last = "" if str(row.get("last_name") or "") in ("", "nan") else str(row["last_name"]).strip()
            name = f"{first} {last}".strip() or "Anonymous"
            org_val = "" if str(row.get("organization") or "") in ("", "nan") else str(row["organization"]).strip()
            org = f" ({org_val})" if org_val else ""
            date = str(row.get("submitted_date", "n/a"))
            lines.append(f"\n**{name}{org}** — {date}")
            body = str(row.get("comment_text") or "")
            preview = body[:400] + ("..." if len(body) > 400 else "")
            lines.append(f"> {preview}")
        lines.append("")

    else:
        lines.append("*No comment text available for theme analysis.*")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by eac-audit-standards pipeline.*")
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    csv_path = DATA_PROCESSED / "comments.csv"

    if not csv_path.exists():
        log.error(
            "Normalized comments not found: %s. Run normalize_comments.py first.", csv_path
        )
        sys.exit(1)

    df = pd.read_csv(csv_path)
    log.info("Loaded %d comments from %s", len(df), csv_path)

    summary = build_summary(df)
    out_path = DATA_SUMMARIES / "comments_summary.md"
    out_path.write_text(summary)
    log.info("Wrote comments summary to %s", out_path)


if __name__ == "__main__":
    main()
