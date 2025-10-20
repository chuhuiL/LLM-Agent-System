"""
HumanReflectorAgent - Interactive review and feedback system

Handles:
- Presenting SOAP sections for human review
- Collecting feedback and corrections
- Rebuilding sections based on input
- Tracking changes and revision history

"""

from typing import Dict, Any, List, Optional


class HumanReflectorAgent:
    """Manages human-in-the-loop review and feedback."""

    def __init__(self):
        self.name = "HumanReflectorAgent"
        self.revision_history = []

    def present_for_review(self, section: str, data: Dict[str, Any], formatted_text: str) -> Dict[str, Any]:
        """Present a SOAP section for human review.

        Args:
            section: Section name (subjective, objective, assessment, plan)
            data: Structured data for the section
            formatted_text: Human-readable formatted text

        Returns:
            Review package for display
        """
        review_package = {
            "section": section,
            "formatted_text": formatted_text,
            "structured_data": data,
            "actions": ["approve", "edit", "regenerate", "add_note"],
            "status": "pending_review"
        }

        return review_package

    def collect_feedback(self, section: str, action: str, feedback: str = "", edits: Dict[str, Any] = None) -> Dict[str, Any]:
        """Collect human feedback on a section.

        Args:
            section: Section being reviewed
            action: Action taken (approve, edit, regenerate, add_note)
            feedback: Free-text feedback
            edits: Dictionary of specific edits made

        Returns:
            Processed feedback result
        """
        feedback_record = {
            "section": section,
            "action": action,
            "feedback": feedback,
            "edits": edits or {},
            "timestamp": None  # Add timestamp in production
        }

        self.revision_history.append(feedback_record)

        result = {
            "status": action,
            "requires_regeneration": action in ["edit", "regenerate"],
            "approved": action == "approve",
            "feedback_recorded": True
        }

        return result

    def apply_edits(self, original_data: Dict[str, Any], edits: Dict[str, Any]) -> Dict[str, Any]:
        """Apply human edits to structured data.

        Args:
            original_data: Original section data
            edits: Dictionary of edits to apply

        Returns:
            Updated data with edits applied
        """
        updated_data = original_data.copy()

        # Deep merge edits into original data
        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = deep_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        updated_data = deep_update(updated_data, edits)

        return updated_data

    def get_revision_history(self, section: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get revision history.

        Args:
            section: Optional section filter

        Returns:
            List of revision records
        """
        if section:
            return [r for r in self.revision_history if r["section"] == section]
        return self.revision_history

    def generate_review_prompt(self, section: str, formatted_text: str) -> str:
        """Generate interactive review prompt for CLI.

        Args:
            section: Section being reviewed
            formatted_text: Formatted section text

        Returns:
            Review prompt string
        """
        prompt = f"\n{'═' * 70}\n"
        prompt += f"REVIEW: {section.upper()} Section\n"
        prompt += f"{'═' * 70}\n\n"
        prompt += formatted_text
        prompt += f"\n\n{'─' * 70}\n"
        prompt += "Actions:\n"
        prompt += "  [A] Approve - Accept as-is and continue\n"
        prompt += "  [E] Edit - Make specific changes\n"
        prompt += "  [R] Regenerate - AI generates new version\n"
        prompt += "  [N] Add Note - Add comment/instruction\n"
        prompt += f"{'─' * 70}\n"

        return prompt

    def interactive_review(self, section: str, data: Dict[str, Any], formatted_text: str) -> Dict[str, Any]:
        """Conduct interactive review (for CLI mode).

        Args:
            section: Section name
            data: Section data
            formatted_text: Formatted text

        Returns:
            Review result
        """
        prompt = self.generate_review_prompt(section, formatted_text)
        print(prompt)

        while True:
            choice = input("\nYour choice [A/E/R/N]: ").strip().upper()

            if choice == 'A':
                return self.collect_feedback(section, "approve")

            elif choice == 'E':
                print("\nEnter your edits (or 'done' to finish):")
                print("Format: field_name=new_value")
                edits = {}
                while True:
                    edit_input = input("> ").strip()
                    if edit_input.lower() == 'done':
                        break
                    if '=' in edit_input:
                        field, value = edit_input.split('=', 1)
                        edits[field.strip()] = value.strip()

                return self.collect_feedback(section, "edit", edits=edits)

            elif choice == 'R':
                feedback = input("What should be different? ")
                return self.collect_feedback(section, "regenerate", feedback=feedback)

            elif choice == 'N':
                note = input("Enter your note: ")
                return self.collect_feedback(section, "add_note", feedback=note)

            else:
                print("Invalid choice. Please choose A, E, R, or N.")


# Global instance
human_reflector = HumanReflectorAgent()


def review_section(section: str, data_dict: Dict[str, Any], formatted: str) -> Dict[str, Any]:
    """Present section for human review.

    Args:
        section: Section name
        data_dict: Section data
        formatted: Formatted text

    Returns:
        Review result
    """
    return human_reflector.present_for_review(section, data_dict, formatted)


def interactive_section_review(section: str, data_dict: Dict[str, Any], formatted: str) -> Dict[str, Any]:
    """Conduct interactive CLI review.

    Args:
        section: Section name
        data_dict: Section data
        formatted: Formatted text

    Returns:
        Review result with user feedback
    """
    return human_reflector.interactive_review(section, data_dict, formatted)
