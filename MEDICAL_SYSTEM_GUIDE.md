# Medical Note-Taking Multi-Agent System

## 🏥 Overview

A sophisticated multi-agent system for generating medical documentation from patient conversations. The system uses specialized AI agents to extract, structure, and format clinical information into professional SOAP notes with human review at each step.

## 🎯 Key Features

### ✅ Multi-Agent Architecture
- **7 Specialized Agents** working together
- **SOAP-based workflow** (Subjective → Objective → Assessment → Plan)
- **Human-in-the-loop** review at each stage
- **Template-driven** output formatting

### ✅ Input Flexibility
- Text conversations
- Audio transcripts
- Structured clinical data
- Multiple language support (future)

### ✅ Output Formats
- Standard SOAP notes
- Concise summaries
- Detailed reports
- EHR export (FHIR, HL7) - planned
- Custom templates

### ✅ Compliance & Quality
- Medical terminology extraction
- ICD-10 code suggestions
- Structured data capture
- Audit trail of all changes

## 🏗️ System Architecture

```
Patient Conversation
         ↓
   InputProcessor
         ↓
    PlannerAgent (Orchestrator)
         ↓
┌────────────────────────────────┐
│  SOAP Workflow                  │
│                                │
│  1. SubjectiveAgent            │
│     ↓ [Human Review]           │
│  2. ObjectiveAgent             │
│     ↓ [Human Review]           │
│  3. AssessmentAgent            │
│     ↓ [Human Review]           │
│  4. PlanAgent                  │
│     ↓ [Human Review]           │
└────────────────────────────────┘
         ↓
   SummaryAgent
         ↓
   Final SOAP Note(s)
```

## 🤖 Agent Descriptions

### 1. TemplateAgent (Existing)
- Manages templates for output formatting
- Upload custom templates
- Supports medical-specific templates (SOAP, H&P, Progress Notes)

### 2. SOAP Agent (4 Sub-Agents)

#### SubjectiveAgent
**Purpose**: Extract patient-reported information

**Extracts**:
- Chief Complaint
- History of Present Illness (HPI)
- Review of Systems (ROS)
- Past Medical History (PMH)
- Medications
- Allergies
- Social/Family History

**Output**: Structured subjective data dictionary

#### ObjectiveAgent
**Purpose**: Extract clinical findings

**Extracts**:
- Vital Signs (BP, HR, RR, Temp, SpO2)
- Physical Examination findings
- Laboratory results
- Imaging results

**Output**: Structured objective data dictionary

#### AssessmentAgent
**Purpose**: Generate clinical assessment

**Generates**:
- Primary Diagnosis
- Differential Diagnoses
- ICD-10 Codes
- Clinical Impression
- Problem List

**Output**: Structured assessment data

#### PlanAgent
**Purpose**: Create treatment plan

**Generates**:
- Medications/Prescriptions
- Diagnostic Tests
- Procedures
- Referrals
- Patient Education
- Follow-up Instructions
- Disposition

**Output**: Structured plan data

### 3. PlannerAgent
**Purpose**: Orchestrate the entire workflow

**Functions**:
- Initialize workflow with metadata
- Manage stage progression (S→O→A→P)
- Validate dependencies
- Track completion status
- Handle errors and retries

**Key Methods**:
- `start_workflow()` - Initialize new note
- `advance_stage()` - Move to next stage
- `get_workflow_status()` - Check progress

### 4. HumanReflectorAgent
**Purpose**: Interactive review and feedback

**Functions**:
- Present sections for human review
- Collect feedback and corrections
- Apply edits to structured data
- Track revision history

**Review Actions**:
- **[A] Approve** - Accept and continue
- **[E] Edit** - Make specific changes
- **[R] Regenerate** - Request AI to redo
- **[N] Add Note** - Add comments

**Key Methods**:
- `interactive_review()` - CLI review interface
- `collect_feedback()` - Record human input
- `apply_edits()` - Merge edits into data

### 5. SummaryAgent
**Purpose**: Final formatting and export

**Functions**:
- Compile complete SOAP note
- Apply templates
- Generate multiple formats
- Add metadata
- Export to EHR formats

**Templates**:
- Default - Full SOAP format
- Concise - Brief summary
- Detailed - Extended documentation

**Export Formats**:
- Plain text
- JSON
- FHIR (planned)
- HL7 (planned)
- CCD XML (planned)

### 6. MedicalTerminologyAgent (Future)
**Purpose**: Medical NLP and coding

**Will Extract**:
- Diagnoses → ICD-10 codes
- Medications → RxNorm codes
- Procedures → CPT codes
- Anatomical terms → SNOMED codes

**Technologies**:
- spaCy + scispaCy
- MedCAT
- Clinical BERT

### 7. InputProcessorAgent (Future)
**Purpose**: Handle multiple input types

**Will Support**:
- Text conversations
- Audio transcripts (via Whisper)
- Structured JSON/XML
- Multi-language (translation)

## 🚀 Quick Start

### Installation

```bash
# Already have the base system
cd /Users/chuhuiliu/PycharmProjects/LLM-Agent-System

# No additional dependencies needed for basic version
# Optional for advanced features:
# pip install spacy scispacy medcat fhir.resources python-hl7
```

### Run the System

```bash
python medical_note_system.py
```

### Choose a Mode

1. **Interactive Mode** - Full human review
2. **Demo Mode** - See example with sample data
3. **Batch Mode** - Process without review (future)

## 📝 Usage Examples

### Example 1: Interactive Note Creation

```bash
$ python medical_note_system.py

Select Mode:
[1] Interactive
[2] Demo
[3] Batch
[4] Exit

Your choice: 1

Enter patient conversation/transcript (type 'END' when done):
─────────────────────────────────────────────────
Patient: I have a headache that started 3 days ago.
Doctor: Is it constant or intermittent?
Patient: It comes and goes, mostly in the morning.
Doctor: Any vision changes?
Patient: No.
Doctor: Taking any medications?
Patient: Just ibuprofen for the pain.
END
─────────────────────────────────────────────────

[System extracts Subjective data]

═══ SUBJECTIVE ═══

Chief Complaint: Headache x 3 days

History of Present Illness:
Patient reports headache started 3 days ago. Pain is intermittent,
predominantly in morning hours. Denies vision changes. Currently
treating with ibuprofen.

Medications:
  • Ibuprofen PRN

───────────────────────────────────────────────────
Actions:
[A] Approve
[E] Edit
[R] Regenerate
[N] Add Note

Your choice: A

[Proceeds to Objective section...]
```

### Example 2: Demo Mode

```bash
$ python medical_note_system.py

Your choice: 2

DEMO: Creating Medical Note from Sample Conversation
═══════════════════════════════════════════════════

[Processes sample conversation automatically]

FINAL MEDICAL NOTE
═══════════════════════════════════════════════════

MEDICAL NOTE - SOAP FORMAT
Date: 2025-01-15
Provider: Dr. Smith
Patient ID: 12345

SUBJECTIVE:
Chief Complaint: Chest pain x 2 days
...

[Complete SOAP note generated]
```

## 📋 Workflow Steps

### Step-by-Step Process

1. **Input**: Enter patient conversation
2. **Metadata**: Provide date, provider, patient ID
3. **Subjective Review**: Review/edit patient complaints
4. **Objective Review**: Review/edit clinical findings
5. **Assessment Review**: Review/edit diagnosis
6. **Plan Review**: Review/edit treatment plan
7. **Generate**: Create final formatted note
8. **Save**: Export to file or EHR

### Review Actions at Each Step

```
[A] Approve
    → Accept section as-is
    → Proceed to next stage

[E] Edit
    → Make specific field changes
    → Format: field_name=new_value
    → Updates structured data

[R] Regenerate
    → Provide feedback
    → AI generates new version

[N] Add Note
    → Add comments/instructions
    → Saved in audit trail
```

## 🎨 Customization

### Adding Custom Templates

Use the existing TemplateAgent:

```bash
python create_template.py

# Upload SOAP template
Template name: soap_cardiology
Description: Cardiology-specific SOAP format
[Paste template with placeholders]
```

### Template Placeholders

Medical templates can use:
- `{chief_complaint}`
- `{history_present_illness}`
- `{medications}`
- `{blood_pressure}`
- `{heart_rate}`
- `{primary_diagnosis}`
- `{icd_codes}`
- `{plan_medications}`
- And more...

## 🔧 System Files

```
medical_agents/
├── __init__.py
├── soap_agent.py              # 4 SOAP sub-agents
├── planner_agent.py           # Workflow orchestration
├── human_reflector_agent.py   # Interactive review
├── summary_agent.py           # Final formatting
└── templates/
    └── soap_default.txt       # Default SOAP template

medical_note_system.py         # Main entry point
MEDICAL_SYSTEM_GUIDE.md        # This file
```

## 📊 Data Flow

### Subjective Data Structure
```python
{
    "chief_complaint": "Headache x 3 days",
    "history_present_illness": "...",
    "review_of_systems": {},
    "past_medical_history": [],
    "medications": ["Ibuprofen PRN"],
    "allergies": ["Penicillin - rash"],
    "social_history": {},
    "family_history": []
}
```

### Objective Data Structure
```python
{
    "vital_signs": {
        "blood_pressure": "120/80",
        "heart_rate": "72",
        "temperature": "98.6F",
        ...
    },
    "physical_exam": {
        "general": "Well-appearing",
        "heent": "Normocephalic...",
        ...
    },
    "laboratory_results": {},
    "imaging_results": {}
}
```

## 🎯 Use Cases

### Primary Care
- Office visit notes
- Annual physicals
- Acute care visits

### Specialists
- Consultation notes
- Procedure notes
- Follow-up visits

### Hospital
- Admission H&P
- Progress notes
- Discharge summaries

### Telemedicine
- Virtual visit documentation
- Remote patient monitoring

## ⚠️ Current Limitations

### Phase 1 (Current)
- ✅ Basic SOAP structure extraction
- ✅ Interactive human review
- ✅ Template-based output
- ❌ No medical NLP (terminology extraction)
- ❌ No ICD/CPT coding
- ❌ No EHR integration
- ❌ No audio transcription

### Future Enhancements
- Medical terminology extraction with scispaCy
- Automatic ICD-10/CPT code suggestions
- FHIR/HL7 export
- Audio transcription integration
- Multi-language support
- Batch processing
- API endpoints for EHR integration

## 🔐 Privacy & Compliance

### Important Notes
⚠️ **HIPAA Compliance**: This is a demonstration system. For production use:
- Implement proper PHI encryption
- Add access controls and audit logging
- Use secure data storage
- Ensure BAA agreements with service providers

⚠️ **Clinical Use**: This system assists with documentation but does not replace clinical judgment. Always review and validate generated notes.

## 🛠️ Development Roadmap

### Phase 1: Core System ✅ (Complete)
- SOAP agent structure
- Human review workflow
- Basic templates
- Interactive CLI

### Phase 2: Medical NLP (Next)
- spaCy + scispaCy integration
- Medical entity extraction
- ICD-10 code suggestions
- CPT code mapping

### Phase 3: Advanced Features
- Audio transcription (Whisper)
- Multi-language support
- Batch processing
- API development

### Phase 4: EHR Integration
- FHIR export
- HL7 messaging
- Direct EHR connectors
- CCD/CCDA support

## 📚 Additional Resources

### Documentation
- `TEMPLATE_AGENT_GUIDE.md` - Template system
- `AGENT_LINKING_GUIDE.md` - Agent integration patterns
- `TROUBLESHOOTING.md` - Common issues

### Medical Standards
- ICD-10: Diagnosis codes
- CPT: Procedure codes
- SNOMED CT: Clinical terminology
- LOINC: Lab/clinical observations
- RxNorm: Medication codes

## 🤝 Contributing

Ideas for extension:
1. Add specialty-specific templates
2. Integrate medical knowledge bases
3. Build web UI
4. Add voice input
5. Create mobile app
6. Implement smart suggestions

## 📞 Support

For issues or questions:
1. Check TROUBLESHOOTING.md
2. Review example conversations
3. Test with demo mode first

---

**System Status**: Phase 1 Complete ✅

**Ready to create your first medical note?**

```bash
python medical_note_system.py
```

🏥 Happy documenting!
