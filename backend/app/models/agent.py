from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Text, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class TaskStatus(str, enum.Enum):
    """Status of agent task."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, enum.Enum):
    """Types of agent tasks."""
    NOTE_GENERATION = "note_generation"
    NOTE_REVIEW = "note_review"
    EXTRACTION = "extraction"
    CLINICAL_REASONING = "clinical_reasoning"
    TEMPLATE_FILLING = "template_filling"
    QUALITY_REVIEW = "quality_review"


class AgentTask(Base):
    """Agent task execution record."""

    __tablename__ = "agent_tasks"

    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, nullable=False, index=True)
    task_type = Column(SQLEnum(TaskType), nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    encounter = relationship("Encounter", back_populates="agent_tasks")
    executions = relationship("AgentExecution", back_populates="task", cascade="all, delete-orphan")
    reviews = relationship("HumanReview", back_populates="task", cascade="all, delete-orphan")
    reflection_logs = relationship("ReflectionLog", back_populates="task", cascade="all, delete-orphan")

    @property
    def duration_seconds(self) -> int:
        """Calculate task duration in seconds."""
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return 0

    def __repr__(self):
        return f"<AgentTask(id={self.id}, encounter_id={self.encounter_id}, type={self.task_type}, status={self.status})>"


class AgentExecution(Base):
    """Individual agent execution within a task."""

    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False, index=True)
    agent_name = Column(String(100), nullable=False)  # e.g., "extraction", "reasoning"
    agent_version = Column(String(50), nullable=True)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)  # LLM model, tokens used, etc.
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    success = Column(Boolean, default=False, nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    task = relationship("AgentTask", back_populates="executions")

    @property
    def duration_seconds(self) -> float:
        """Calculate execution duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def __repr__(self):
        return f"<AgentExecution(id={self.id}, task_id={self.task_id}, agent={self.agent_name})>"


class ReviewAction(str, enum.Enum):
    """Human review actions."""
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    REQUEST_CHANGES = "request_changes"


class HumanReview(Base):
    """Human review records for agent outputs."""

    __tablename__ = "human_reviews"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False, index=True)
    reviewer_id = Column(Integer, nullable=False)
    action = Column(SQLEnum(ReviewAction), nullable=False)
    feedback = Column(Text, nullable=True)
    changes_made = Column(JSON, nullable=True)  # Track what was modified
    quality_score = Column(Float, nullable=True)  # Optional quality rating
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    task = relationship("AgentTask", back_populates="reviews")

    def __repr__(self):
        return f"<HumanReview(id={self.id}, task_id={self.task_id}, action={self.action})>"


class ReflectionLog(Base):
    """Reflection agent learning logs."""

    __tablename__ = "reflection_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False, index=True)
    iteration = Column(Integer, nullable=False, default=1)
    feedback_analysis = Column(JSON, nullable=True)  # Analyzed feedback patterns
    refinements = Column(JSON, nullable=True)  # What was changed
    improved_output = Column(JSON, nullable=True)  # New generated output
    improvement_score = Column(Float, nullable=True)  # Quality improvement measure
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    task = relationship("AgentTask", back_populates="reflection_logs")

    def __repr__(self):
        return f"<ReflectionLog(id={self.id}, task_id={self.task_id}, iteration={self.iteration})>"
