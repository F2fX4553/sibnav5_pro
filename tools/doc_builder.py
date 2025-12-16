import os
import shutil
import re
from pathlib import Path

# Config
SRC_DIR = "docs/content"
OUT_DIR = "docs/public"
THEME_DIR = "docs/theme"
SITE_TITLE = "Sibna Protocol Docs"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {site_title}</title>
    <link rel="stylesheet" href="{css_path}"> 
</head>
<body>
    <nav class="navbar">
        <div class="brand">
            <span>⚡</span> Sibna Protocol
        </div>
    </nav>
    <div class="main-container">
        <aside class="sidebar">
            {sidebar}
        </aside>
        <main class="content">
            {content}
        </main>
        <aside class="toc">
            <strong>On this page</strong>
            {toc}
        </aside>
    </div>
</body>
</html>
"""

def generate_sidebar(file_tree, current_file):
    # Hardcoded structure for specific order
    structure = {
        "Introduction": ["index.md", "introduction/philosophy.md", "introduction/architecture.md"],
        "Protocol Core": ["protocol/specs.md", "protocol/security.md"],
        "SDKs": ["sdk/python.md", "sdk/javascript.md", "sdk/flutter.md"],
        "Deployment": ["deployment.md"]
    }
    
    html = ""
    for section, files in structure.items():
        html += f'<div class="nav-group"><div class="nav-header">{section}</div>'
        for f in files:
            # Check if file exists to fetch title
            path = os.path.join(SRC_DIR, f)
            if not os.path.exists(path): continue
            
            title = f.replace(".md", "").replace("/", " ").title()
            if f == "index.md": title = "Home"
            if "introduction/philosophy.md" in f: title = "Philosophy & Manifesto"
            
            # Try getting first h1 if possible
            try:
                with open(path, 'r', encoding='utf-8') as handle:
                    first_line = handle.readline().strip()
                    if first_line.startswith("# "):
                        title = first_line[2:]
            except: pass
            
            # Link resolution
            link = f.replace(".md", ".html")
            active = 'active' if f == current_file else ''
            
            # Fix relative links
            current_depth = len(current_file.split("/")) - 1
            prefix = "../" * current_depth
            final_link = prefix + link
            
            html += f'<a href="{final_link}" class="nav-item {active}">{title}</a>'
        html += '</div>'
    return html

def parse_markdown(md_text):
    lines = md_text.split('\n')
    html = ""
    in_code = False
    
    for line in lines:
        line = line.strip()
        if line.startswith("```"):
            in_code = not in_code
            html += "<pre><code>" if in_code else "</code></pre>"
            continue
        
        if in_code:
            html += f"{line}\n"
            continue
            
        if line.startswith("# "):
            html += f"<h1>{line[2:]}</h1>"
        elif line.startswith("## "):
            html += f"<h2>{line[3:]}</h2>"
        elif line.startswith("### "):
            html += f"<h3>{line[4:]}</h3>"
        elif line.startswith("- "):
            html += f"<li>{line[2:]}</li>"
        elif line.startswith("> "):
             html += f"<blockquote>{line[2:]}</blockquote>"
        elif line == "":
            html += "<br>"
        else:
            html += f"<p>{line}</p>"
    return html

def main():
    # Clean Output
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)
    
    # Copy Assets
    shutil.copy(f"{THEME_DIR}/style.css", f"{OUT_DIR}/style.css")
    
    # 1. Collect all pages for Next/Prev logic
    pages = []
    # Explicit order based on structure + others found
    # For now, just recursive walk to capture everything
    for root, dirs, files in os.walk(SRC_DIR):
        for file in files:
            if not file.endswith(".md"): continue
            rel_path = os.path.relpath(os.path.join(root, file), SRC_DIR).replace("\\", "/")
            pages.append(rel_path)
    pages.sort()

    # 2. Build
    for i, rel_path in enumerate(pages):
        full_path = os.path.join(SRC_DIR, rel_path)
            
        with open(full_path, "r", encoding='utf-8') as f:
            content_md = f.read()
        
        # Parse Content
        title = "Doc"
        if content_md.startswith("# "):
            title = content_md.split("\n")[0][2:]
            
        content_html = parse_markdown(content_md)
        sidebar_html = generate_sidebar(None, rel_path)
        
        # Footer Nav
        nav_footer = '<div class="docs-footer">'
        
        # Previous
        if i > 0:
            prev_rel = pages[i-1]
            current_depth = len(rel_path.split("/")) - 1
            # link calculation:
            target_link = ("../" * current_depth) + prev_rel.replace(".md", ".html")
            nav_footer += f'<a href="{target_link}" class="nav-prev">← Previous</a>'
            
        # Next
        if i < len(pages) - 1:
            next_rel = pages[i+1]
            current_depth = len(rel_path.split("/")) - 1
            target_link = ("../" * current_depth) + next_rel.replace(".md", ".html")
            nav_footer += f'<a href="{target_link}" class="nav-next">Next →</a>'
            
        nav_footer += '</div>'
        content_html += nav_footer
        
        # CSS Path
        depth = len(rel_path.split("/")) - 1
        css_path = ("../" * depth) + "style.css"
        
        # Render
        final_html = HTML_TEMPLATE.format(
            title=title,
            site_title=SITE_TITLE,
            content=content_html,
            sidebar=sidebar_html,
            toc="<ul><li><a href='#'>Top</a></li></ul>",
            css_path=css_path
        )
        
        # Write
        out_file_path = os.path.join(OUT_DIR, rel_path.replace(".md", ".html"))
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
        with open(out_file_path, "w", encoding='utf-8') as f:
            f.write(final_html)
                
    print(f"Build Complete. Open {os.path.abspath(OUT_DIR)}/index.html")

if __name__ == "__main__":
    main()
