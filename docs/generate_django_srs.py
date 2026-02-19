import os
import ast
from datetime import datetime

PROJECT_PATH = "."
OUTPUT_FILE = "docs/Complete_Project_Documentation.md"

fr_counter = 1


def next_fr():
    global fr_counter
    fr_id = f"FR-{fr_counter:03}"
    fr_counter += 1
    return fr_id


def extract_views(file_path):
    views = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                views.append(node.name)
            elif isinstance(node, ast.ClassDef):
                views.append(node.name)
    except Exception:
        pass

    return views


def generate_folder_structure(md):
    md.write("## 📁 1. Project Folder Structure\n\n")
    for root, dirs, files in os.walk(PROJECT_PATH):
        level = root.replace(PROJECT_PATH, "").count(os.sep)
        indent = "  " * level
        md.write(f"{indent}- {os.path.basename(root)}/\n")
        subindent = "  " * (level + 1)
        for file in files:
            md.write(f"{subindent}- {file}\n")
    md.write("\n")


def generate_functional_requirements(md):
    md.write("## 🎯 2. Functional Requirements\n\n")

    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            if file == "views.py":
                file_path = os.path.join(root, file)
                views = extract_views(file_path)

                for view in views:
                    fr_id = next_fr()
                    md.write(f"### {fr_id}\n")

                    if "add" in view.lower() or "create" in view.lower():
                        md.write(f"- The system shall allow users to create records using `{view}`.\n")
                    elif "edit" in view.lower() or "update" in view.lower():
                        md.write(f"- The system shall allow users to update records using `{view}`.\n")
                    elif "delete" in view.lower():
                        md.write(f"- The system shall allow users to delete records using `{view}`.\n")
                    elif "export" in view.lower():
                        md.write(f"- The system shall allow users to export data using `{view}`.\n")
                    elif "import" in view.lower():
                        md.write(f"- The system shall allow users to import bulk data using `{view}`.\n")
                    elif "dashboard" in view.lower():
                        md.write(f"- The system shall display dashboard analytics using `{view}`.\n")
                    elif "login" in view.lower():
                        md.write(f"- The system shall authenticate users using `{view}`.\n")
                    else:
                        md.write(f"- The system shall execute business logic via `{view}`.\n")

                    md.write(f"- Source: `{file}`\n\n")


def generate_non_functional(md):
    md.write("## ⚙️ 3. Non-Functional Requirements\n\n")
    md.write("- Performance: Response time < 3 seconds.\n")
    md.write("- Security: Role-based access control enforced.\n")
    md.write("- Scalability: System supports user growth.\n")
    md.write("- Maintainability: Modular Django architecture.\n")
    md.write("- Availability: 99% uptime target.\n\n")


def generate_run_guide(md):
    md.write("## ▶ 4. Local Installation & Run Guide\n\n")
    md.write("```bash\n")
    md.write("python -m venv venv\n")
    md.write("venv\\Scripts\\activate  # Windows\n")
    md.write("source venv/bin/activate  # Linux/Mac\n")
    md.write("pip install -r requirements.txt\n")
    md.write("python manage.py makemigrations\n")
    md.write("python manage.py migrate\n")
    md.write("python manage.py createsuperuser\n")
    md.write("python manage.py runserver\n")
    md.write("```\n\n")


def generate_deployment_guide(md):
    md.write("## 🚀 5. Production Deployment Guide (VPS)\n\n")
    md.write("```bash\n")
    md.write("sudo apt update\n")
    md.write("sudo apt install python3-pip python3-venv nginx\n")
    md.write("git clone <repo>\n")
    md.write("python3 -m venv venv\n")
    md.write("source venv/bin/activate\n")
    md.write("pip install -r requirements.txt\n")
    md.write("pip install gunicorn\n")
    md.write("python manage.py collectstatic\n")
    md.write("python manage.py migrate\n")
    md.write("gunicorn project_name.wsgi:application\n")
    md.write("```\n\n")


def generate_hosting_section(md):
    md.write("## 🌍 6. Recommended Hosting Providers\n\n")
    md.write("### VPS Providers\n")
    md.write("- DigitalOcean\n")
    md.write("- AWS\n")
    md.write("- Hostinger VPS\n")
    md.write("- Linode\n\n")
    md.write("Shared hosting is not recommended for Django production.\n\n")


def generate_architecture(md):
    md.write("## 🏗 7. System Architecture\n\n")
    md.write("```\n")
    md.write("User Browser\n")
    md.write("     ↓\n")
    md.write("Nginx (Web Server)\n")
    md.write("     ↓\n")
    md.write("Gunicorn (WSGI Server)\n")
    md.write("     ↓\n")
    md.write("Django Application\n")
    md.write("     ↓\n")
    md.write("PostgreSQL Database\n")
    md.write("```\n\n")


def generate_security(md):
    md.write("## 🔐 8. Security Hardening Checklist\n\n")
    md.write("- DEBUG = False\n")
    md.write("- Use HTTPS (SSL)\n")
    md.write("- Use PostgreSQL in production\n")
    md.write("- Environment variables for secrets\n")
    md.write("- Regular database backups\n\n")


def generate_scalability(md):
    md.write("## 📈 9. Scalability Strategy\n\n")
    md.write("- Phase 1: Single VPS\n")
    md.write("- Phase 2: Increase RAM + Redis cache\n")
    md.write("- Phase 3: Load balancer + Docker\n\n")


def generate_backup(md):
    md.write("## 💾 10. Backup Strategy\n\n")
    md.write("```bash\n")
    md.write("pg_dump database_name > backup.sql\n")
    md.write("```\n\n")


def generate_client_delivery(md):
    md.write("## 📦 11. Client Delivery Checklist\n\n")
    md.write("- Source Code\n")
    md.write("- requirements.txt\n")
    md.write("- Deployment Guide\n")
    md.write("- Admin Credentials\n")
    md.write("- Database Backup\n")
    md.write("- Architecture Diagram\n\n")


def generate_document():
    os.makedirs("docs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as md:
        md.write("# Complete Django Project Documentation\n\n")
        md.write(f"Generated on: {datetime.now()}\n\n")

        generate_folder_structure(md)
        generate_functional_requirements(md)
        generate_non_functional(md)
        generate_run_guide(md)
        generate_deployment_guide(md)
        generate_hosting_section(md)
        generate_architecture(md)
        generate_security(md)
        generate_scalability(md)
        generate_backup(md)
        generate_client_delivery(md)

    print(f"\n✅ Complete documentation generated at: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_document()
