# Smart Public Issue Detection System using Generative AI

A simple Streamlit web application where citizens report public infrastructure issues with image uploads, Generative AI analyzes the images, and administrators manage complaints through a dashboard.

---

## Project Overview

This is a final-year academic project that demonstrates how **Generative AI**, **Python**, **Streamlit**, and **SQLite** can be combined to build a practical civic issue reporting system.

Citizens upload a photo of a public problem (pothole, garbage, drainage, etc.). The AI identifies the issue category, severity, and suggested action. Complaints are stored in SQLite and managed through an admin dashboard.

---

## Problem Statement

Public infrastructure issues like potholes, garbage accumulation, and broken street lights often go unreported or take too long to resolve. Citizens need a simple way to report problems, and authorities need organized complaint data with initial AI-assisted assessment.

---

## Objectives

1. Allow citizens to report public issues with image upload
2. Use Generative AI for automatic issue detection and severity assessment
3. Store complaints in a SQLite database
4. Provide an admin dashboard for complaint management
5. Demonstrate AI, database, and web application concepts for academic evaluation

---

## Features

- **Home Page** with project overview and workflow
- **Report Issue** with citizen details and image upload
- **AI Analysis** using Google Gemini (with Demo Mode fallback)
- **My Complaints** lookup by phone number
- **Admin Dashboard** with statistics, charts, filters, status updates, and delete
- **Sample Data** loader for demonstration
- **Demo AI Mode** — works without an API key

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend/UI | Streamlit |
| Programming | Python |
| Database | SQLite |
| AI | Google Gemini (Generative AI) |
| Image Processing | Pillow |
| Charts | Plotly |
| Environment | python-dotenv |

---

## System Architecture

```
Citizen
   ↓
Streamlit Interface
   ↓
Image Upload
   ↓
Generative AI (Gemini)
   ↓
Issue Detection
   ↓
SQLite Database
   ↓
Admin Dashboard
   ↓
Complaint Status Update
```

---

## Project Structure

```
smart-public-issue-detection/
│
├── app.py                  # Main Streamlit application
├── database.py             # SQLite database operations
├── ai_service.py           # Generative AI image analysis
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example            # Example environment file
├── .gitignore
├── README.md
├── PROJECT_EXPLANATION.md
├── VIVA_QUESTIONS.md
│
├── data/
│   └── complaints.db       # SQLite database (auto-created)
│
└── uploads/                # Uploaded issue images
    └── .gitkeep
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Clone or download** the project folder

2. **Open terminal** in the project directory:

```bash
cd "GenAI project"
```

3. **Create virtual environment** (recommended):

```bash
python -m venv venv
venv\Scripts\activate
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## Environment Setup

1. Copy the example environment file:

```bash
copy .env.example .env
```

2. Edit `.env`:

```env
AI_API_KEY=your_api_key_here
DEMO_MODE=True
ADMIN_PASSWORD=admin123
```

---

## AI API Setup

This project uses **Google Gemini** for image understanding.

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a free API key
3. Add it to `.env`:

```env
AI_API_KEY=your_actual_api_key
DEMO_MODE=False
```

4. Restart the application

**Note:** If no API key is set or `DEMO_MODE=True`, the app uses Demo AI Mode with sample results.

---

## Demo Mode

Set in `.env`:

```env
DEMO_MODE=True
```

When Demo Mode is active:
- No API key is required
- AI returns a sample pothole analysis
- A **🟡 Demo AI Mode** badge appears in the sidebar

This allows you to demonstrate the project without depending on an external API.

---

## How to Run

```bash
streamlit run app.py
```

The application opens in your browser at `http://localhost:8501`

---

## Database Structure

**Table: complaints**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| citizen_name | TEXT | Name of the citizen |
| phone | TEXT | Phone number |
| location | TEXT | Issue location |
| additional_description | TEXT | Extra details |
| image_path | TEXT | Path to uploaded image |
| ai_category | TEXT | AI-detected category |
| ai_description | TEXT | AI-generated description |
| severity | TEXT | Low / Medium / High |
| suggested_action | TEXT | AI-suggested action |
| status | TEXT | Pending / Under Review / In Progress / Resolved |
| created_at | TEXT | Timestamp |

---

## Application Workflow

1. Citizen opens **Report Issue**
2. Enters name, phone, location, description
3. Uploads an image of the public issue
4. Clicks **Analyze Issue with AI**
5. AI returns category, description, severity, suggested action
6. Citizen clicks **Submit Complaint**
7. Complaint saved to SQLite with status **Pending**
8. Admin logs in and reviews complaints
9. Admin updates status: Pending → Under Review → In Progress → Resolved

---

## Admin Access

- **Password:** `admin123` (configurable in `.env`)

> ⚠️ **Important:** This simple password is only for academic demonstration and is **NOT suitable for production**.

---

## Testing Checklist

| # | Test | Expected Result |
|---|------|-----------------|
| 1 | Home page | Title, features, workflow visible |
| 2 | Report issue | Form loads correctly |
| 3 | Image upload | Image preview shown |
| 4 | Image preview | Valid image displayed |
| 5 | AI analysis | AI result displayed |
| 6 | Demo AI mode | Demo badge shown, sample result returned |
| 7 | Complaint submission | Success message with complaint ID |
| 8 | SQLite storage | Complaint appears in admin table |
| 9 | My Complaints | Search by phone returns results |
| 10 | Admin login | Correct password grants access |
| 11 | Admin dashboard | Statistics and charts load |
| 12 | Statistics | KPI metrics show correct counts |
| 13 | Filters | Category/severity/status filters work |
| 14 | Status update | Status changes in database |
| 15 | Delete complaint | Complaint removed after confirmation |
| 16 | Invalid input | Friendly error messages |
| 17 | Invalid image | Error for wrong file type |
| 18 | Large image | Error for files > 5 MB |
| 19 | AI failure | Fallback result, no crash |
| 20 | Sample data | 9 sample complaints inserted |

---

## Limitations

1. **No real authentication** — phone-based lookup and simple admin password only
2. **AI accuracy** — The AI-generated analysis is an initial assessment and should be verified by the concerned authority. AI is **not 100% accurate**.
3. **No GPS/Maps** — location is text-based only
4. **Single-user SQLite** — not suitable for high concurrent traffic
5. **No notifications** — no SMS/email alerts
6. **Demo Mode** — returns fixed sample data when API key is unavailable

---

## Future Enhancements

- GPS location and Google Maps integration
- Mobile application
- Municipal corporation API integration
- SMS, email, and WhatsApp notifications
- Automatic duplicate complaint detection
- Multilingual AI support
- Advanced severity prediction
- Cloud deployment (Streamlit Cloud, AWS, etc.)
- Real-time complaint tracking
- Automatic department assignment

---

## Disclaimer

The AI-generated analysis is an **initial assessment** and should be verified by the concerned authority. This project is built for **academic demonstration purposes**.

---

## Author

Final Year B.Tech Project — Artificial Intelligence and Data Science
