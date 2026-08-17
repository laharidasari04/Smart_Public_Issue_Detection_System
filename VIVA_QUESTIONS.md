# VIVA Questions and Answers

## Smart Public Issue Detection System using Generative AI

---

### 1. What is Generative AI?

Generative AI is a type of artificial intelligence that can create and understand content like text, images, and code. In our project, Google Gemini analyzes uploaded images and generates descriptions about public issues.

---

### 2. Why use Generative AI?

Generative AI can automatically analyze images and identify problems without manual inspection. This saves time for municipal authorities and helps classify complaints quickly.

---

### 3. What is Streamlit?

Streamlit is a Python library used to build web applications quickly. It allows us to create forms, buttons, charts, and file uploads using only Python code.

---

### 4. Why did you choose Streamlit?

Streamlit is beginner-friendly, requires no HTML/CSS/JavaScript, and is ideal for AI and data science projects. The entire app runs with one command: `streamlit run app.py`.

---

### 5. What is SQLite?

SQLite is a lightweight, file-based relational database. It stores data in a single file (`complaints.db`) and does not need a separate database server.

---

### 6. Why SQLite?

SQLite is simple to set up, perfect for academic projects, supports SQL queries, and requires no additional installation or configuration.

---

### 7. What is image understanding?

Image understanding is the ability of AI to analyze visual content in an image and describe what it sees — such as identifying a pothole, garbage, or broken street light.

---

### 8. How does AI analyze the image?

The uploaded image is sent to Google Gemini along with a structured prompt. The AI examines the image and returns JSON with category, description, severity, and suggested action.

---

### 9. What is prompt engineering?

Prompt engineering is the practice of writing clear instructions for AI models. Our prompt tells Gemini exactly what categories to use, what JSON format to return, and how to assign severity.

---

### 10. What is an API?

An API (Application Programming Interface) is a way for two software systems to communicate. Our app sends the image to the Gemini API and receives the analysis result back.

---

### 11. What is an API key?

An API key is a secret token that authenticates our application when calling the Gemini API. It is stored in the `.env` file and never hardcoded in source code.

---

### 12. Why use environment variables?

Environment variables keep sensitive data like API keys and passwords out of source code. They are loaded from the `.env` file using `python-dotenv`.

---

### 13. What is CRUD?

CRUD stands for Create, Read, Update, Delete — the four basic database operations. Our project creates complaints, reads them, updates status, and deletes complaints.

---

### 14. How is data stored?

Complaint data is stored in a SQLite database (`data/complaints.db`) in a table called `complaints` with fields for citizen info, AI results, status, and timestamp.

---

### 15. How is an image stored?

Uploaded images are saved in the `uploads/` folder with a unique filename generated using UUID. The file path is stored in the database.

---

### 16. What is severity?

Severity indicates how urgent an issue is. Our system uses three levels: **Low** (minor), **Medium** (moderate), and **High** (urgent/serious).

---

### 17. How is status updated?

The admin selects a complaint, chooses a new status (Pending, Under Review, In Progress, Resolved), and clicks Update Status. The change is saved in SQLite using an UPDATE query.

---

### 18. What is Demo Mode?

Demo Mode allows the project to work without an API key. It returns a sample AI analysis result so the project can be demonstrated offline or without API access.

---

### 19. What happens if AI fails?

If the AI API fails or returns invalid JSON, the system shows a safe fallback result instead of crashing. The user sees a friendly warning message.

---

### 20. What are the limitations?

- Simple password authentication (not production-ready)
- AI analysis needs human verification
- No GPS or map integration
- No SMS/email notifications
- SQLite not suitable for very large scale

---

### 21. What is the future scope?

GPS location, Google Maps, mobile app, municipal integration, SMS/WhatsApp notifications, multilingual AI, cloud deployment, and automatic department assignment.

---

### 22. Why not train your own model?

Training a custom deep learning model requires large datasets, GPU resources, and significant time. Using a pre-trained Generative AI API is simpler, faster, and more suitable for an academic project.

---

### 23. What is Computer Vision?

Computer Vision is a field of AI that enables computers to understand and interpret visual information from images and videos. Our project uses it through Gemini's image understanding capability.

---

### 24. What is Generative AI vs traditional ML?

Traditional ML uses labeled data to train models for specific tasks. Generative AI models like Gemini are pre-trained on vast data and can understand images and generate text without task-specific training.

---

### 25. How does the admin dashboard work?

Admin logs in with a password, sees statistics and charts, filters complaints, views details with images, updates status, and can delete complaints with confirmation.

---

### 26. Why use SQLite instead of MySQL?

SQLite requires no server setup, stores everything in one file, and is sufficient for a student project with moderate data. MySQL is better for large production systems.

---

### 27. What is Streamlit session state?

Session state (`st.session_state`) stores data between user interactions in Streamlit, such as AI analysis results, form data, and admin login status.

---

### 28. How does Streamlit run?

When you run `streamlit run app.py`, Streamlit starts a local web server and opens the application in your browser. It re-runs the Python script on each user interaction.

---

### 29. What security measures are used?

- Parameterized SQL queries (prevents SQL injection)
- Environment variables for secrets
- Image file validation (type and size)
- Admin password protection
- Delete confirmation before removal

Note: This is an academic project with basic security only.

---

### 30. How can the project be deployed?

The project can be deployed on **Streamlit Community Cloud** (free), or on cloud platforms like AWS, Azure, or Google Cloud. For production, use PostgreSQL instead of SQLite and proper authentication.

---

### 31. What categories can AI detect?

Pothole, Garbage, Drainage, Water Leakage, Broken Street Light, Damaged Road, Open Manhole, Fallen Tree, and Other.

---

### 32. What libraries are used?

Streamlit, Pillow, python-dotenv, Plotly, google-generativeai, and Python built-in sqlite3.

---

### 33. What is the maximum image size?

5 MB. Images larger than this are rejected with a friendly error message.

---

### 34. What image formats are supported?

JPG, JPEG, and PNG formats are supported.

---

### 35. How does My Complaints work?

The citizen enters their phone number. The system searches the database for matching complaints and displays them with images, status, severity, and AI analysis.

---

### 36. What is the admin password?

The default password is `admin123`, configurable in the `.env` file. This is for academic demonstration only.

---

### 37. What charts are shown in the admin dashboard?

1. **Bar chart** — Complaints by Category
2. **Pie chart** — Complaints by Status

Both are created using Plotly.

---

### 38. What is the complaint workflow?

Pending → Under Review → In Progress → Resolved

---

### 39. Is AI 100% accurate?

No. The AI-generated analysis is an initial assessment and should be verified by the concerned authority. We never claim 100% accuracy.

---

### 40. What is the project architecture?

Citizen → Streamlit UI → Image Upload → Generative AI → Issue Detection → SQLite Database → Admin Dashboard → Status Update
