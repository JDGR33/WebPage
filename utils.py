import argparse
import html
import os
import re
from pathlib import Path

import markdown

PLACEHOLDER = "<!--ADD -->"
TEMPLATE_PLACEHOLDER = "{ post_content }"
POST_TITLE_PLACEHOLDER = "{ post_title }"
META_DESCRIPTION_PLACEHOLDER = "{ meta_description }"


def parse_front_matter(source_text: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    if not source_text.startswith("---\n"):
        return metadata, source_text

    front_matter_end = source_text.find("\n---\n", 4)
    if front_matter_end == -1:
        return metadata, source_text

    front_matter = source_text[4:front_matter_end]
    body = source_text[front_matter_end + 5 :]

    for line in front_matter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip().lower()] = value.strip()

    return metadata, body


def extract_first_heading(markdown_text: str) -> str | None:
    for line in markdown_text.splitlines():
        heading_match = re.match(r"^\s*#{1,6}\s+(.+?)\s*$", line)
        if heading_match:
            return heading_match.group(1).strip()
    return None


def extract_description(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return stripped
    return ""


def normalize_meta_description(text: str, max_length: int = 160) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= max_length:
        return cleaned

    cutoff = cleaned[: max_length - 1].rstrip()
    if " " in cutoff:
        cutoff = cutoff.rsplit(" ", 1)[0]
    return f"{cutoff}…"


def build_article_entry(
    post_href: str,
    post_title: str,
    description: str,
    date: str,
    tags: str,
) -> str:
    safe_title = html.escape(post_title)
    safe_description = html.escape(description)
    safe_date = html.escape(date)
    safe_tags = html.escape(tags)

    meta_parts = [part for part in (safe_date, safe_tags) if part]
    meta_line = ""
    if meta_parts:
        meta_line = f"\n                <p>{' | '.join(meta_parts)}</p>"

    return (
        "\n            <article>\n"
        f'                <h3><a href="{post_href}">{safe_title}</a></h3>\n'
        f"                <p>{safe_description}</p>{meta_line}\n"
        "            </article>\n"
        f"            {PLACEHOLDER}\n"
    )


def add_post_to_index(
    blog_main_path: Path,
    post_href: str,
    post_title: str,
    description: str = "",
    date: str = "",
    tags: str = "",
) -> bool:
    text = blog_main_path.read_text(encoding="utf-8")

    if f'href="{post_href}"' in text:
        return False

    if PLACEHOLDER not in text:
        raise ValueError(
            f"Could not find placeholder '{PLACEHOLDER}' in {blog_main_path}"
        )

    text_to_add = build_article_entry(post_href, post_title, description, date, tags)
    updated_text = text.replace(PLACEHOLDER, text_to_add, 1)
    blog_main_path.write_text(updated_text, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown posts into HTML and optionally add them to blogMain.html"
    )
    parser.add_argument("input_path", help="Path to the source markdown file")
    parser.add_argument(
        "--template",
        default="BlogPosts/postTemplate.html",
        help="Path to the HTML post template",
    )
    parser.add_argument(
        "--blog-index",
        default="BlogPosts/blogMain.html",
        help="Path to the blog index file that contains the placeholder",
    )
    parser.add_argument("--title", default="", help="Override post title")
    parser.add_argument(
        "--description", default="", help="Override short post description"
    )
    parser.add_argument("--date", default="", help="Optional date shown on blog index")
    parser.add_argument("--tags", default="", help="Optional tags shown on blog index")
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Generate HTML only and skip blog index update",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input_path)
    template_path = Path(args.template)
    blog_main_path = Path(args.blog_index)

    if not input_path.exists():
        raise FileNotFoundError(f"Input markdown file does not exist: {input_path}")
    if input_path.suffix.lower() != ".md":
        raise ValueError(f"Input file must use .md extension: {input_path}")
    if not template_path.exists():
        raise FileNotFoundError(f"Template file does not exist: {template_path}")

    source_text = input_path.read_text(encoding="utf-8")
    metadata, markdown_body = parse_front_matter(source_text)

    title = (
        args.title.strip()
        or metadata.get("title", "").strip()
        or extract_first_heading(markdown_body)
        or input_path.stem.replace("_", " ").replace("-", " ").title()
    )
    description = (
        args.description.strip()
        or metadata.get("description", "").strip()
        or extract_description(markdown_body)
    )
    date = args.date.strip() or metadata.get("date", "").strip()
    tags = args.tags.strip() or metadata.get("tags", "").strip()

    post_html = markdown.markdown(
        markdown_body, extensions=["extra", "fenced_code", "tables"]
    )
    template_text = template_path.read_text(encoding="utf-8")

    if TEMPLATE_PLACEHOLDER not in template_text:
        raise ValueError(
            f"Template placeholder '{TEMPLATE_PLACEHOLDER}' not found in {template_path}"
        )

    if POST_TITLE_PLACEHOLDER not in template_text:
        raise ValueError(
            f"Template placeholder '{POST_TITLE_PLACEHOLDER}' not found in {template_path}"
        )

    if META_DESCRIPTION_PLACEHOLDER not in template_text:
        raise ValueError(
            f"Template placeholder '{META_DESCRIPTION_PLACEHOLDER}' not found in {template_path}"
        )

    raw_meta_description = description or (
        "Article by Julio Guerrero about AI, data, software, and practical engineering workflows."
    )
    meta_description = normalize_meta_description(raw_meta_description)

    output_text = template_text.replace(TEMPLATE_PLACEHOLDER, post_html)
    output_text = output_text.replace(POST_TITLE_PLACEHOLDER, html.escape(title))
    output_text = output_text.replace(
        META_DESCRIPTION_PLACEHOLDER,
        html.escape(meta_description),
    )
    output_path = input_path.with_suffix(".html")
    output_path.write_text(output_text, encoding="utf-8", errors="xmlcharrefreplace")

    print(f"Generated HTML: {output_path}")

    if args.no_index:
        print("Skipped blog index update (--no-index).")
        return

    if not blog_main_path.exists():
        raise FileNotFoundError(f"Blog index file does not exist: {blog_main_path}")

    post_href = output_path.name
    if output_path.parent.resolve() != blog_main_path.parent.resolve():
        post_href = os.path.relpath(
            output_path.resolve(),
            start=blog_main_path.parent.resolve(),
        ).replace("\\", "/")

    inserted = add_post_to_index(
        blog_main_path=blog_main_path,
        post_href=post_href,
        post_title=title,
        description=description,
        date=date,
        tags=tags,
    )

    if inserted:
        print(f"Added '{title}' to {blog_main_path}")
    else:
        print(f"Skipped index update: '{post_href}' already exists in {blog_main_path}")


if __name__ == "__main__":
    main()
