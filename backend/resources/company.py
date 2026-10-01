from datetime import datetime ,date 
from flask import Blueprint, request, jsonify
from extensions import db , cache
from models import CompanyProfile , PlacementDrive, Application 
from utils import role_required , current_company
from resources.admin import clear_stats_cache

company_bp=Blueprint("company",__name__)

def _drive_cache_key(company_id):
    return f"company_drives_{company_id}"

#------------------------------------------------------------------------------------------
# Company Profile / Dashboard
#------------------------------------------------------------------------------------------
@company_bp.route("/profile", methods=["GET"])
@role_required("company")
def get_profile():
    company =current_company()
    return jsonify({"company":company.to_dict()})

@company_bp.route("/profile", methods=["POST"])
@role_required("company")
def update_profile():
    company = current_company()
    data = request.get_json() or {}
    for field in ("company_name" , "hr_name", "hr_contact", "website", "location" ,"description"):
        if field in data:
            setattr(company, field , data[field])
    db.session.commit()
    return jsonify({"message":"Profile updated successfully"})

@company_bp.route("/dashboard",methods=["GET"])
@role_required("company")
def dashboard():
    company = current_company()
    drives = company.drives
    total_applicants = sum(len(d.applications) for d in drives)
    selected = sum(1 for d in drives for a in d.applications if a.status == "selected")
    return jsonify({
        "company":company.to_dict(),
        "stats":{
            "total_drives":len(drives),
            "approved_drives":sum(1 for d in drives if d.status == "approved"),
            "pending_drives":sum(1 for d in drives if d.status == "pending"),
            "total_applicants":total_applicants,
            "selected":selected,
        }
    })
@company_bp.route("/drives" ,methods =["GET"])
@role_required("company")
def list_drives():
    company = current_company()
    drives = (
        PlacementDrive.query.filter_by(company_id = company.id)
        .order_by(PlacementDrive.created_at.desc())
        .all()
    )
    return jsonify({"drives":[d.to_dict() for d in drives]})

@company_bp.route("/drives",methods= ["POST"])
@role_required("company")
def create_drive():
    company = current_company()
    if company.approval_status != "approved":
        return jsonify(
            {"message":"company must be approved by the admin before creating drives"}
        ), 403
    data = request.get_json() or {}
    if not (data.get("job_title") or "").strip():
        return jsonify({"message":"job_title is required"}), 400
    deadline = None
    if data.get("application_deadline"):
        try:
            deadline = datetime.strptime(data["application_deadline"] , "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid deadline format (YYYY-MM-DD)"}), 400
    branches = data.get("eligible_branches")
    if isinstance(branches, list):
        branches = [branch.upper() for branch in branches]
        branches = ",".join(branches)
    drive = PlacementDrive(
        company_id = company.id,
        job_title = data["job_title"].strip(),
        job_description = data.get("job_description"),
        eligible_branches = branches,
        min_cgpa= float(data.get("min_cgpa") or 0),
        eligible_year = int(data["eligible_year"]) if data.get("eligible_year") else None,
        package = data.get("package"),
        location = data.get("location"),
        openings = int(data.get("openings")or 1),
        application_deadline = deadline,
        status = "pending"
    )
    db.session.add(drive)
    db.session.commit()
    clear_stats_cache()
    return jsonify({"message": "Drive created , awaiting admin approval", "drive":drive.to_dict()}), 201

@company_bp.route("/drive/<int:drive_id>",methods = ["PUT"])
@role_required("company")
def update_drive(drive_id):
    company = current_company()
    drive = PlacementDrive.query.filter_by(id = drive_id, company_id = company.id).first()
    if not drive:
        return jsonify({"message":"Drive not found"}), 404
    data = request.get_json() or {}

    for field in ("job_title", "job_description" , "package" ,"location"):
        if field in data:
            setattr(drive, field, data[field])

    if "eligible_branches" in data:
        b = data["eligible_branches"]
        drive.eligible_branches = ",".join(b) if isinstance(b, list) else b
    if "min_cgpa" in data:
        drive.min_cgpa = float(data["min_cgpa"] or 0)
    if "eligible_year" in data:
        drive.eligible_year = int(data["eligible_year"]) if data["eligible_year"] else None
    if "openings" in data:
        drive.openings = int(data["openings"] or 1)
    if data.get("application_deadline"):
        try:
            drive.application_deadline = datetime.strptime(
                data["application_deadline"], "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({"message":"Invalid deadline format (YYYY-MM-DD)"}), 400
    if data.get("status")=="closed":
        drive.status = "closed"
    db.session.commit()
    return jsonify({"message":"Drive updated successfully","drive":drive.to_dict()})

#---------------------------------------------------------------------------------------------------
# Applications for a drive
#---------------------------------------------------------------------------------------------------
@company_bp.route("/drives/<int:drive_id>/applications",methods=["GET"])
@role_required("company")
def drive_applications(drive_id):
    company = current_company()
    drive = PlacementDrive.query.filter_by(id = drive_id , company_id = company.id).first_or_404()
    apps = (
        Application.query.filter_by(drive_id = drive.id)
        .order_by(Application.application_date.desc())
        .all()
    )
    return jsonify({
        "drive":drive.to_dict(),
        "applications":[a.to_dict() for a in apps],

    })
@company_bp.route("/applications/<int:app_id>",methods = ["PATCH"])
@role_required("company")
def update_application(app_id):
    company = current_company()
    app = Application.query.get_or_404(app_id)
    if not app.drive or app.drive.company_id != company.id:
        return jsonify({"message":"not your applicant"}),403
    data = request.get_json() or {}
    status = data.get("status")
    if status and status not in ("applied" , "shortlisted" ,"selected" , "rejected"):
        return jsonify({"message":"Invalide status"}),400
    if status:
        app.status = status
    if "notes" in data:
        app.notes = data["notes"]
    if data.get("interview_datetime"):
        try:
            app.interview_datetime = datetime.fromisoformat(data["interview_datetime"])
        except ValueError:
            return jsonify({"message": "Invalid interview datetime (ISO format)"}), 400
    db.session.commit()
    clear_stats_cache()
    return jsonify({"message": "Application updated", "application": app.to_dict()})
