#!/usr/bin/env python3
"""
Interactive Template Creator
Allows users to create multi-line templates easily by pasting or typing.
"""

from template_agent import template_agent
import sys


def create_template_interactive():
    """Interactive mode for creating templates."""
    print("=" * 70)
    print("📝 Interactive Template Creator")
    print("=" * 70)
    print("\nThis tool helps you create multi-line templates.")
    print("You can paste your template directly!")
    print()

    # Get template name
    name = input("Template name: ").strip()
    if not name:
        print("❌ Template name cannot be empty")
        return

    # Get description
    description = input("Description (optional): ").strip()

    # Get template content
    print("\n📋 Enter your template content below.")
    print("   Use {variable_name} for placeholders")
    print("   Press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows) when done")
    print("   OR type 'END' on a new line")
    print("-" * 70)

    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
    except EOFError:
        pass  # User pressed Ctrl+D

    template_content = "\n".join(lines)

    if not template_content.strip():
        print("\n❌ Template content cannot be empty")
        return

    # Show preview
    print("\n" + "=" * 70)
    print("📄 Template Preview:")
    print("=" * 70)
    print(f"Name: {name}")
    print(f"Description: {description}")
    print("\nContent:")
    print("-" * 70)
    print(template_content)
    print("-" * 70)

    # Confirm
    confirm = input("\nSave this template? (y/n): ").strip().lower()

    if confirm == 'y':
        result = template_agent.upload_template(name, template_content, description)
        print(f"\n✅ {result}")
    else:
        print("\n❌ Template not saved")


def create_template_from_file():
    """Create template from a file."""
    print("=" * 70)
    print("📂 Create Template from File")
    print("=" * 70)

    name = input("Template name: ").strip()
    if not name:
        print("❌ Template name cannot be empty")
        return

    file_path = input("File path (.txt, .md, .pdf): ").strip()
    if not file_path:
        print("❌ File path cannot be empty")
        return

    description = input("Description (optional): ").strip()

    # Determine file type
    if file_path.lower().endswith('.pdf'):
        from template_agent import read_template_from_pdf
        try:
            content = read_template_from_pdf(file_path)
            result = template_agent.upload_template(name, content, description)
            print(f"\n✅ {result}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        from template_agent import read_template_from_file
        try:
            content = read_template_from_file(file_path)
            result = template_agent.upload_template(name, content, description)
            print(f"\n✅ {result}")
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    """Main menu."""
    while True:
        print("\n" + "=" * 70)
        print("🎨 Template Creator Menu")
        print("=" * 70)
        print("1. Create template interactively (paste multi-line text)")
        print("2. Create template from file (.txt, .md, .pdf)")
        print("3. List all templates")
        print("4. Exit")
        print()

        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            create_template_interactive()
        elif choice == '2':
            create_template_from_file()
        elif choice == '3':
            print("\n" + template_agent.list_templates())
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please choose 1-4")


if __name__ == "__main__":
    main()
