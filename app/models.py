from datetime import datetime
from app import db


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    intake = db.relationship("IntakeRecord", backref="patient", uselist=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class IntakeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    status = db.Column(db.String(50), default="pending")  # pending, in_progress, complete, flagged

    # Workflow steps
    personal_info_complete = db.Column(db.Boolean, default=False)
    insurance_verified = db.Column(db.Boolean, default=False)
    medical_history_complete = db.Column(db.Boolean, default=False)
    consent_forms_signed = db.Column(db.Boolean, default=False)
    id_verified = db.Column(db.Boolean, default=False)

    # Insurance info
    insurance_provider = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    insurance_group_number = db.Column(db.String(50))

    # Medical history
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    medical_conditions = db.Column(db.Text)

    # Metadata
    notes = db.Column(db.Text)
    flagged_reason = db.Column(db.String(200))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def completion_percentage(self):
        steps = [
            self.personal_info_complete,
            self.insurance_verified,
            self.medical_history_complete,
            self.consent_forms_signed,
            self.id_verified,
        ]
        return int((sum(steps) / len(steps)) * 100)

    @property
    def pending_steps(self):
        pending = []
        if not self.personal_info_complete:
            pending.append("Personal Information")
        if not self.insurance_verified:
            pending.append("Insurance Verification")
        if not self.medical_history_complete:
            pending.append("Medical History")
        if not self.consent_forms_signed:
            pending.append("Consent Forms")
        if not self.id_verified:
            pending.append("ID Verification")
        return pending
