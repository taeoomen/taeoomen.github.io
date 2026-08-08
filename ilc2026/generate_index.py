#!/usr/bin/env python3
"""
Generates an index.html directory listing for a folder.

Usage:
    python3 generate_index.py /path/to/your/folder

Rerun it any time the folder's contents change.
"""

import os
import sys
import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, nofollow">
<title>Index of {folder_name}</title>
<style>
  :root {{
    --bg: #0f1115;
    --panel: #171a21;
    --border: #2a2e37;
    --text: #e6e8eb;
    --muted: #8b909c;
    --accent: #5b9dff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 3rem 1.5rem;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    display: flex;
    justify-content: center;
  }}
  main {{
    width: 100%;
    max-width: 780px;
  }}
  h1 {{
    font-size: 1.4rem;
    font-weight: 600;
    margin: 0 0 0.25rem;
  }}
  .path {{
    color: var(--muted);
    font-family: "SFMono-Regular", Consolas, Menlo, monospace;
    font-size: 0.85rem;
    margin: 0 0 1.75rem;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }}
  th {{
    text-align: left;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--muted);
    font-weight: 500;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
  }}
  td {{
    padding: 0.65rem 1rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
    vertical-align: middle;
  }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(91, 157, 255, 0.06); }}
  a {{
    color: var(--text);
    text-decoration: none;
  }}
  a:hover {{ color: var(--accent); }}
  .icon {{ opacity: 0.6; margin-right: 0.5rem; }}
  .size, .date {{ color: var(--muted); white-space: nowrap; }}
  footer {{
    margin-top: 1.5rem;
    color: var(--muted);
    font-size: 0.75rem;
    text-align: center;
  }}
</style>
</head>
<body>
<main>
  <h1>Index of {folder_name}</h1>
  <p class="path">{full_path}</p>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th class="size">Size</th>
        <th class="date">Modified</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
  <footer>Generated {generated_at}</footer>
</main>
</body>
</html>
"""

ROW_TEMPLATE = """      <tr>
        <td><a href="{href}"><span class="icon">{icon}</span>{name}</a></td>
        <td class="size">{size}</td>
        <td class="date">{date}</td>
      </tr>"""


def human_size(num_bytes):
    if num_bytes is None:
        return "—"
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}" if unit == "B" else f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def build_rows(folder):
    entries = sorted(os.scandir(folder), key=lambda e: (e.is_file(), e.name.lower()))
    rows = []

    # Parent link, unless we're already at the top
    rows.append(ROW_TEMPLATE.format(href="../", icon="↩", name="../", size="", date=""))

    for entry in entries:
        if entry.name == "index.html":
            continue  # don't list itself
        stat = entry.stat()
        modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        if entry.is_dir():
            rows.append(ROW_TEMPLATE.format(
                href=f"{entry.name}/", icon="📁", name=f"{entry.name}/",
                size="—", date=modified
            ))
        else:
            rows.append(ROW_TEMPLATE.format(
                href=entry.name, icon="📄", name=entry.name,
                size=human_size(stat.st_size), date=modified
            ))
    return "\n".join(rows)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_index.py /path/to/folder")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"Not a directory: {folder}")
        sys.exit(1)

    rows = build_rows(folder)
    html = HTML_TEMPLATE.format(
        folder_name=os.path.basename(os.path.abspath(folder)) or "/",
        full_path=os.path.abspath(folder),
        rows=rows,
        generated_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    out_path = os.path.join(folder, "index.html")
    with open(out_path, "w") as f:
        f.write(html)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()