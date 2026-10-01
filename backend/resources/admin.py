from flask import jsonify , request , Blueprint
from extensions import db ,cache
from models import User , StudentProfile , CompanyProfile , PlacementDrive , Application 
from utils import role_required

admin_bp = Blueprint("admin",__name__)

STATS_CACHE_KEY = "admin_dashboard_stats"

def clear_stats_cache():
    cache.delete(STATS_CACHE_KEY)

#----------------------------------------------------------------------------
#Dashboard (with cached)
#----------------------------------------------------------------------------

@admin_bp.route("/dashboard" , methods = ["GET"])
@role_required("admin")
def dashboard():
    stats = cache.get(STATS_CACHE_KEY)
    cached = stats is not None
    if stats is None:
        stats ={
            "total_student":StudentProfile.query.count(),
            "total_company":CompanyProfile.query.count(),
            "approved_company" : CompanyProfile.query.filter_by(approval_status = "approved").count(),
            "pending_company" : CompanyProfile.query.filter_by(approval_status = "pending").count(),
            "total_drives" : PlacementDrive.query.count(),
            "approved_drive": PlacementDrive.query.filter_by(status = "approved").count(),
            "pending_drives": PlacementDrive.query.filter_by(status = "pending").count(),
            "total_application":Application.query.count(),
            "total_selected":Application.query.filter_by(status = "selected").count()
        }
        cache.set(STATS_CACHE_KEY , stats , timeout = 60)
    return jsonify({"stats" :stats , "cached" :cached})

#---------------------------------------------------------------------------------------------------------------------------
# Companies
#---------------------------------------------------------------------------------------------------------------------------

@admin_bp.route("/companies" ,methods = ["GET"])
@role_required("admin")
def list_companies():
    q= (request.args.get("q") or "").strip()
    status = request.args.get("status")
    query = CompanyProfile.query
    if q:
        query = query.filter(CompanyProfile.company_name.ilike(f"%{q}%"))
    if status:
        query = query.filter_by(approval_status = status)
    companies = query.order_by(CompanyProfile.created_at.desc()).all()
    return jsonify({"companies":[c.to_dict() for c in companies]})

@admin_bp.route("/companies/<int:company_id>/approval" ,methods=["PATCH"])
@role_required("admin")
def set_company_approval(company_id):
    company = CompanyProfile.query.get_or_404(company_id)
    decision = (request.get_json() or {}).get("decision")
    if decision not in ("approved" , "rejected" , "pending"):
        return jsonify({"message" : "Decision must be approved/ reject/ pending"}), 400
    company.approval_status = decision
    db.session.commit()
    clear_stats_cache()
    return jsonify({"message":f"company {decision}" , "company":company.to_dict()})

#--------------------------------------------------------------------------------------------------------------
# Student
#--------------------------------------------------------------------------------------------------------------

@admin_bp.route("/students" , methods = ["GET"])
@role_required("admin")
def list_student():
    q= (request.args.get("q") or "").strip()
    query= StudentProfile.query
    if q:
        query = query.filter(db.or_(
            StudentProfile.name.ilike(f"%{q}%"),
            StudentProfile.roll_number.ilike(f"%{q}%"),
            StudentProfile.branch.ilike(f"%{q}%"))
            )
        
    students = query.order_by(StudentProfile.id.desc()).all()
    return jsonify({"students":[s.to_dict() for s in students]})

#------------------------------------------------------------------------------------------
# Blacklist / deactivate (works for both students and companies)
#------------------------------------------------------------------------------------------
@admin_bp.route("/users/<int:user_id>/status" , methods = ["PATCH"])
@role_required("admin")
def set_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == "admin":
        return jsonify({"message" : "can not modify an admin"}), 400
    data = request.get_json() or {}
    if "is_active" in data:
        user.is_active = bool(data["is_active"])
    if "is_blacklisted" in data :
        user.is_blacklisted = bool(data["is_blacklisted"])
    db.session.commit()
    clear_stats_cache()
    return jsonify({"message" :"user status updated", "user":user.to_dict()})

#---------------------------------------------------------------------------------------------------
# Drives
#---------------------------------------------------------------------------------------------------
@admin_bp.route("/drives" ,methods = ["GET"])
@role_required("admin")
def list_drive():
    status = request.args.get("status")
    q = (request.args.get("q") or "").strip()
    query = PlacementDrive.query
    if status:
        query = query.filter_by(status= status)
    if q:
        query = query.filter(PlacementDrive.job_title.ilike(f"%{q}%"))
    drives = query.order_by(PlacementDrive.created_at.desc()).all()
    return jsonify({"drives":[d.to_dict() for d in drives]})

@admin_bp.route("/drives/<int:drive_id>/approval" , methods = ["PATCH"])
@role_required("admin")
def set_drive_approval(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    decision = (request.get_json() or {}).get("decision")
    if decision not in ("approved" , "rejected" , "pending"):
        return jsonify({"message" : "Invalid decision"}), 400
    drive.status = decision
    db.session.commit()
    clear_stats_cache()
    return jsonify({"message":f"Drive {decision}" , "drive":drive.to_dict()})

#----------------------------------------------------------------------------------------------------------------
# All applications (oversight)
#----------------------------------------------------------------------------------------------------------------
@admin_bp.route("/applications", methods = ["GET"])
@role_required("admin")
def list_applications():
    applications = Application.query.order_by(Application.application_date.desc()).all()
    return jsonify({"application" : [a.to_dict() for a in applications]})

#------------------------------------------------------------------------------------------------------------------
# Reports / placement statics
#------------------------------------------------------------------------------------------------------------------
@admin_bp.route("/reports" ,methods = ["GET"])
@role_required("admin")
def reports():
    drives = PlacementDrive.query.all()
    apps = Application.query.all()
    status_count = {"applied" : 0 , "shortlisted":0 , "selected" : 0 , "rejected":0}
    for a in apps:
        status_count[a.status] = status_count.get(a.status,0)+1

    branch_selecte={}
    for a in apps:
        if a.status == "selected" and a.student:
            branch = a.student.branch or "unknown"
            branch_selecte[branch]= branch_selecte.get(branch , 0)+1
    top_drives = sorted(drives , key=lambda d: len(d.applications), reverse=True)[:5]
    return jsonify({
        "status_counts":status_count,
        "branch_selected" : branch_selecte,
        "top_drives":[
            {"job_title":d.job_title,
             "company":d.company.company_name if d.company else "",
             "applicants":len(d.applications)} for d in top_drives
        ],
        "total":{
            "drives":len(drives),
            "applications":len(apps),
            "selected":status_count.get("selected" , 0),
        }
    })
