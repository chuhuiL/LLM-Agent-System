"""
PlannerAgent - Orchestrates the medical note-taking workflow

Coordinates:
- Input processing
- SOAP agent execution (S → O → A → P)
- Human review checkpoints
- Summary generation
- Output formatting

"""

from typing import Dict, Any, List, Optional
from enum import Enum
import json


class WorkflowStage(Enum):
    """Stages in the medical note workflow."""
    INPUT = "input"
    SUBJECTIVE = "subjective"
    OBJECTIVE = "objective"
    ASSESSMENT = "assessment"
    PLAN = "plan"
    SUMMARY = "summary"
    COMPLETE = "complete"


class PlannerAgent:
    """Orchestrates the entire medical note-taking workflow."""

    def __init__(self):
        self.name = "PlannerAgent"
        self.current_stage = WorkflowStage.INPUT
        self.workflow_data = {
            "input": None,
            "subjective": None,
            "objective": None,
            "assessment": None,
            "plan": None,
            "summary": None,
            "metadata": {
                "date": None,
                "provider": None,
                "patient_id": None,
                "encounter_type": None
            }
        }
        self.review_history = []

    def start_workflow(self, input_data: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Initialize a new medical note workflow.

        Args:
            input_data: Raw conversation, transcript, or structured input
            metadata: Optional metadata (provider, patient ID, date, etc.)

        Returns:
            Workflow initialization status
        """
        self.workflow_data["input"] = input_data
        if metadata:
            self.workflow_data["metadata"].update(metadata)

        self.current_stage = WorkflowStage.SUBJECTIVE

        return {
            "status": "initialized",
            "current_stage": self.current_stage.value,
            "next_action": "extract_subjective"
        }

    def advance_stage(self, stage_data: Dict[str, Any], approved: bool = True) -> Dict[str, Any]:
        """Advance to the next workflow stage.

        Args:
            stage_data: Data from completed stage
            approved: Whether the stage was approved by human reviewer

        Returns:
            Next stage information
        """
        if not approved:
            return {
                "status": "revision_needed",
                "current_stage": self.current_stage.value,
                "message": "Stage not approved. Please revise."
            }

        # Store the approved stage data
        stage_name = self.current_stage.value
        self.workflow_data[stage_name] = stage_data

        # Determine next stage
        stage_sequence = [
            WorkflowStage.SUBJECTIVE,
            WorkflowStage.OBJECTIVE,
            WorkflowStage.ASSESSMENT,
            WorkflowStage.PLAN,
            WorkflowStage.SUMMARY,
            WorkflowStage.COMPLETE
        ]

        current_index = stage_sequence.index(self.current_stage)
        if current_index < len(stage_sequence) - 1:
            self.current_stage = stage_sequence[current_index + 1]

        return {
            "status": "advanced",
            "current_stage": self.current_stage.value,
            "next_action": self._get_next_action()
        }

    def _get_next_action(self) -> str:
        """Determine the next action based on current stage."""
        action_map = {
            WorkflowStage.SUBJECTIVE: "extract_subjective",
            WorkflowStage.OBJECTIVE: "extract_objective",
            WorkflowStage.ASSESSMENT: "generate_assessment",
            WorkflowStage.PLAN: "generate_plan",
            WorkflowStage.SUMMARY: "generate_summary",
            WorkflowStage.COMPLETE: "export_note"
        }
        return action_map.get(self.current_stage, "unknown")

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status.

        Returns:
            Complete workflow status including all completed stages
        """
        completed_stages = []
        for stage in [WorkflowStage.SUBJECTIVE, WorkflowStage.OBJECTIVE,
                      WorkflowStage.ASSESSMENT, WorkflowStage.PLAN]:
            if self.workflow_data[stage.value] is not None:
                completed_stages.append(stage.value)

        return {
            "current_stage": self.current_stage.value,
            "completed_stages": completed_stages,
            "pending_stages": self._get_pending_stages(),
            "workflow_data": self.workflow_data,
            "metadata": self.workflow_data["metadata"]
        }

    def _get_pending_stages(self) -> List[str]:
        """Get list of pending workflow stages."""
        all_stages = ["subjective", "objective", "assessment", "plan"]
        completed = [s for s in all_stages if self.workflow_data[s] is not None]
        return [s for s in all_stages if s not in completed]

    def record_review(self, stage: str, feedback: str, action: str) -> None:
        """Record human review feedback.

        Args:
            stage: Stage being reviewed
            feedback: Human feedback
            action: Action taken (approved, revised, rejected)
        """
        self.review_history.append({
            "stage": stage,
            "feedback": feedback,
            "action": action,
            "timestamp": None  # Add timestamp in production
        })

    def get_stage_dependencies(self, stage: str) -> List[str]:
        """Get required prior stages for a given stage.

        Args:
            stage: Stage name

        Returns:
            List of required prior stages
        """
        dependencies = {
            "subjective": [],
            "objective": ["subjective"],
            "assessment": ["subjective", "objective"],
            "plan": ["subjective", "objective", "assessment"],
            "summary": ["subjective", "objective", "assessment", "plan"]
        }
        return dependencies.get(stage, [])

    def validate_stage_ready(self, stage: str) -> bool:
        """Check if all dependencies for a stage are met.

        Args:
            stage: Stage to validate

        Returns:
            True if stage can proceed, False otherwise
        """
        dependencies = self.get_stage_dependencies(stage)
        for dep in dependencies:
            if self.workflow_data[dep] is None:
                return False
        return True

    def reset_workflow(self) -> None:
        """Reset workflow to initial state."""
        self.current_stage = WorkflowStage.INPUT
        self.workflow_data = {
            "input": None,
            "subjective": None,
            "objective": None,
            "assessment": None,
            "plan": None,
            "summary": None,
            "metadata": {
                "date": None,
                "provider": None,
                "patient_id": None,
                "encounter_type": None
            }
        }
        self.review_history = []


# Global instance
planner_agent = PlannerAgent()


def get_planner_status() -> Dict[str, Any]:
    """Get current planner workflow status.

    Returns:
        Workflow status dictionary
    """
    return planner_agent.get_workflow_status()


def start_medical_note(input_text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """Start a new medical note workflow.

    Args:
        input_text: Patient conversation or medical data
        metadata: Optional metadata dictionary

    Returns:
        Initialization status
    """
    return planner_agent.start_workflow(input_text, metadata)


def advance_workflow(stage_data: Dict[str, Any], approved: bool = True) -> Dict[str, Any]:
    """Advance workflow to next stage.

    Args:
        stage_data: Completed stage data
        approved: Whether stage was approved

    Returns:
        Next stage information
    """
    return planner_agent.advance_stage(stage_data, approved)
