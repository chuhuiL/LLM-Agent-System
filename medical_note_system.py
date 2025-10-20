#!/usr/bin/env python3
"""
Medical Note-Taking Multi-Agent System
Main entry point for the medical documentation system

Integrates:
- TemplateAgent (existing)
- SOAP Agent (4 sub-agents: S, O, A, P)
- PlannerAgent (orchestration)
- HumanReflectorAgent (interactive review)
- SummaryAgent (final formatting)

Usage:
    python medical_note_system.py

"""

import sys
import os
from datetime import datetime

# Add medical_agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'medical_agents'))

from medical_agents.soap_agent import (
    subjective_agent, objective_agent, assessment_agent, plan_agent
)
from medical_agents.planner_agent import planner_agent
from medical_agents.human_reflector_agent import human_reflector
from medical_agents.summary_agent import summary_agent


class MedicalNoteSystem:
    """Main system orchestrator for medical note-taking."""

    def __init__(self):
        self.planner = planner_agent
        self.subjective = subjective_agent
        self.objective = objective_agent
        self.assessment = assessment_agent
        self.plan = plan_agent
        self.reflector = human_reflector
        self.summary = summary_agent

    def create_note_from_conversation(self, conversation: str, metadata: dict = None, review_mode: str = "interactive"):
        """Create a medical note from a patient conversation.

        Args:
            conversation: Patient conversation text/transcript
            metadata: Optional metadata (date, provider, patient_id)
            review_mode: "interactive", "auto", or "batch"

        Returns:
            Final formatted medical note
        """
        print("\n" + "=" * 70)
        print("MEDICAL NOTE-TAKING SYSTEM")
        print("=" * 70)

        # Initialize workflow
        if metadata is None:
            metadata = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "provider": "Dr. [Provider Name]",
                "patient_id": "[Patient ID]",
                "encounter_type": "Office Visit"
            }

        workflow_init = self.planner.start_workflow(conversation, metadata)
        print(f"\n✓ Workflow initialized: {workflow_init['current_stage']}")

        # STEP 1: Extract Subjective Data
        print("\n" + "─" * 70)
        print("STEP 1: Extracting Subjective Data...")
        print("─" * 70)

        subjective_data = self.subjective.extract_subjective(conversation)
        subjective_formatted = self.subjective.format_subjective(subjective_data)

        if review_mode == "interactive":
            review_result = self.reflector.interactive_review("subjective", subjective_data, subjective_formatted)

            if review_result["status"] == "edit":
                subjective_data = self.reflector.apply_edits(subjective_data, review_result.get("edits", {}))
                subjective_formatted = self.subjective.format_subjective(subjective_data)

            approved = review_result["approved"]
        else:
            print(subjective_formatted)
            approved = True

        self.planner.advance_stage(subjective_data, approved)

        # STEP 2: Extract Objective Data
        print("\n" + "─" * 70)
        print("STEP 2: Extracting Objective Data...")
        print("─" * 70)

        objective_data = self.objective.extract_objective(conversation)
        objective_formatted = self.objective.format_objective(objective_data)

        if review_mode == "interactive":
            review_result = self.reflector.interactive_review("objective", objective_data, objective_formatted)

            if review_result["status"] == "edit":
                objective_data = self.reflector.apply_edits(objective_data, review_result.get("edits", {}))
                objective_formatted = self.objective.format_objective(objective_data)

            approved = review_result["approved"]
        else:
            print(objective_formatted)
            approved = True

        self.planner.advance_stage(objective_data, approved)

        # STEP 3: Generate Assessment
        print("\n" + "─" * 70)
        print("STEP 3: Generating Assessment...")
        print("─" * 70)

        assessment_data = self.assessment.generate_assessment(subjective_data, objective_data)
        assessment_formatted = self.assessment.format_assessment(assessment_data)

        if review_mode == "interactive":
            review_result = self.reflector.interactive_review("assessment", assessment_data, assessment_formatted)

            if review_result["status"] == "edit":
                assessment_data = self.reflector.apply_edits(assessment_data, review_result.get("edits", {}))
                assessment_formatted = self.assessment.format_assessment(assessment_data)

            approved = review_result["approved"]
        else:
            print(assessment_formatted)
            approved = True

        self.planner.advance_stage(assessment_data, approved)

        # STEP 4: Generate Plan
        print("\n" + "─" * 70)
        print("STEP 4: Generating Plan...")
        print("─" * 70)

        plan_data = self.plan.generate_plan(assessment_data)
        plan_formatted = self.plan.format_plan(plan_data)

        if review_mode == "interactive":
            review_result = self.reflector.interactive_review("plan", plan_data, plan_formatted)

            if review_result["status"] == "edit":
                plan_data = self.reflector.apply_edits(plan_data, review_result.get("edits", {}))
                plan_formatted = self.plan.format_plan(plan_data)

            approved = review_result["approved"]
        else:
            print(plan_formatted)
            approved = True

        self.planner.advance_stage(plan_data, approved)

        # STEP 5: Generate Final Note
        print("\n" + "─" * 70)
        print("STEP 5: Generating Final Note...")
        print("─" * 70)

        soap_data = {
            "subjective": subjective_data,
            "objective": objective_data,
            "assessment": assessment_data,
            "plan": plan_data,
            "metadata": metadata
        }

        final_note = self.summary.compile_soap_note(soap_data, template="default")

        print("\n" + "=" * 70)
        print("FINAL MEDICAL NOTE")
        print("=" * 70)
        print(final_note)

        return final_note

    def quick_demo(self):
        """Run a quick demonstration with sample data."""
        sample_conversation = """
        Patient: I've been having chest pain for the past 2 days.
        Doctor: Tell me more about the chest pain.
        Patient: It's a sharp pain in the center of my chest, especially when I breathe deeply.
        Doctor: Any shortness of breath?
        Patient: Yes, a little bit.
        Doctor: Any fever?
        Patient: No fever.
        Doctor: Are you taking any medications?
        Patient: Just my blood pressure medication, lisinopril 10mg daily.
        Doctor: Any allergies?
        Patient: Penicillin - I get a rash.

        [Physical Exam]
        Vitals: BP 130/85, HR 78, RR 18, Temp 98.6F, SpO2 98%
        Lungs: Clear to auscultation bilaterally
        Heart: Regular rate and rhythm, no murmurs
        Chest: Tender to palpation over left chest wall

        [Assessment]
        This appears to be costochondritis - inflammation of the chest wall.
        No signs of cardiac or pulmonary pathology.

        [Plan]
        - Ibuprofen 400mg TID PRN for pain
        - Avoid strenuous activity for 1 week
        - Follow-up in 1 week if not improved
        - Return immediately if chest pain worsens or shortness of breath increases
        """

        print("\n" + "═" * 70)
        print("DEMO: Creating Medical Note from Sample Conversation")
        print("═" * 70)

        metadata = {
            "date": "2025-01-15",
            "provider": "Dr. Smith",
            "patient_id": "12345",
            "encounter_type": "Office Visit"
        }

        # Run in auto mode for demo (no human review)
        final_note = self.create_note_from_conversation(
            sample_conversation,
            metadata=metadata,
            review_mode="auto"
        )

        return final_note


def main():
    """Main entry point."""
    print("\n" + "═" * 70)
    print("MEDICAL NOTE-TAKING MULTI-AGENT SYSTEM")
    print("═" * 70)
    print("\nSelect Mode:")
    print("  [1] Interactive - Create note with human review at each step")
    print("  [2] Demo - Run quick demonstration with sample data")
    print("  [3] Batch - Process without interactive review")
    print("  [4] Exit")
    print("=" * 70)

    system = MedicalNoteSystem()

    while True:
        choice = input("\nYour choice [1-4]: ").strip()

        if choice == '1':
            print("\n" + "─" * 70)
            print("INTERACTIVE MODE")
            print("─" * 70)
            print("\nEnter patient conversation/transcript")
            print("(Type 'END' on a new line when done, or Ctrl+D):")
            print("─" * 70)

            lines = []
            try:
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
            except EOFError:
                pass

            conversation = "\n".join(lines)

            if not conversation.strip():
                print("\n❌ No conversation provided.")
                continue

            # Collect metadata
            print("\n" + "─" * 70)
            print("Metadata (press Enter to use defaults):")
            print("─" * 70)

            provider = input("Provider name [Dr. Provider]: ").strip() or "Dr. Provider"
            patient_id = input("Patient ID [AUTO]: ").strip() or "AUTO-" + datetime.now().strftime("%Y%m%d%H%M")
            encounter_type = input("Encounter type [Office Visit]: ").strip() or "Office Visit"

            metadata = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "provider": provider,
                "patient_id": patient_id,
                "encounter_type": encounter_type
            }

            final_note = system.create_note_from_conversation(
                conversation,
                metadata=metadata,
                review_mode="interactive"
            )

            # Offer to save
            save = input("\nSave note to file? [y/n]: ").strip().lower()
            if save == 'y':
                filename = f"medical_note_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(final_note)
                print(f"\n✓ Note saved to: {filename}")

        elif choice == '2':
            system.quick_demo()
            input("\nPress Enter to continue...")

        elif choice == '3':
            print("\n❌ Batch mode not yet implemented")

        elif choice == '4':
            print("\n👋 Goodbye!")
            break

        else:
            print("\n❌ Invalid choice. Please choose 1-4.")


if __name__ == "__main__":
    main()
