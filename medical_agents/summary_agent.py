"""
SummaryAgent - Final integration and formatting

Handles:
- Collecting outputs from all SOAP agents
- Applying selected templates
- Generating multiple output formats
- Adding metadata
- Formatting for EHR export

"""

from typing import Dict, Any, List, Optional
import json
from datetime import datetime


class SummaryAgent:
    """Generates final formatted medical notes from SOAP components."""

    def __init__(self):
        self.name = "SummaryAgent"

    def compile_soap_note(self, soap_data: Dict[str, Any], template: str = "default") -> str:
        """Compile complete SOAP note from individual sections.

        Args:
            soap_data: Dictionary containing all SOAP sections
            template: Template name to use for formatting

        Returns:
            Complete formatted SOAP note
        """
        # Extract sections
        subjective = soap_data.get("subjective", {})
        objective = soap_data.get("objective", {})
        assessment = soap_data.get("assessment", {})
        plan = soap_data.get("plan", {})
        metadata = soap_data.get("metadata", {})

        # Build note based on template
        if template == "default":
            note = self._format_default_soap(subjective, objective, assessment, plan, metadata)
        elif template == "concise":
            note = self._format_concise_soap(subjective, objective, assessment, plan, metadata)
        elif template == "detailed":
            note = self._format_detailed_soap(subjective, objective, assessment, plan, metadata)
        else:
            note = self._format_default_soap(subjective, objective, assessment, plan, metadata)

        return note

    def _format_default_soap(self, s: Dict, o: Dict, a: Dict, p: Dict, metadata: Dict) -> str:
        """Format using default SOAP template."""
        lines = []

        # Header
        lines.append("=" * 70)
        lines.append("MEDICAL NOTE - SOAP FORMAT")
        lines.append("=" * 70)

        if metadata.get("date"):
            lines.append(f"Date: {metadata['date']}")
        if metadata.get("provider"):
            lines.append(f"Provider: {metadata['provider']}")
        if metadata.get("patient_id"):
            lines.append(f"Patient ID: {metadata['patient_id']}")

        lines.append("")

        # Subjective
        lines.append("SUBJECTIVE:")
        lines.append("-" * 70)
        if s.get("chief_complaint"):
            lines.append(f"Chief Complaint: {s['chief_complaint']}")
        if s.get("history_present_illness"):
            lines.append(f"\nHistory of Present Illness:\n{s['history_present_illness']}")

        if s.get("medications"):
            lines.append("\nMedications:")
            for med in s['medications']:
                lines.append(f"  • {med}")

        if s.get("allergies"):
            lines.append("\nAllergies:")
            for allergy in s['allergies']:
                lines.append(f"  • {allergy}")

        lines.append("")

        # Objective
        lines.append("OBJECTIVE:")
        lines.append("-" * 70)

        vs = o.get("vital_signs", {})
        if any(vs.values()):
            lines.append("Vital Signs:")
            if vs.get("blood_pressure"):
                lines.append(f"  BP: {vs['blood_pressure']}")
            if vs.get("heart_rate"):
                lines.append(f"  HR: {vs['heart_rate']} bpm")
            if vs.get("temperature"):
                lines.append(f"  Temp: {vs['temperature']}")

        pe = o.get("physical_exam", {})
        if pe:
            lines.append("\nPhysical Examination:")
            for system, findings in pe.items():
                lines.append(f"  {system}: {findings}")

        lines.append("")

        # Assessment
        lines.append("ASSESSMENT:")
        lines.append("-" * 70)
        if a.get("primary_diagnosis"):
            lines.append(f"Primary Diagnosis: {a['primary_diagnosis']}")

        if a.get("icd_codes"):
            lines.append(f"ICD-10 Codes: {', '.join(a['icd_codes'])}")

        if a.get("clinical_impression"):
            lines.append(f"\nClinical Impression:\n{a['clinical_impression']}")

        lines.append("")

        # Plan
        lines.append("PLAN:")
        lines.append("-" * 70)

        if p.get("medications"):
            lines.append("Medications:")
            for med in p['medications']:
                lines.append(f"  • {med}")

        if p.get("diagnostic_tests"):
            lines.append("\nDiagnostic Tests:")
            for test in p['diagnostic_tests']:
                lines.append(f"  • {test}")

        if p.get("follow_up"):
            lines.append(f"\nFollow-up: {p['follow_up']}")

        if p.get("disposition"):
            lines.append(f"Disposition: {p['disposition']}")

        lines.append("")
        lines.append("=" * 70)
        lines.append(f"Note generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)

        return "\n".join(lines)

    def _format_concise_soap(self, s: Dict, o: Dict, a: Dict, p: Dict, metadata: Dict) -> str:
        """Format using concise template."""
        lines = []
        lines.append("SOAP NOTE - CONCISE")
        lines.append("")

        lines.append(f"S: {s.get('chief_complaint', 'N/A')}")
        lines.append(f"O: VS - BP: {o.get('vital_signs', {}).get('blood_pressure', 'N/A')}")
        lines.append(f"A: {a.get('primary_diagnosis', 'N/A')}")
        lines.append(f"P: {', '.join(p.get('medications', [])) if p.get('medications') else 'See plan'}")

        return "\n".join(lines)

    def _format_detailed_soap(self, s: Dict, o: Dict, a: Dict, p: Dict, metadata: Dict) -> str:
        """Format using detailed template (similar to default but more verbose)."""
        return self._format_default_soap(s, o, a, p, metadata)

    def generate_multiple_formats(self, soap_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate note in multiple formats.

        Args:
            soap_data: Complete SOAP data

        Returns:
            Dictionary with different format outputs
        """
        return {
            "default": self.compile_soap_note(soap_data, "default"),
            "concise": self.compile_soap_note(soap_data, "concise"),
            "detailed": self.compile_soap_note(soap_data, "detailed")
        }

    def export_to_json(self, soap_data: Dict[str, Any]) -> str:
        """Export SOAP data as JSON.

        Args:
            soap_data: Complete SOAP data

        Returns:
            JSON string
        """
        return json.dumps(soap_data, indent=2)

    def export_to_ehr_format(self, soap_data: Dict[str, Any], format_type: str = "fhir") -> str:
        """Export to EHR format (placeholder for FHIR/HL7).

        Args:
            soap_data: Complete SOAP data
            format_type: EHR format (fhir, hl7, ccd)

        Returns:
            Formatted EHR data
        """
        # Placeholder - would integrate with fhir.resources or python-hl7
        if format_type == "fhir":
            return json.dumps({
                "resourceType": "DocumentReference",
                "status": "current",
                "type": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "11506-3",
                        "display": "Progress note"
                    }]
                },
                "content": [{
                    "attachment": {
                        "contentType": "text/plain",
                        "data": self.compile_soap_note(soap_data)
                    }
                }]
            }, indent=2)
        else:
            return "EHR export format not implemented"


# Global instance
summary_agent = SummaryAgent()


def generate_final_note(soap_data: Dict[str, Any], template: str = "default") -> str:
    """Generate final formatted medical note.

    Args:
        soap_data: Complete SOAP data
        template: Template to use

    Returns:
        Formatted note
    """
    return summary_agent.compile_soap_note(soap_data, template)


def generate_all_formats(soap_data: Dict[str, Any]) -> Dict[str, str]:
    """Generate note in all available formats.

    Args:
        soap_data: Complete SOAP data

    Returns:
        Dictionary of all formats
    """
    return summary_agent.generate_multiple_formats(soap_data)
