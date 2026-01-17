from datetime import datetime
from app import db
from app.models import Patient, IntakeRecord


def create_patient_intake(patient_data):
    """Create a new patient and their intake record."""
    patient = Patient(
        first_name=patient_data["first_name"],
        last_name=patient_data["last_name"],
        date_of_birth=patient_data["date_of_birth"],
        email=patient_data.get("email"),
        phone=patient_data.get("phone"),
        address=patient_data.get("address"),
        emergency_contact_name=patient_data.get("emergency_contact_name"),
        emergency_contact_phone=patient_data.get("emergency_contact_phone"),
    )
    db.session.add(patient)
    db.session.flush()

    intake = IntakeRecord(
        patient_id=patient.id,
        status="pending",
        personal_info_complete=True,  # Just completed by filling form
        started_at=datetime.utcnow(),
    )
    db.session.add(intake)
    db.session.commit()

    return patient, intake


def update_intake_step(intake_id, step_name, value, extra_data=None):
    """Update a specific step in the intake workflow."""
    intake = IntakeRecord.query.get(intake_id)
    if not intake:
        return None

    setattr(intake, step_name, value)

    if extra_data:
        for key, val in extra_data.items():
            if hasattr(intake, key):
                setattr(intake, key, val)

    # Update status based on completion
    if intake.status == "pending" and intake.completion_percentage > 0:
        intake.status = "in_progress"

    if intake.completion_percentage == 100:
        intake.status = "complete"
        intake.completed_at = datetime.utcnow()

    db.session.commit()
    return intake


def flag_intake(intake_id, reason):
    """Flag an intake for review."""
    intake = IntakeRecord.query.get(intake_id)
    if intake:
        intake.status = "flagged"
        intake.flagged_reason = reason
        db.session.commit()
    return intake


def get_dashboard_stats():
    """Get statistics for the dashboard."""
    total = IntakeRecord.query.count()
    pending = IntakeRecord.query.filter_by(status="pending").count()
    in_progress = IntakeRecord.query.filter_by(status="in_progress").count()
    complete = IntakeRecord.query.filter_by(status="complete").count()
    flagged = IntakeRecord.query.filter_by(status="flagged").count()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "complete": complete,
        "flagged": flagged,
    }
