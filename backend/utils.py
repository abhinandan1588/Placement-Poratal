from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request , get_jwt , get_jwt_identity

from models import User , StudentProfile , CompanyProfile 

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args , **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            id = get_jwt_identity()
            user = User.query.get(int(id)) if id else None
            if user is None:
                return jsonify({"message" : "user not found "}) , 404
            if not user.is_active :
                return jsonify({"message" : "user is not activated"}), 403
            if user.is_blacklisted:
                return jsonify({"message" : "user is blacklisted"}), 403
            if roles and user.role not in roles:
                return jsonify({"message" : "forbidden : insufficient role"}), 403
            return fn(*args , **kwargs)
        return decorator
    return wrapper

def current_user():
    uid = get_jwt_identity()
    return User.query.get(int(uid)) if uid else None

def current_student():
    user = current_user()
    return user.student if user else None

def current_company():
    user = current_user()
    return user.company if user else None

def is_eligibel(student:StudentProfile , drive):
    branches = drive.eligible_branch_list()
    if branches and student.branch not in branches:
        return False , "Your branche is not eligible for this drive"
    if drive.min_cgpa and (student.cgpa or 0) < drive.min_cgpa:
        return False , f"minimum {drive.min_cgpa} is required"
    if drive.eligible_year and (student.graduation_year or 0) < drive.eligible_year:
        return False , "you have not completed your graduation"
    return True , "Eligible"