"""Helper utilities for the Smart Public Issue Detection System."""

import os
import uuid
from datetime import datetime
from io import BytesIO

from PIL import Image

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")


def validate_image(uploaded_file):
    """
    Validate uploaded image file.
    Returns (is_valid, error_message).
    """
    if uploaded_file is None:
        return False, "Please upload an image before continuing."

    filename = uploaded_file.name.lower()
    ext = os.path.splitext(filename)[1]
    if ext not in ALLOWED_EXTENSIONS:
        return False, "Invalid file type. Allowed: JPG, JPEG, PNG."

    file_bytes = uploaded_file.getvalue()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        return False, f"Image too large. Maximum size is {MAX_FILE_SIZE_MB} MB."

    try:
        Image.open(BytesIO(file_bytes)).verify()
    except Exception:
        return False, "Invalid image file. Please upload a valid JPG or PNG image."

    return True, ""


def save_uploaded_image(uploaded_file):
    """
    Save uploaded image with a unique filename.
    Returns the saved file path.
    """
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    ext = os.path.splitext(uploaded_file.name.lower())[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOADS_DIR, unique_name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    return file_path


def format_date(date_str):
    """Format ISO date string to DD-Mon-YYYY."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d-%b-%Y")
    except (ValueError, TypeError):
        return str(date_str)


def generate_complaint_id(complaint_id):
    """Format complaint ID for display."""
    return f"#{complaint_id}"


def get_severity_emoji(severity):
    """Return emoji indicator for severity level."""
    severity = (severity or "").strip().lower()
    if severity == "high":
        return "🔴 High"
    if severity == "medium":
        return "🟡 Medium"
    return "🟢 Low"


def get_status_emoji(status):
    """Return emoji indicator for complaint status."""
    status = (status or "").strip().lower()
    mapping = {
        "pending": "🟡 Pending",
        "under review": "🔵 Under Review",
        "in progress": "🟠 In Progress",
        "resolved": "🟢 Resolved",
    }
    return mapping.get(status, f"⚪ {status}")
