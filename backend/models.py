"""Database models for the Placement Portal Application.

A single unified ``User`` model differentiates all roles (admin / company /
student) and is linked one-to-one with a role-specific profile.
"""
from datetime import datetime, date

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


# ---------------------------------------------------------------------------
# Unified user model
# ---------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin | company | student
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship(
        "StudentProfile", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    company = db.relationship(
        "CompanyProfile", backref="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "is_blacklisted": self.is_blacklisted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# Student profile
# ---------------------------------------------------------------------------
class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    roll_number = db.Column(db.String(40))
    branch = db.Column(db.String(60))
    cgpa = db.Column(db.Float, default=0.0)
    graduation_year = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    resume_filename = db.Column(db.String(255))

    applications = db.relationship(
        "Application", backref="student", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.user.email if self.user else None,
            "name": self.name,
            "roll_number": self.roll_number,
            "branch": self.branch,
            "cgpa": self.cgpa,
            "graduation_year": self.graduation_year,
            "phone": self.phone,
            "bio": self.bio,
            "resume_filename": self.resume_filename,
            "is_active": self.user.is_active if self.user else True,
            "is_blacklisted": self.user.is_blacklisted if self.user else False,
        }


# ---------------------------------------------------------------------------
# Company profile
# ---------------------------------------------------------------------------
class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    company_name = db.Column(db.String(120), nullable=False)
    hr_name = db.Column(db.String(120))
    hr_contact = db.Column(db.String(40))
    website = db.Column(db.String(200))
    location = db.Column(db.String(120))
    description = db.Column(db.Text)
    approval_status = db.Column(db.String(20), default="pending")  # pending|approved|rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    drives = db.relationship(
        "PlacementDrive", backref="company", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.user.email if self.user else None,
            "company_name": self.company_name,
            "hr_name": self.hr_name,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "location": self.location,
            "description": self.description,
            "approval_status": self.approval_status,
            "is_active": self.user.is_active if self.user else True,
            "is_blacklisted": self.user.is_blacklisted if self.user else False,
            "drives_count": len(self.drives),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# Placement drive
# ---------------------------------------------------------------------------
class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer, db.ForeignKey("company_profiles.id"), nullable=False
    )
    job_title = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.Text)
    eligible_branches = db.Column(db.String(255))  # comma separated, empty = all
    min_cgpa = db.Column(db.Float, default=0.0)
    eligible_year = db.Column(db.Integer)  # graduation year, null = any
    package = db.Column(db.String(60))
    location = db.Column(db.String(120))
    openings = db.Column(db.Integer, default=1)
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default="pending")  # pending|approved|rejected|closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship(
        "Application", backref="drive", cascade="all, delete-orphan"
    )

    def eligible_branch_list(self):
        if not self.eligible_branches:
            return []
        return [b.strip() for b in self.eligible_branches.split(",") if b.strip()]

    def to_dict(self, include_company=True):
        data = {
            "id": self.id,
            "company_id": self.company_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "eligible_branches": self.eligible_branch_list(),
            "min_cgpa": self.min_cgpa,
            "eligible_year": self.eligible_year,
            "package": self.package,
            "location": self.location,
            "openings": self.openings,
            "application_deadline": self.application_deadline.isoformat()
            if self.application_deadline
            else None,
            "status": self.status,
            "applicants_count": len(self.applications),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_company and self.company:
            data["company_name"] = self.company.company_name
            data["company_website"] = self.company.website
        return data


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("student_profiles.id"), nullable=False
    )
    drive_id = db.Column(
        db.Integer, db.ForeignKey("placement_drives.id"), nullable=False
    )
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="applied")  # applied|shortlisted|selected|rejected
    interview_datetime = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )

    def to_dict(self):
        data = {
            "id": self.id,
            "student_id": self.student_id,
            "drive_id": self.drive_id,
            "application_date": self.application_date.isoformat()
            if self.application_date
            else None,
            "status": self.status,
            "interview_datetime": self.interview_datetime.isoformat()
            if self.interview_datetime
            else None,
            "notes": self.notes,
        }
        if self.drive:
            data["job_title"] = self.drive.job_title
            data["company_name"] = (
                self.drive.company.company_name if self.drive.company else None
            )
        if self.student:
            data["student_name"] = self.student.name
            data["student_branch"] = self.student.branch
            data["student_cgpa"] = self.student.cgpa
            data["student_email"] = self.student.user.email if self.student.user else None
        return data
