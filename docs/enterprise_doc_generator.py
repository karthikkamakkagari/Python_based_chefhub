import os
import ast
import json
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from docx import Document
from graphviz import Digraph
from tabulate import tabulate
from jinja2 import Template


# ==============================
# CONFIGURATION
# ==============================

PROJECT_PATH = "."
DOCS_DIR = "docs"

MD_FILE = os.path.join(DOCS_DIR, "Enterprise_Django_Documentation.md")
PDF_FILE = os.path.join(DOCS_DIR, "Enterprise_Django_Documentation.pdf")
DOCX_FILE = os.path.join(DOCS_DIR, "Enterprise_Django_Documentation.docx")
HTML_FILE = os.path.join(DOCS_DIR, "Enterprise_Django_Documentation.html")
SWAGGER_FILE = os.path.join(DOCS_DIR, "swagger_spec.json")
ARCH_FILE = os.path.join(DOCS_DIR, "architecture")

fr_counter = 1


# ==============================
# UTIL
# ==============================

def next_fr():
    global fr_counter
    fr_id = f"FR-{fr_counter:03}"
    fr_counter += 1
    return fr_id


# ==============================
# AST PARSERS
# ==============================

def extract_views(file_path):
    views = []
    try:
        tree = ast.parse(open(file_path, "r", encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                views.append(node.name)
            elif isinstance(node, ast.ClassDef):
                views.append(node.name)
    except:
        pass
    return views


def extract_models(file_path):
    models = {}
    try:
        tree = ast.parse(open(file_path, "r", encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                fields = []
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if hasattr(target, "id"):
                                fields.append(target.id)
                models[node.name] = fields
    except:
        pass
    return models


def extract_forms(file_path):
    forms = {}
    try:
        tree = ast.parse(open(file_path, "r", encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                fields = []
                validations = []
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if hasattr(target, "id"):
                                fields.append(target.id)
                    if isinstance(item, ast.FunctionDef):
                        if item.name.startswith("clean"):
                            validations.append(item.name)
                if fields:
                    forms[node.name] = {
                        "fields": fields,
                        "validations": validations
                    }
    except:
        pass
    return forms


def extract_permissions(file_path):
    permissions = {}
    try:
        tree = ast.parse(open(file_path, "r", encoding="utf-8").read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                decorators = []
                for d in node.decorator_list:
                    if isinstance(d, ast.Name):
                        decorators.append(d.id)
                if decorators:
                    permissions[node.name] = decorators
    except:
        pass
    return permissions


def extract_urls(file_path):
    urls = []
    try:
        content = open(file_path, "r", encoding="utf-8").read()
        for line in content.split("\n"):
            if "path(" in line:
                urls.append(line.strip())
    except:
        pass
    return urls


# ==============================
# COLLECT PROJECT DATA
# ==============================

def collect_project_data():
    views, models, forms, permissions, urls = [], {}, {}, {}, []

    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            full_path = os.path.join(root, file)

            if file == "views.py":
                views.extend(extract_views(full_path))
                permissions.update(extract_permissions(full_path))

            if file == "models.py":
                models.update(extract_models(full_path))

            if file == "forms.py":
                forms.update(extract_forms(full_path))

            if file == "urls.py":
                urls.extend(extract_urls(full_path))

    return views, models, forms, permissions, urls


# ==============================
# GENERATORS
# ==============================

def generate_markdown(views, models, forms, permissions, urls):
    with open(MD_FILE, "w", encoding="utf-8") as md:
        md.write("# Enterprise Django Documentation\n\n")
        md.write(f"Generated on: {datetime.now()}\n\n")

        # Folder Structure
        md.write("## 1. Folder Structure\n\n")
        for root, dirs, files in os.walk(PROJECT_PATH):
            level = root.replace(PROJECT_PATH, "").count(os.sep)
            indent = "  " * level
            md.write(f"{indent}- {os.path.basename(root)}/\n")
            for file in files:
                md.write(f"{indent}  - {file}\n")

        # Functional Requirements
        md.write("\n## 2. Functional Requirements\n\n")
        for view in views:
            md.write(f"### {next_fr()}\n")
            md.write(f"- The system shall execute `{view}` functionality.\n\n")

        # Models
        md.write("## 3. Database Models\n\n")
        for model, fields in models.items():
            md.write(f"### {model}\n")
            for f in fields:
                md.write(f"- Field: `{f}`\n")
            md.write("\n")

        # Forms
        md.write("## 4. Forms & Validation\n\n")
        for form, data in forms.items():
            md.write(f"### {form}\n")
            md.write("Fields:\n")
            for f in data["fields"]:
                md.write(f"- `{f}`\n")
            md.write("Validation Methods:\n")
            for v in data["validations"]:
                md.write(f"- `{v}`\n")
            md.write("\n")

        # Permissions
        md.write("## 5. Permissions & Decorators\n\n")
        for func, decs in permissions.items():
            md.write(f"- `{func}` → {', '.join(decs)}\n")

        # URLs
        md.write("\n## 6. URL Endpoints\n\n")
        for u in urls:
            md.write(f"- `{u}`\n")

        # Hosting Table
        md.write("\n## 7. Hosting Comparison\n\n")
        hosting_table = tabulate(
            [
                ["DigitalOcean", "VPS", "High", "₹500+"],
                ["AWS", "Cloud", "Very High", "Usage Based"],
                ["Hostinger", "VPS", "Medium", "₹400+"],
                ["Shared Hosting", "Shared", "Low", "₹200+"],
            ],
            headers=["Provider", "Type", "Scalability", "Cost"],
            tablefmt="grid",
        )
        md.write(hosting_table + "\n\n")

        # ISO Mode
        md.write("## 8. ISO 26262 Formal Statements\n\n")
        for view in views:
            md.write(f"- The system shall ensure `{view}` operates in a fail-safe manner.\n")

        # Risk Section
        md.write("\n## 9. Risk Assessment\n")
        md.write("R1: Database Failure → Mitigation: Daily backup\n")
        md.write("R2: Unauthorized Access → Mitigation: RBAC\n")
        md.write("R3: Server Crash → Mitigation: VPS Monitoring\n")

        # Test Cases
        md.write("\n## 10. Test Cases\n")
        for view in views:
            md.write(f"- TC-{view}: Verify `{view}` executes successfully.\n")


def generate_swagger(urls):
    swagger = {
        "openapi": "3.0.0",
        "info": {"title": "Django API", "version": "1.0.0"},
        "paths": {},
    }

    for u in urls:
        swagger["paths"][u] = {
            "get": {
                "summary": u,
                "responses": {"200": {"description": "Success"}},
            }
        }

    with open(SWAGGER_FILE, "w") as f:
        json.dump(swagger, f, indent=4)


def generate_architecture(output_path="docs/architecture"):
    dot = Digraph(comment="System Architecture", format="png")
    dot.attr(rankdir="LR")

    dot.node("User", shape="oval")
    dot.node("Nginx", shape="box")
    dot.node("Gunicorn", shape="box")
    dot.node("Django", shape="box")
    dot.node("PostgreSQL", shape="cylinder")

    dot.edges([
        ("User", "Nginx"),
        ("Nginx", "Gunicorn"),
        ("Gunicorn", "Django"),
        ("Django", "PostgreSQL"),
    ])

    dot.render(output_path, cleanup=True)

def generate_er_diagram(output_path="docs/database_er"):
    dot = Digraph(comment="Database ER Diagram", format="png")
    dot.attr(rankdir="LR")

    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            if file == "models.py":
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        model_name = node.name
                        dot.node(model_name, model_name, shape="box")

                        for body_item in node.body:
                            if isinstance(body_item, ast.Assign):
                                value = body_item.value
                                if hasattr(value, "func"):
                                    if hasattr(value.func, "attr"):
                                        field_type = value.func.attr
                                        if field_type == "ForeignKey":
                                            if hasattr(value.args[0], "id"):
                                                related_model = value.args[0].id
                                                dot.edge(model_name, related_model)

    dot.render(output_path, cleanup=True)


def generate_pdf():
    doc = SimpleDocTemplate(PDF_FILE)
    styles = getSampleStyleSheet()
    story = []

    for line in open(MD_FILE, "r", encoding="utf-8"):
        story.append(Paragraph(line.strip(), styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)


def generate_docx():
    document = Document()
    for line in open(MD_FILE, "r", encoding="utf-8"):
        document.add_paragraph(line.strip())
    document.save(DOCX_FILE)


def generate_html(content, output_file):
    template = Template("""
    <html>
    <head>
        <title>Enterprise Django Documentation</title>
        <style>
            body { font-family: Arial; padding: 40px; }
            summary { font-weight: bold; cursor: pointer; }
            details { margin-left: 20px; }
            pre { background: #f4f4f4; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>Enterprise Django Documentation</h1>
        {{ content | safe }}
    </body>
    </html>
    """)

    html_content = template.render(content=content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_folder_tree_html():
    html = "<ul>"

    for root, dirs, files in os.walk(PROJECT_PATH):
        level = root.replace(PROJECT_PATH, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root)

        html += f"""
        <li>
            <details>
                <summary>{folder_name}/</summary>
                <ul>
        """

        for file in files:
            html += f"<li>{file}</li>"

        html += "</ul></details></li>"

    html += "</ul>"
    return html

def generate_static_explorer(project_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), output_html="docs/static_explorer.html"):
    import os
    import json
    import base64
    from jinja2 import Template

    os.makedirs("docs", exist_ok=True)

    IGNORE_FOLDERS = {
        "__pycache__", ".git", ".idea", ".vscode",
        "venv", "env", "node_modules", "docs"
    }

    IGNORE_FILES = {".DS_Store"}
    SHOW_HIDDEN = False

    def is_visible(name):
        if not SHOW_HIDDEN and name.startswith("."):
            return False
        if name in IGNORE_FOLDERS or name in IGNORE_FILES:
            return False
        return True

    def build_tree(path):
        name = os.path.basename(path)

        if not is_visible(name):
            return None

        node = {"name": name}

        if os.path.isdir(path):
            node["type"] = "folder"
            children = []

            for child in sorted(os.listdir(path)):
                child_path = os.path.join(path, child)
                child_node = build_tree(child_path)
                if child_node:
                    children.append(child_node)

            node["children"] = children

        else:
            node["type"] = "file"
            ext = os.path.splitext(path)[1].lower()
            node["extension"] = ext

            try:
                if ext in [".png", ".jpg", ".jpeg", ".gif"]:
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode("utf-8")
                    node["binary"] = True
                    node["content"] = encoded
                else:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        node["content"] = f.read()
                    node["binary"] = False
            except:
                node["content"] = "Unable to read file"
                node["binary"] = False

        return node

    tree_data = build_tree(project_path)

    template = Template("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Project Explorer</title>
<style>
body { margin:0; display:flex; height:100vh; font-family:Segoe UI; }
.sidebar { width:30%; background:#1e272e; color:white; overflow:auto; padding:20px; }
.viewer { width:70%; padding:30px; overflow:auto; background:white; }
ul { list-style:none; padding-left:20px; }
.folder, .file { cursor:pointer; padding:4px; }
.folder:hover, .file:hover { background:rgba(255,255,255,0.1); }
pre { background:#2f3640; color:#f5f6fa; padding:20px; border-radius:8px; white-space:pre-wrap; }
img { max-width:100%; border-radius:8px; }
</style>
</head>
<body>

<div class="sidebar">
<h2>📁 Project Structure</h2>
<div id="tree"></div>
</div>

<div class="viewer">
<h2>📄 File Viewer</h2>
<div id="content">Select a file to view content</div>
</div>

<script>
const treeData = {{ tree | tojson }};

function build(node) {
    const li = document.createElement("li");

    if (node.type === "folder") {
        const span = document.createElement("div");
        span.textContent = "📁 " + node.name;
        span.className = "folder";

        const ul = document.createElement("ul");
        ul.style.display = "none";

        span.onclick = () => {
            ul.style.display = ul.style.display === "none" ? "block" : "none";
        };

        node.children.forEach(child => {
            ul.appendChild(build(child));
        });

        li.appendChild(span);
        li.appendChild(ul);
    }

    if (node.type === "file") {
        li.textContent = "📄 " + node.name;
        li.className = "file";

        li.onclick = () => {
            const contentDiv = document.getElementById("content");
            contentDiv.innerHTML = "";

            if (node.binary) {
                const img = document.createElement("img");
                img.src = "data:image/"+node.extension.replace(".","")+";base64,"+node.content;
                contentDiv.appendChild(img);
            } else {
                const pre = document.createElement("pre");
                pre.textContent = node.content;
                contentDiv.appendChild(pre);
            }
        };
    }

    return li;
}

const rootUl = document.createElement("ul");
rootUl.appendChild(build(treeData));
document.getElementById("tree").appendChild(rootUl);
</script>

</body>
</html>
""")

    html_content = template.render(tree=tree_data)

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("✅ Professional Static Explorer Generated:", output_html)

# ==============================
# MAIN
# ==============================

def main():
    os.makedirs(DOCS_DIR, exist_ok=True)

    views, models, forms, permissions, urls = collect_project_data()

    generate_markdown(views, models, forms, permissions, urls)
    generate_swagger(urls)
    # generate_architecture()
    generate_pdf()
    generate_docx()
    # generate_html()
    # generate_er_diagram()
    # folder_html = generate_folder_tree_html()
    # generate_html(folder_html, os.path.join(DOCS_DIR, "folder_structure.html"))
    generate_static_explorer()

    print("\n✅ ENTERPRISE DOCUMENTATION GENERATED SUCCESSFULLY")
    print("📂 Check the 'docs/' folder.")


if __name__ == "__main__":
    main()
