"""
SOAP Agent - Medical Note Generation System
Contains 4 specialized sub-agents for each SOAP component:
- SubjectiveAgent: Extract patient complaints, symptoms, history
- ObjectiveAgent: Extract vital signs, physical exam findings
- AssessmentAgent: Generate diagnosis and clinical assessment
- PlanAgent: Create treatment plan and follow-up

"""

from typing import Dict, Any, List
from smolagents import tool
import json


class SubjectiveAgent:
    """Extracts and structures subjective patient information."""

    def __init__(self):
        self.name = "SubjectiveAgent"

    def extract_subjective(self, conversation: str) -> Dict[str, Any]:
        """Extract subjective information from patient conversation.

        Args:
            conversation: Raw conversation text or transcript

        Returns:
            Dictionary with subjective data structured as:
            - chief_complaint: Main reason for visit
            - history_present_illness: Detailed HPI
            - review_of_systems: ROS by system
            - past_medical_history: PMH
            - medications: Current medications
            - allergies: Known allergies
            - social_history: Social factors
            - family_history: Family medical history
        """
        # This will be enhanced with LLM processing
        subjective_data = {
            "chief_complaint": "",
            "history_present_illness": "",
            "review_of_systems": {},
            "past_medical_history": [],
            "medications": [],
            "allergies": [],
            "social_history": {},
            "family_history": []
        }

        return subjective_data

    def format_subjective(self, data: Dict[str, Any]) -> str:
        """Format subjective data for display/review.

        Args:
            data: Structured subjective data

        Returns:
            Formatted string for human review
        """
        output = "═══ SUBJECTIVE ═══\n\n"
        output += f"Chief Complaint: {data.get('chief_complaint', 'N/A')}\n\n"
        output += f"History of Present Illness:\n{data.get('history_present_illness', 'N/A')}\n\n"

        if data.get('medications'):
            output += "Medications:\n"
            for med in data['medications']:
                output += f"  • {med}\n"
            output += "\n"

        if data.get('allergies'):
            output += "Allergies:\n"
            for allergy in data['allergies']:
                output += f"  • {allergy}\n"
            output += "\n"

        if data.get('past_medical_history'):
            output += "Past Medical History:\n"
            for pmh in data['past_medical_history']:
                output += f"  • {pmh}\n"

        return output


class ObjectiveAgent:
    """Extracts and structures objective clinical findings."""

    def __init__(self):
        self.name = "ObjectiveAgent"

    def extract_objective(self, conversation: str, clinical_data: Dict = None) -> Dict[str, Any]:
        """Extract objective clinical findings.

        Args:
            conversation: Raw conversation/documentation
            clinical_data: Optional structured clinical data (vitals, labs)

        Returns:
            Dictionary with objective data:
            - vital_signs: BP, HR, RR, Temp, SpO2, etc.
            - physical_exam: PE findings by system
            - laboratory_results: Lab values
            - imaging_results: Imaging findings
            - other_findings: Additional objective data
        """
        objective_data = {
            "vital_signs": {
                "blood_pressure": "",
                "heart_rate": "",
                "respiratory_rate": "",
                "temperature": "",
                "oxygen_saturation": "",
                "weight": "",
                "height": "",
                "bmi": ""
            },
            "physical_exam": {},
            "laboratory_results": {},
            "imaging_results": {},
            "other_findings": []
        }

        return objective_data

    def format_objective(self, data: Dict[str, Any]) -> str:
        """Format objective data for display/review."""
        output = "═══ OBJECTIVE ═══\n\n"

        # Vital Signs
        vs = data.get('vital_signs', {})
        if any(vs.values()):
            output += "Vital Signs:\n"
            if vs.get('blood_pressure'):
                output += f"  BP: {vs['blood_pressure']}\n"
            if vs.get('heart_rate'):
                output += f"  HR: {vs['heart_rate']}\n"
            if vs.get('respiratory_rate'):
                output += f"  RR: {vs['respiratory_rate']}\n"
            if vs.get('temperature'):
                output += f"  Temp: {vs['temperature']}\n"
            if vs.get('oxygen_saturation'):
                output += f"  SpO2: {vs['oxygen_saturation']}\n"
            output += "\n"

        # Physical Exam
        pe = data.get('physical_exam', {})
        if pe:
            output += "Physical Examination:\n"
            for system, findings in pe.items():
                output += f"  {system}: {findings}\n"
            output += "\n"

        # Lab Results
        labs = data.get('laboratory_results', {})
        if labs:
            output += "Laboratory Results:\n"
            for test, value in labs.items():
                output += f"  {test}: {value}\n"

        return output


class AssessmentAgent:
    """Generates clinical assessment and diagnosis."""

    def __init__(self):
        self.name = "AssessmentAgent"

    def generate_assessment(self, subjective: Dict, objective: Dict) -> Dict[str, Any]:
        """Generate clinical assessment from S and O data.

        Args:
            subjective: Subjective data from SubjectiveAgent
            objective: Objective data from ObjectiveAgent

        Returns:
            Dictionary with assessment:
            - primary_diagnosis: Main diagnosis
            - differential_diagnoses: List of differentials
            - icd_codes: ICD-10 codes
            - clinical_impression: Narrative assessment
            - problem_list: Active problems
        """
        assessment_data = {
            "primary_diagnosis": "",
            "differential_diagnoses": [],
            "icd_codes": [],
            "clinical_impression": "",
            "problem_list": [],
            "severity": ""
        }

        return assessment_data

    def format_assessment(self, data: Dict[str, Any]) -> str:
        """Format assessment data for display/review."""
        output = "═══ ASSESSMENT ═══\n\n"

        if data.get('primary_diagnosis'):
            output += f"Primary Diagnosis: {data['primary_diagnosis']}\n"

        if data.get('icd_codes'):
            output += f"ICD-10 Codes: {', '.join(data['icd_codes'])}\n\n"

        if data.get('differential_diagnoses'):
            output += "Differential Diagnoses:\n"
            for ddx in data['differential_diagnoses']:
                output += f"  • {ddx}\n"
            output += "\n"

        if data.get('clinical_impression'):
            output += f"Clinical Impression:\n{data['clinical_impression']}\n\n"

        if data.get('problem_list'):
            output += "Active Problems:\n"
            for problem in data['problem_list']:
                output += f"  • {problem}\n"

        return output


class PlanAgent:
    """Generates treatment plan and follow-up."""

    def __init__(self):
        self.name = "PlanAgent"

    def generate_plan(self, assessment: Dict) -> Dict[str, Any]:
        """Generate treatment plan based on assessment.

        Args:
            assessment: Assessment data from AssessmentAgent

        Returns:
            Dictionary with plan:
            - medications: Prescriptions and dosing
            - procedures: Procedures to perform
            - diagnostic_tests: Tests to order
            - referrals: Specialist referrals
            - patient_education: Education provided
            - follow_up: Follow-up instructions
            - disposition: Patient disposition
        """
        plan_data = {
            "medications": [],
            "procedures": [],
            "diagnostic_tests": [],
            "referrals": [],
            "patient_education": [],
            "follow_up": "",
            "disposition": ""
        }

        return plan_data

    def format_plan(self, data: Dict[str, Any]) -> str:
        """Format plan data for display/review."""
        output = "═══ PLAN ═══\n\n"

        if data.get('medications'):
            output += "Medications:\n"
            for med in data['medications']:
                output += f"  • {med}\n"
            output += "\n"

        if data.get('diagnostic_tests'):
            output += "Diagnostic Tests:\n"
            for test in data['diagnostic_tests']:
                output += f"  • {test}\n"
            output += "\n"

        if data.get('procedures'):
            output += "Procedures:\n"
            for proc in data['procedures']:
                output += f"  • {proc}\n"
            output += "\n"

        if data.get('referrals'):
            output += "Referrals:\n"
            for ref in data['referrals']:
                output += f"  • {ref}\n"
            output += "\n"

        if data.get('patient_education'):
            output += "Patient Education:\n"
            for edu in data['patient_education']:
                output += f"  • {edu}\n"
            output += "\n"

        if data.get('follow_up'):
            output += f"Follow-up: {data['follow_up']}\n\n"

        if data.get('disposition'):
            output += f"Disposition: {data['disposition']}\n"

        return output


# Global instances
subjective_agent = SubjectiveAgent()
objective_agent = ObjectiveAgent()
assessment_agent = AssessmentAgent()
plan_agent = PlanAgent()


# Tool functions for CodeAgent integration
@tool
def extract_subjective_data(conversation: str) -> dict:
    """Extract subjective patient information from conversation.

    Args:
        conversation: Patient conversation or medical transcript

    Returns:
        Structured subjective data (chief complaint, HPI, PMH, medications, allergies)
    """
    return subjective_agent.extract_subjective(conversation)


@tool
def extract_objective_data(conversation: str, clinical_data: str = "") -> dict:
    """Extract objective clinical findings from documentation.

    Args:
        conversation: Clinical documentation
        clinical_data: Optional JSON string with structured clinical data

    Returns:
        Structured objective data (vital signs, physical exam, labs, imaging)
    """
    clinical_dict = json.loads(clinical_data) if clinical_data else None
    return objective_agent.extract_objective(conversation, clinical_dict)


@tool
def generate_assessment_data(subjective_json: str, objective_json: str) -> dict:
    """Generate clinical assessment from subjective and objective data.

    Args:
        subjective_json: JSON string of subjective data
        objective_json: JSON string of objective data

    Returns:
        Structured assessment (diagnosis, ICD codes, clinical impression)
    """
    subjective = json.loads(subjective_json)
    objective = json.loads(objective_json)
    return assessment_agent.generate_assessment(subjective, objective)


@tool
def generate_plan_data(assessment_json: str) -> dict:
    """Generate treatment plan from assessment.

    Args:
        assessment_json: JSON string of assessment data

    Returns:
        Structured plan (medications, tests, referrals, follow-up)
    """
    assessment = json.loads(assessment_json)
    return plan_agent.generate_plan(assessment)


@tool
def format_soap_section(section: str, data_json: str) -> str:
    """Format a SOAP section for human review.

    Args:
        section: Section name ('subjective', 'objective', 'assessment', 'plan')
        data_json: JSON string of section data

    Returns:
        Formatted string for display
    """
    data = json.loads(data_json)

    if section.lower() == 'subjective':
        return subjective_agent.format_subjective(data)
    elif section.lower() == 'objective':
        return objective_agent.format_objective(data)
    elif section.lower() == 'assessment':
        return assessment_agent.format_assessment(data)
    elif section.lower() == 'plan':
        return plan_agent.format_plan(data)
    else:
        return f"Unknown section: {section}"
