xxxxxxxxxxy# Project Explanation — Smart Public Issue Detection System

## 1. What is the Project?

This project is a **Smart Public Issue Detection System** built using Python and Streamlit. Citizens can report public infrastructure problems (like potholes, garbage, drainage issues) by uploading a photo. Generative AI analyzes the image and identifies the issue type, severity, and suggested action. All complaints are stored in a SQLite database, and administrators can manage them through a dashboard.

---

## 2. What Problem Does It Solve?

In many cities, public issues go unreported or take a long time to fix because:
- Citizens don't know how to report problems
- Manual complaint processing is slow
- There is no organized system to track issues

Our system provides a simple web interface where anyone can report a problem with a photo, and AI helps classify the issue automatically.

---

## 3. Why Did We Choose This Project?

- It combines **AI**, **web development**, and **database management**
- It solves a **real-world civic problem**
- It is **simple enough** for a final-year student project
- It is **easy to demonstrate** in viva and project presentation
- It shows practical use of **Generative AI** and **Computer Vision**

---

## 4. What is Generative AI?

Generative AI is a type of artificial intelligence that can **understand and generate** content such as text, images, and code. Unlike traditional software that follows fixed rules, Generative AI models (like Google Gemini) can analyze images and describe what they see in natural language.

---

## 5. How is Generative AI Used in This Project?

When a citizen uploads an image of a public issue:
1. The image is sent to the **Google Gemini API**
2. A carefully written **prompt** asks the AI to identify the issue
3. The AI returns a JSON response with category, description, severity, and suggested action
4. This result is displayed to the citizen and stored in the database

If no API key is available, **Demo Mode** returns a sample result for demonstration.

---

## 6. Why Streamlit?

Streamlit is a Python library for building web applications quickly. We chose it because:
- No HTML/CSS/JavaScript knowledge required
- Perfect for data and AI projects
- Easy to create forms, buttons, charts, and file uploads
- Runs with a single command: `streamlit run app.py`

---

## 7. Why SQLite?

SQLite is a lightweight file-based database. We chose it because:
- No separate database server needed
- Easy to set up for academic projects
- Supports SQL queries for CRUD operations
- Database is stored in a single file (`complaints.db`)

---

## 8. How Does Image Upload Work?

1. Citizen selects an image (JPG, JPEG, or PNG)
2. The app validates file type and size (max 5 MB)
3. Image is displayed as a preview
4. On submission, the image is saved in the `uploads/` folder with a unique filename
5. The file path is stored in the SQLite database

---

## 9. How Does AI Analyze the Image?

1. User clicks **"Analyze Issue with AI"**
2. The image is passed to `ai_service.py`
3. The AI prompt describes possible issue categories and asks for JSON output
4. Google Gemini analyzes the image and returns category, description, severity, and action
5. The response is parsed safely — if JSON is invalid, a fallback result is used

---

## 10. How is Severity Determined?

The AI model evaluates the image and assigns severity based on what it observes:
- **Low** — Minor issue, low immediate risk
- **Medium** — Moderate issue needing attention
- **High** — Serious issue requiring urgent action

The AI uses visual cues like size of damage, safety risk, and obstruction level.

---

## 11. How is the Complaint Stored?

When the citizen clicks **Submit Complaint**:
1. All form data and AI results are collected
2. `database.py` inserts a record into the `complaints` table using parameterized SQL
3. A unique complaint ID is generated (e.g., #1001)
4. Default status is set to **Pending**

---

## 12. How Does the Admin Dashboard Work?

1. Admin enters password (`admin123`)
2. Dashboard shows statistics: total, pending, under review, in progress, resolved
3. Plotly charts show complaints by category and status
4. Admin can filter complaints and search by location
5. Admin selects a complaint to view full details
6. Admin can update status or delete a complaint

---

## 13. What Happens When the Complaint is Resolved?

1. Admin changes status to **Resolved**
2. The update is saved in SQLite
3. Citizen can see updated status in **My Complaints** by searching with phone number
4. Statistics and charts reflect the change

---

## 14. What Are the Limitations?

- Simple password-based admin access (not production-ready)
- AI analysis may not always be accurate — needs human verification
- No GPS or map integration
- No SMS/email notifications
- SQLite is not ideal for very large-scale deployment
- Demo Mode returns fixed sample data

---

## 15. What is the Future Scope?

- GPS-based location tracking
- Google Maps integration
- Mobile app for Android/iOS
- Integration with municipal corporation systems
- SMS/WhatsApp notifications to citizens
- Multilingual AI support
- Cloud deployment for public access
- Automatic routing to relevant departments

---

# 2 Minute Explanation

> **Script for project guide presentation:**

"Good morning/afternoon, Sir/Madam.

My project is called **Smart Public Issue Detection System using Generative AI**.

The problem is that public issues like potholes, garbage, and broken street lights often go unreported or take too long to fix.

My solution is a **Streamlit web application** where citizens can report problems by uploading a photo. **Generative AI** — specifically Google Gemini — analyzes the image and automatically identifies the issue category, severity, and suggested action.

The complaint is stored in a **SQLite database**. An **Admin Dashboard** allows the administrator to view all complaints, filter them, update their status from Pending to Resolved, and see statistics with charts.

The project uses **Python, Streamlit, SQLite, Pillow, Plotly**, and the **Google Gemini API**. It also has a **Demo Mode** so I can demonstrate it without an internet API.

In summary, this project combines Artificial Intelligence, Computer Vision, Database Management, and Web Development to create a simple civic issue reporting system.

Thank you."

---

# 5 Minute Explanation

## Problem

Public infrastructure problems — potholes, garbage, drainage blocks, water leaks, broken lights — affect daily life. Reporting them is often difficult. There is no simple digital system for citizens to report issues with photo evidence and get automatic initial assessment.

## Solution

We built a **Smart Public Issue Detection System** — a web app where:
- Citizens fill a form and upload an issue photo
- AI analyzes the image and classifies the problem
- Complaints are stored and tracked until resolution

## Technology

| Layer | Tool |
|-------|------|
| UI | Streamlit |
| Backend | Python |
| Database | SQLite |
| AI | Google Gemini API |
| Images | Pillow |
| Charts | Plotly |

## Workflow

1. **Home** — Overview and features
2. **Report Issue** — Citizen details + image upload
3. **AI Analysis** — Category, severity, description, action
4. **Submit** — Save to SQLite with status Pending
5. **My Complaints** — Search by phone number
6. **Admin Dashboard** — Statistics, charts, filters, status update, delete

## AI

We use **prompt engineering** — a structured prompt tells Gemini to return JSON with category, description, severity, and suggested action. Categories include Pothole, Garbage, Drainage, Water Leakage, and others. If the API fails or no key is set, **Demo Mode** provides sample results.

## Database

SQLite stores all complaints with fields for citizen info, image path, AI results, status, and timestamp. We use **parameterized queries** to prevent SQL injection.

## Dashboard

Admin sees KPI metrics, bar chart (by category), pie chart (by status), filterable complaint table, and can update status or delete complaints.

## Result

A working, demonstrable system that shows Generative AI, CRUD operations, file upload, and data visualization — suitable for final-year project evaluation.

## Future Scope

GPS, maps, mobile app, municipal integration, notifications, multilingual AI, and cloud deployment.

## Closing

"The AI analysis is an initial assessment and should be verified by authorities. AI is not 100% accurate, but it speeds up complaint classification and helps administrators prioritize issues."

Thank you.
