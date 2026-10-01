from flask import Blueprint , request , jsonify 
from flask_jwt_extended import create_access_token , jwt_required
from extensions import db
from models import User, StudentProfile, CompanyProfile
from utils import current_user

auth_bp = Blueprint("auth", __name__)

def _make_token(user):
    return create_access_token(identity=str(user.id) , additional_claims={"role" : user.role , "email" :user.email} )


@auth_bp.route('/register/student' , methods = ["POST"])
def register_student():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    name = (data.get("name") or "").strip()

    if not email or not password or not name :
        return jsonify({"message" : "email , password and name is required"}), 400
    if User.query.filter_by(email = email).first():
        return jsonify({
            "message" :"email already exists"
        }), 409
    user = User(email=email , role = "student")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    profile = StudentProfile(
        user_id = user.id,
        name = name,
        roll_number = data.get("roll_number"),
        cgpa = data.get("cgpa"),
        graduation_year =int(data["graduation_year"]) if data.get("graduation_year") else None,
        phone = data.get("phone"),
        branch=str(data["branch"]).upper()
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify({
        "message" : "Student registered successfully",
        "access_token": _make_token(user),
        "user" : user.to_dict()
    })


@auth_bp.route("/register/company" , methods = ["POST"])
def register_company():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    company_name = (data.get("company_name") or "").strip()
    if not email or not password or not company_name:
        return jsonify({"message" : "email , password , name is required"}), 400
    if User.query.filter_by(email = email).first():
        return jsonify({
            "message":"email already exists"
        }), 409
    user = User(email= email , role = "company")
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    profile = CompanyProfile(
        user_id = user.id,
        company_name = company_name,
        hr_name =data.get("hr_name"),
        hr_contact = data.get("hr_contact"),
        website = data.get("website"),
        location = data.get("location"),
        description = data.get("description"),
        approval_status = "pending"
    )

    db.session.add(profile)
    db.session.commit()
    return jsonify({
        "message":"Company registered Successfully",
        "access_token":_make_token(user),
        "user":user.to_dict()
    })

@auth_bp.route("/login" , methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = User.query.filter_by(email = email).first()
    if not user or not user.check_password(password):
        return jsonify({"message" : "invalid email or password"}), 401
    if not user.is_active:
        return jsonify({"message" : "user is temporarily not active"}), 403
    if user.is_blacklisted:
        return jsonify({"message" : "user is blacklisted"}), 403
    return jsonify({
        "message" : "Login successfully",
        "access_token" : _make_token(user),
        "user": user.to_dict()
    })

@auth_bp.route("/me" , methods= ["GET"])
@jwt_required()
def me():
    user = current_user()
    if not user:
        return jsonify({"message" : "User not found"}),404
    data = user.to_dict()
    if user.role == "student" and user.student:
        data["profile"] = user.student.to_dict()
    elif user.role == "company" and user.company :
        data["profile"] = user.company.to_dict()
    return jsonify({
        "user":data
    })
    