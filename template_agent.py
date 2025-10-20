"""
TemplateAgent - A flexible template management and content generation system.

This agent allows users to:
1. Upload custom templates
2. Store templates persistently
3. Generate content using stored templates
4. Manage multiple templates for different content types
"""

import json
import os
from typing import Dict, Optional, Any
from smolagents import tool


class TemplateAgent:
    """Agent for managing templates and generating formatted content."""

    def __init__(self, template_dir: str = "templates"):
        """Initialize the TemplateAgent.

        Args:
            template_dir: Directory to store template files
        """
        self.template_dir = template_dir
        self.templates = {}
        self.template_file = os.path.join(template_dir, "templates.json")

        # Create template directory if it doesn't exist
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)

        # Load existing templates
        self._load_templates()

    def _load_templates(self):
        """Load templates from storage."""
        if os.path.exists(self.template_file):
            try:
                with open(self.template_file, 'r') as f:
                    self.templates = json.load(f)
            except Exception as e:
                print(f"Error loading templates: {e}")
                self.templates = {}
        else:
            self.templates = {}

    def _save_templates(self):
        """Save templates to storage."""
        try:
            with open(self.template_file, 'w') as f:
                json.dump(self.templates, f, indent=2)
        except Exception as e:
            print(f"Error saving templates: {e}")

    def upload_template(self, name: str, template: str, description: str = "") -> str:
        """Upload and store a new template.

        Args:
            name: Unique name for the template
            template: The template string with placeholders (e.g., {variable})
            description: Optional description of what the template is for

        Returns:
            Confirmation message
        """
        # Validate template for common errors
        validation_error = self._validate_template(template)
        if validation_error:
            return f"Template validation failed: {validation_error}\n\nTip: Use single braces like {{variable}}, not double braces like {{{{variable}}}}"

        self.templates[name] = {
            "template": template,
            "description": description
        }
        self._save_templates()
        return f"Template '{name}' uploaded successfully! {len(self.templates)} templates stored."

    def _validate_template(self, template: str) -> str:
        """Validate template for common formatting errors.

        Args:
            template: Template string to validate

        Returns:
            Error message if invalid, empty string if valid
        """
        # Check for double braces which cause formatting errors
        if "{{" in template or "}}" in template:
            return "Template contains double braces {{ or }}. Use single braces for placeholders: {variable}"

        # Check for mismatched braces
        open_count = template.count("{")
        close_count = template.count("}")

        if open_count != close_count:
            return f"Mismatched braces: {open_count} opening {{ but {close_count} closing }}"

        # Try to find valid placeholder pattern
        import re
        placeholders = re.findall(r'\{(\w+)\}', template)

        # Check for empty placeholders
        if "{}" in template:
            return "Template contains empty placeholder {}. Placeholders must have a name like {variable}"

        return ""  # Valid template

    def get_template(self, name: str) -> Optional[Dict[str, str]]:
        """Retrieve a template by name.

        Args:
            name: Name of the template

        Returns:
            Template dictionary or None if not found
        """
        return self.templates.get(name)

    def list_templates(self) -> str:
        """List all available templates.

        Returns:
            Formatted string of all templates
        """
        if not self.templates:
            return "No templates stored yet."

        result = f"=� Available Templates ({len(self.templates)}):\n\n"
        for name, data in self.templates.items():
            desc = data.get('description', 'No description')
            result += f" {name}: {desc}\n"
        return result

    def delete_template(self, name: str) -> str:
        """Delete a template.

        Args:
            name: Name of the template to delete

        Returns:
            Confirmation message
        """
        if name in self.templates:
            del self.templates[name]
            self._save_templates()
            return f"Template '{name}' deleted successfully."
        return f"Template '{name}' not found."

    def generate_content(self, template_name: str, data: Dict[str, Any]) -> str:
        """Generate content using a stored template.

        Args:
            template_name: Name of the template to use
            data: Dictionary of data to fill into the template

        Returns:
            Formatted content or error message
        """
        template_data = self.get_template(template_name)

        if not template_data:
            return f"Error: Template '{template_name}' not found. Available templates: {', '.join(self.templates.keys())}"

        template = template_data['template']

        try:
            # Replace placeholders with actual data
            content = template.format(**data)
            return content
        except KeyError as e:
            missing_key = str(e).strip("'")
            return f"Error: Missing data for placeholder '{missing_key}' in template. Provided keys: {list(data.keys())}"
        except ValueError as e:
            # This catches formatting errors like "Single '}' encountered"
            error_msg = str(e)
            if "Single" in error_msg and ("}" in error_msg or "{" in error_msg):
                return f"Error: Template has malformed braces. Use single braces for placeholders like {{variable}}, not double braces. Error: {error_msg}"
            return f"Error in template format: {error_msg}"
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def update_template(self, name: str, template: str, description: str = "") -> str:
        """Update an existing template.

        Args:
            name: Name of the template to update
            template: New template string
            description: New description

        Returns:
            Confirmation message
        """
        if name not in self.templates:
            return f"Template '{name}' not found. Use upload_template to create a new one."

        self.templates[name] = {
            "template": template,
            "description": description
        }
        self._save_templates()
        return f"Template '{name}' updated successfully!"

    def view_template(self, name: str) -> str:
        """View the content of a specific template.

        Args:
            name: Name of the template

        Returns:
            Template content and description
        """
        template_data = self.get_template(name)

        if not template_data:
            return f"Template '{name}' not found."

        result = f"=� Template: {name}\n"
        result += f"Description: {template_data.get('description', 'No description')}\n\n"
        result += f"Template Content:\n{template_data['template']}"
        return result


# Create global instance
template_agent = TemplateAgent()


def read_template_from_file(file_path: str) -> str:
    """Read template content from a text file.

    Args:
        file_path: Path to the template file (.txt, .md, etc.)

    Returns:
        Template content as string
    """
    import os
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_template_from_pdf(pdf_path: str) -> str:
    """Read template content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text from PDF
    """
    try:
        import PyPDF2
    except ImportError:
        return "Error: PyPDF2 not installed. Install with: pip install PyPDF2"

    import os
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text.strip()


# Tools for use with CodeAgent
@tool
def upload_template(name: str, template: str, description: str = "") -> str:
    """Upload and store a new template for content generation.

    Args:
        name: Unique name for the template (e.g., 'weather_report', 'email_summary')
        template: The template string with placeholders like {variable_name}
        description: Optional description of the template's purpose

    Returns:
        Confirmation message

    Example:
        upload_template("greeting", "Hello {name}, welcome to {location}!", "A simple greeting template")
    """
    return template_agent.upload_template(name, template, description)


@tool
def list_all_templates() -> str:
    """List all available templates.

    Returns:
        Formatted list of all stored templates
    """
    return template_agent.list_templates()


@tool
def view_template_content(name: str) -> str:
    """View the content of a specific template.

    Args:
        name: Name of the template to view

    Returns:
        Template content and description
    """
    return template_agent.view_template(name)


@tool
def delete_template(name: str) -> str:
    """Delete a template.

    Args:
        name: Name of the template to delete

    Returns:
        Confirmation message
    """
    return template_agent.delete_template(name)


@tool
def generate_from_template(template_name: str, data: dict) -> str:
    """Generate formatted content using a stored template.

    Args:
        template_name: Name of the template to use
        data: Dictionary containing the data to fill into the template

    Returns:
        Formatted content

    Example:
        data = {"name": "Alice", "location": "Paris"}
        generate_from_template("greeting", data)
    """
    return template_agent.generate_content(template_name, data)


@tool
def update_existing_template(name: str, template: str, description: str = "") -> str:
    """Update an existing template.

    Args:
        name: Name of the template to update
        template: New template string
        description: New description

    Returns:
        Confirmation message
    """
    return template_agent.update_template(name, template, description)


@tool
def upload_template_from_file(name: str, file_path: str, description: str = "") -> str:
    """Upload a template from a text file (.txt, .md, etc.).

    Args:
        name: Unique name for the template
        file_path: Path to the template file
        description: Optional description

    Returns:
        Confirmation message

    Example:
        upload_template_from_file("my_template", "/path/to/template.txt", "My custom template")
    """
    try:
        template_content = read_template_from_file(file_path)
        return template_agent.upload_template(name, template_content, description)
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def upload_template_from_pdf(name: str, pdf_path: str, description: str = "") -> str:
    """Upload a template from a PDF file.

    Args:
        name: Unique name for the template
        pdf_path: Path to the PDF file
        description: Optional description

    Returns:
        Confirmation message

    Example:
        upload_template_from_pdf("weather_template", "/path/to/template.pdf", "Weather template from PDF")
    """
    try:
        template_content = read_template_from_pdf(pdf_path)
        return template_agent.upload_template(name, template_content, description)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
