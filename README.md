# Patient Intake Automation System

A healthcare workflow automation tool that streamlines the patient intake process. Built to demonstrate practical problem-solving in healthcare operations.

## The Problem

Patient intake in healthcare facilities is often a fragmented, paper-heavy process:
- Patients fill out redundant forms
- Staff manually track which steps are complete
- Insurance verification happens ad-hoc
- No visibility into bottlenecks or delays

## The Solution

This system digitizes and automates the entire intake workflow:

- **Centralized Dashboard** - Real-time visibility into all patient intakes
- **Workflow Tracking** - 5-step intake process with progress indicators
- **Flagging System** - Identify and surface issues (e.g., insurance problems)
- **Status Filtering** - Quickly find pending, in-progress, or flagged intakes

## Features

### Dashboard
- At-a-glance stats: total, pending, in-progress, complete, flagged
- Flagged items surfaced for immediate attention
- Recent activity feed

### Intake Workflow
1. **Personal Information** - Patient demographics and contact
2. **Insurance Verification** - Provider, policy, and group numbers
3. **Medical History** - Allergies, medications, conditions
4. **Consent Forms** - Track signed documents
5. **ID Verification** - Confirm patient identity

### Patient Management
- Filter by status
- Progress tracking per patient
- Complete audit trail

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite (easily swappable)
- **Frontend**: Server-rendered templates, vanilla CSS

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py

# Open in browser
open http://localhost:5100

# Load demo data (optional)
# Click "Load Demo Data" on the dashboard
```

## Project Structure

```
patient-intake-automation/
├── app/
│   ├── __init__.py      # App factory
│   ├── models.py        # Patient & IntakeRecord models
│   ├── routes.py        # All endpoints
│   ├── workflow.py      # Business logic
│   └── templates/       # Jinja2 templates
├── static/
│   └── style.css        # Styling
├── config.py            # Configuration
├── run.py               # Entry point
└── requirements.txt     # Dependencies
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard |
| `/intake/new` | GET/POST | New patient intake form |
| `/patient/<id>` | GET | Patient detail & workflow |
| `/patient/<id>/update` | POST | Update intake step |
| `/patients` | GET | All patients (filterable) |
| `/api/stats` | GET | JSON stats for dashboard |
| `/demo/seed` | GET | Load demo data |

## Screenshots

The system provides a clean, professional interface:
- Dashboard with stats cards and recent activity
- Step-by-step workflow with visual progress
- Flag system for issues requiring attention

## Future Enhancements

- Email/SMS notifications for patients
- Integration with EHR systems
- Appointment scheduling integration
- Document upload for insurance cards/IDs
- Multi-location support

---

*Built as a portfolio project demonstrating healthcare domain knowledge and workflow automation skills.*
