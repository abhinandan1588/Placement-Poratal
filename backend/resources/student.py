import os
from datetime import date 
from flask import request ,jsonify , Blueprint , send_from_directory
from werkzeug.utils import secure_filename

from extensions import db
from config import Config
from models import StudentProfile ,PlacementDrive , Application
from utils import role_required , current_student , is_eligibel
from resources.admin import clear_stats_cache
import tasks

student_bp = Blueprint("student",__name__)
ALLOWED_RESUME_EXT = {".pdf" , ".doc",".docx"}

#------------------------------------------------------------------------------------------------
# Student Profile
#------------------------------------------------------------------------------------------------
@student_bp.route("/profile", methods = ["GET"])
@role_required("student")
def get_profile():
    student = current_student()
    return jsonify({"student":student.to_dict()})

@student_bp.route("/profile" , methods = ["PUT"])
@role_required("student")
def update_profile():
    student = current_student()
    data = request.get_json()  or {}
    for field in ("name" ,"roll_number" , "phone" , "bio"):
        if field in data:
            setattr(student ,field , data[field])
    if "cgpa" in data:
        student.cgpa = float(data["cgpa"] or 6)
    if "branch" in data:
        student.branch = str(data["branch"]).upper()
    if "graduation_year" in data:
        student.graduation_year = int(data["graduation_year"])
    db.session.commit()
    return jsonify({"message":"profile updated" , "student":student.to_dict()})

@student_bp.route("/resume" , methods = ["POST"])
@role_required("student")
def upload_resume():
    student = current_student()
    if "resume" not in request.files:
        return jsonify({"message" :"No file uploaded"}) ,400
    file = request.files["resume"]
    if not file.filename:
        return jsonify({"message":"no file selected"}), 400
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_RESUME_EXT:
        return jsonify({"message" :"only pdf / doc / docx allowed"}), 400
    filename = secure_filename(f"resume_student_{student.id}{ext}")
    file.save(os.path.join(Config.Upload , filename))
    student.resume_filename = filename
    db.session.commit()
    return jsonify({"message":"Resume uploded" , "resume_filename":filename})

@student_bp.route("/resume" , methods = ["GET"])
@role_required("student")
def download_resume():
    student = current_student()
    if not student.resume_filename:
        return jsonify({"message":"No resume uploaded"}), 404
    return send_from_directory(Config.Upload , student.resume_filename , as_attachment = True)

@student_bp.route("/drives" , methods=["GET"])
@role_required("student")
def list_drive():
    student = current_student()
    q= (request.args.get("q") or "").strip()
    only_eligibel = request.args.get("eligible") == "true"
    query = PlacementDrive.query.filter_by(status="approved")
    if q :
        query = query.filter(PlacementDrive.job_title.ilike(f"%{q}%"))
    drives = query.order_by(PlacementDrive.created_at.desc()).all()
    applied_ids = {a.drive_id for a in student.applications}
    result = []
    for d in drives:
        eligible , reason = is_eligibel(student ,d)
        if only_eligibel and not eligible:
            continue
        item = d.to_dict()
        item["eligible"] = eligible
        item["eligibility_reason"] = reason
        item["already_applied"] = d.id in applied_ids
        item["deadline_passed"] = bool(d.application_deadline and d.application_deadline < date.today())
        result.append(item)
    return jsonify({"drives":result})

#----------------------------------------------------------------------------------------------------------------------------------
# Apply
#----------------------------------------------------------------------------------------------------------------------------------
@student_bp.route("/drives/<int:drive_id>/apply" ,methods = ["POST"])
@role_required("student")
def apply(drive_id):
    student = current_student()
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.status != "approved":
        return jsonify({"message":"this drive is not approved"}) ,400
    if drive.application_deadline and drive.application_deadline < date.today():
        return jsonify({"message":"Application deadline passed"}), 400
    existing = Application.query.filter_by(student_id = student.id ,drive_id=drive.id).first()
    if existing:
        return jsonify({"message":"You have already applied to this drive"}), 409
    eligibel ,reason = is_eligibel(student , drive)
    if not eligibel:
        return jsonify({"message":f"Not eligible : {reason}"}),403
    application =Application(student_id = student.id,drive_id=drive.id)
    db.session.add(application)
    db.session.commit()
    clear_stats_cache()
    return jsonify({"message":"Applied successfully" , "application":application.to_dict()})

#----------------------------------------------------------------------------------------------------------
# My applications / placement history
#----------------------------------------------------------------------------------------------------------
@student_bp.route("/applications", methods=["GET"])
@role_required("student")
def my_applications():
    student = current_student()
    apps =(
        Application.query.filter_by(student_id = student.id)
        .order_by(Application.application_date.desc())
        .all()
    )
    return jsonify({"applications":[a.to_dict() for a in apps ]})

#-----------------------------------------------------------------------------------------------------------------
# Async CSV export (Celery)
#-----------------------------------------------------------------------------------------------------------------
@student_bp.route("/export", methods = ["POST"])
@role_required("student")
def export_applications():
    student = current_student()
    async_result = tasks.export_applications_csv.delay(student.id)
    return jsonify({
        "message":"Export started . You will be notified when it is ready",
        "task_id":async_result.id
    })
@student_bp.route("/export/<task_id>",methods=["GET"])
@role_required("student")
def export_status(task_id):
    result = tasks.export_applications_csv.AsyncResult(task_id)
    payload = {"task_id":task_id , "state":result.state}
    if result.successful():
        payload["result"]= result.result
    return jsonify(payload)

@student_bp.route("/export/download/<path:filename>" , methods=["GET"])
@role_required("student")
def download_export(filename):
    safe = secure_filename(filename)
    if not os.path.exists(os.path.join(Config.Export,safe)):
        return jsonify({"message":"File not found"}) ,404
    return send_from_directory(Config.Export,safe ,as_attachment = True)
