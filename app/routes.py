from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Patient, IntakeRecord
from app.workflow import create_patient_intake, update_intake_step, flag_intake, get_dashboard_stats

main = Blueprint("main", __name__)


@main.route("/")
def dashboard():
    stats = get_dashboard_stats()
    recent_intakes = (
        IntakeRecord.query.order_by(IntakeRecord.updated_at.desc()).limit(10).all()
    )
    flagged = IntakeRecord.query.filter_by(status="flagged").all()
    return render_template(
        "dashboard.html", stats=stats, recent_intakes=recent_intakes, flagged=flagged
    )


@main.route("/intake/new", methods=["GET", "POST"])
def new_intake():
    if request.method == "POST":
        try:
            dob = datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d").date()
            patient_data = {
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "date_of_birth": dob,
                "email": request.form.get("email"),
                "phone": request.form.get("phone"),
                "address": request.form.get("address"),
                "emergency_contact_name": request.form.get("emergency_contact_name"),
                "emergency_contact_phone": request.form.get("emergency_contact_phone"),
            }
            patient, intake = create_patient_intake(patient_data)
            flash(f"Intake started for {patient.full_name}", "success")
            return redirect(url_for("main.patient_detail", patient_id=patient.id))
        except Exception as e:
            flash(f"Error creating intake: {str(e)}", "error")

    return render_template("intake_form.html")


@main.route("/patient/<int:patient_id>")
def patient_detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("patient_detail.html", patient=patient)


@main.route("/patient/<int:patient_id>/update", methods=["POST"])
def update_patient_intake(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    intake = patient.intake

    step = request.form.get("step")
    action = request.form.get("action")

    if action == "complete":
        extra_data = {}

        # Handle insurance data
        if step == "insurance_verified":
            extra_data = {
                "insurance_provider": request.form.get("insurance_provider"),
                "insurance_policy_number": request.form.get("insurance_policy_number"),
                "insurance_group_number": request.form.get("insurance_group_number"),
            }

        # Handle medical history
        if step == "medical_history_complete":
            extra_data = {
                "allergies": request.form.get("allergies"),
                "current_medications": request.form.get("current_medications"),
                "medical_conditions": request.form.get("medical_conditions"),
            }

        update_intake_step(intake.id, step, True, extra_data if extra_data else None)
        flash("Step completed", "success")

    elif action == "flag":
        reason = request.form.get("flag_reason", "Needs review")
        flag_intake(intake.id, reason)
        flash("Intake flagged for review", "warning")

    return redirect(url_for("main.patient_detail", patient_id=patient_id))


@main.route("/patients")
def patient_list():
    status_filter = request.args.get("status")
    query = IntakeRecord.query

    if status_filter:
        query = query.filter_by(status=status_filter)

    intakes = query.order_by(IntakeRecord.updated_at.desc()).all()
    return render_template("patient_list.html", intakes=intakes, current_filter=status_filter)


@main.route("/api/stats")
def api_stats():
    return jsonify(get_dashboard_stats())


@main.route("/demo/seed")
def seed_demo_data():
    """Seed database with demo data for showcase purposes."""
    from app.models import Patient, IntakeRecord

    # Clear existing data
    IntakeRecord.query.delete()
    Patient.query.delete()

    demo_patients = [
        {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "date_of_birth": datetime(1985, 3, 15).date(),
            "email": "sarah.j@email.com",
            "phone": "555-0101",
            "status": "complete",
            "steps": [True, True, True, True, True],
        },
        {
            "first_name": "Michael",
            "last_name": "Chen",
            "date_of_birth": datetime(1990, 7, 22).date(),
            "email": "m.chen@email.com",
            "phone": "555-0102",
            "status": "in_progress",
            "steps": [True, True, True, False, False],
        },
        {
            "first_name": "Emily",
            "last_name": "Rodriguez",
            "date_of_birth": datetime(1978, 11, 8).date(),
            "email": "emily.r@email.com",
            "phone": "555-0103",
            "status": "flagged",
            "steps": [True, False, False, False, False],
            "flag_reason": "Insurance verification failed - policy expired",
        },
        {
            "first_name": "James",
            "last_name": "Wilson",
            "date_of_birth": datetime(1995, 1, 30).date(),
            "email": "jwilson@email.com",
            "phone": "555-0104",
            "status": "pending",
            "steps": [True, False, False, False, False],
        },
        {
            "first_name": "Maria",
            "last_name": "Garcia",
            "date_of_birth": datetime(1982, 9, 12).date(),
            "email": "mgarcia@email.com",
            "phone": "555-0105",
            "status": "in_progress",
            "steps": [True, True, False, False, False],
        },
    ]

    for pdata in demo_patients:
        patient = Patient(
            first_name=pdata["first_name"],
            last_name=pdata["last_name"],
            date_of_birth=pdata["date_of_birth"],
            email=pdata["email"],
            phone=pdata["phone"],
        )
        db.session.add(patient)
        db.session.flush()

        intake = IntakeRecord(
            patient_id=patient.id,
            status=pdata["status"],
            personal_info_complete=pdata["steps"][0],
            insurance_verified=pdata["steps"][1],
            medical_history_complete=pdata["steps"][2],
            consent_forms_signed=pdata["steps"][3],
            id_verified=pdata["steps"][4],
            started_at=datetime.utcnow(),
            flagged_reason=pdata.get("flag_reason"),
        )
        if pdata["status"] == "complete":
            intake.completed_at = datetime.utcnow()
        db.session.add(intake)

    db.session.commit()
    flash("Demo data loaded successfully!", "success")
    return redirect(url_for("main.dashboard"))
