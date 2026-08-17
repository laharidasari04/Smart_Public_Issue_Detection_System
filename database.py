"""SQLite database operations for complaint management."""

import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "complaints.db")

VALID_STATUSES = ["Pending", "Under Review", "In Progress", "Resolved"]

CATEGORIES = [
    "Pothole",
    "Garbage",
    "Drainage",
    "Water Leakage",
    "Broken Street Light",
    "Damaged Road",
    "Open Manhole",
    "Fallen Tree",
    "Other",
]


def get_connection():
    """Create and return a database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the complaints table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citizen_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            additional_description TEXT,
            image_path TEXT NOT NULL,
            ai_category TEXT NOT NULL,
            ai_description TEXT NOT NULL,
            severity TEXT NOT NULL,
            suggested_action TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_complaint(data):
    """Insert a new complaint and return the new complaint ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO complaints (
            citizen_name, phone, location, additional_description,
            image_path, ai_category, ai_description, severity,
            suggested_action, status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["citizen_name"],
            data["phone"],
            data["location"],
            data.get("additional_description", ""),
            data["image_path"],
            data["ai_category"],
            data["ai_description"],
            data["severity"],
            data["suggested_action"],
            data.get("status", "Pending"),
            data.get("created_at", datetime.now().isoformat()),
        ),
    )
    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return complaint_id


def get_all_complaints():
    """Return all complaints ordered by newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_complaint_by_id(complaint_id):
    """Return a single complaint by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_complaints_by_phone(phone):
    """Return complaints matching a phone number."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM complaints WHERE phone = ? ORDER BY id DESC",
        (phone.strip(),),
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def update_status(complaint_id, status):
    """Update complaint status."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (status, complaint_id),
    )
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_complaint(complaint_id):
    """Delete a complaint by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT image_path FROM complaints WHERE id = ?", (complaint_id,))
    row = cursor.fetchone()

    cursor.execute("DELETE FROM complaints WHERE id = ?", (complaint_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if deleted and row and row["image_path"]:
        image_path = row["image_path"]
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass

    return deleted


def get_statistics():
    """Return complaint statistics for the admin dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM complaints")
    total = cursor.fetchone()["total"]

    stats = {"total": total}
    for status in VALID_STATUSES:
        cursor.execute(
            "SELECT COUNT(*) AS count FROM complaints WHERE status = ?",
            (status,),
        )
        stats[status.lower().replace(" ", "_")] = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT ai_category, COUNT(*) AS count
        FROM complaints
        GROUP BY ai_category
        ORDER BY count DESC
        """
    )
    stats["by_category"] = [
        {"category": row["ai_category"], "count": row["count"]}
        for row in cursor.fetchall()
    ]

    cursor.execute(
        """
        SELECT status, COUNT(*) AS count
        FROM complaints
        GROUP BY status
        """
    )
    stats["by_status"] = [
        {"status": row["status"], "count": row["count"]}
        for row in cursor.fetchall()
    ]

    conn.close()
    return stats


def insert_sample_data():
    """Insert sample complaints for demonstration."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS count FROM complaints")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return 0

    samples = [
        {
            "citizen_name": "Ravi Kumar",
            "phone": "9876543210",
            "location": "Main Road, Amalapuram, Andhra Pradesh",
            "additional_description": "Large pothole causing traffic issues.",
            "image_path": "uploads/sample_pothole.jpg",
            "ai_category": "Pothole",
            "ai_description": "Deep pothole visible on the main road surface.",
            "severity": "High",
            "suggested_action": "Immediate road repair required.",
            "status": "Pending",
        },
        {
            "citizen_name": "Priya Sharma",
            "phone": "9123456780",
            "location": "Market Street, Rajahmundry, Andhra Pradesh",
            "additional_description": "Garbage not collected for 3 days.",
            "image_path": "uploads/sample_garbage.jpg",
            "ai_category": "Garbage",
            "ai_description": "Accumulated waste near the roadside.",
            "severity": "Medium",
            "suggested_action": "Schedule garbage collection immediately.",
            "status": "Under Review",
        },
        {
            "citizen_name": "Anil Reddy",
            "phone": "9988776655",
            "location": "Gandhi Nagar, Kakinada, Andhra Pradesh",
            "additional_description": "Blocked drainage causing water logging.",
            "image_path": "uploads/sample_drainage.jpg",
            "ai_category": "Drainage",
            "ai_description": "Blocked drainage pipe with stagnant water.",
            "severity": "High",
            "suggested_action": "Clear drainage and inspect pipeline.",
            "status": "In Progress",
        },
        {
            "citizen_name": "Sneha Devi",
            "phone": "9012345678",
            "location": "Station Road, Vijayawada, Andhra Pradesh",
            "additional_description": "Water leaking from pipeline.",
            "image_path": "uploads/sample_water.jpg",
            "ai_category": "Water Leakage",
            "ai_description": "Visible water leakage from underground pipe.",
            "severity": "Medium",
            "suggested_action": "Repair the leaking water pipeline.",
            "status": "Resolved",
        },
        {
            "citizen_name": "Karthik Rao",
            "phone": "9876501234",
            "location": "Park Avenue, Visakhapatnam, Andhra Pradesh",
            "additional_description": "Street light not working at night.",
            "image_path": "uploads/sample_light.jpg",
            "ai_category": "Broken Street Light",
            "ai_description": "Non-functional street light pole observed.",
            "severity": "Low",
            "suggested_action": "Replace or repair the street light.",
            "status": "Pending",
        },
        {
            "citizen_name": "Meena Kumari",
            "phone": "8765432109",
            "location": "Highway Road, Guntur, Andhra Pradesh",
            "additional_description": "Road surface severely damaged.",
            "image_path": "uploads/sample_road.jpg",
            "ai_category": "Damaged Road",
            "ai_description": "Cracked and uneven road surface detected.",
            "severity": "High",
            "suggested_action": "Resurface the damaged road section.",
            "status": "Under Review",
        },
        {
            "citizen_name": "Vikram Singh",
            "phone": "9123456789",
            "location": "College Road, Tirupati, Andhra Pradesh",
            "additional_description": "Open manhole without cover.",
            "image_path": "uploads/sample_manhole.jpg",
            "ai_category": "Open Manhole",
            "ai_description": "Uncovered manhole posing safety risk.",
            "severity": "High",
            "suggested_action": "Cover manhole immediately for public safety.",
            "status": "In Progress",
        },
        {
            "citizen_name": "Lakshmi N",
            "phone": "9876543210",
            "location": "Green Park, Nellore, Andhra Pradesh",
            "additional_description": "Tree fallen after storm.",
            "image_path": "uploads/sample_tree.jpg",
            "ai_category": "Fallen Tree",
            "ai_description": "Fallen tree blocking the pathway.",
            "severity": "Medium",
            "suggested_action": "Remove fallen tree and clear the area.",
            "status": "Resolved",
        },
        {
            "citizen_name": "Arjun Patel",
            "phone": "9000112233",
            "location": "Lake View, Warangal, Telangana",
            "additional_description": "Miscellaneous public infrastructure issue.",
            "image_path": "uploads/sample_other.jpg",
            "ai_category": "Other",
            "ai_description": "General public infrastructure concern reported.",
            "severity": "Low",
            "suggested_action": "Inspect the location and assign appropriate department.",
            "status": "Pending",
        },
    ]

    count = 0
    for i, sample in enumerate(samples):
        created_at = datetime.now().replace(hour=10 + i % 8).isoformat()
        cursor.execute(
            """
            INSERT INTO complaints (
                citizen_name, phone, location, additional_description,
                image_path, ai_category, ai_description, severity,
                suggested_action, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sample["citizen_name"],
                sample["phone"],
                sample["location"],
                sample["additional_description"],
                sample["image_path"],
                sample["ai_category"],
                sample["ai_description"],
                sample["severity"],
                sample["suggested_action"],
                sample["status"],
                created_at,
            ),
        )
        count += 1

    conn.commit()
    conn.close()
    return count
