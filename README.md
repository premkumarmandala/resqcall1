# 🚑 ResQ - Emergency Rescue & Routing Platform

ResQ is an intelligent, full-stack emergency response system designed to minimize response times during critical medical, vehicle, and trauma crises. By utilizing AI symptom analysis, it dynamically dispatches the optimal ambulance and routes patients directly to the most appropriate hospital based on active capacities and specialties. 

## 🚀 Key Functionalities & Features

### 🤖 AI-Powered Symptom Analysis (Google Gemini Integration)
- **Triage & Diagnosis:** Instantly analyzes user-reported symptoms to predict medical urgency.
- **Smart Recommendations:** Recommends specific hospital specialties and advises on first aid.
- **Embedded Chatbot:** A 24/7 AI chat assistant available for on-the-spot first aid advice.

### 📍 Live Real-Time Ambulance Tracking (Google Maps / Leaflet)
- **Smart Dispatch:** Locates the nearest available ambulance and assigns it.
- **Dual-Focus Map Tracking:** Dynamic live tracking actively plots shifting coordinates. The map bounds to continually fit both the user and the incoming ambulance on the screen.
- **Dashboard Integration:** Tracking map injects directly into the dashboard during active emergencies.

### 🏥 Intelligent Hospital Routing
- **Capacity Checks:** Continuously evaluates distances to nearby hospitals and checks capacity.
- **Turn-by-Turn Navigation:** Generates full route paths and ETAs.

---

## 📂 Project File Structure

Whenever you return to this project after a long time, use this structure to easily navigate where everything is located:

```text
📦 ResQ-call
 ┣ 📂 project
 ┃ ┣ 📂 backend                 # Python/Flask Backend API
 ┃ ┃ ┣ 📂 routes                # Individual API Endpoints
 ┃ ┃ ┃ ┣ 📜 ai_analysis.py      # Gemini Chatbot & Analysis Logic
 ┃ ┃ ┃ ┣ 📜 ambulances.py       # Ambulance updating/tracking
 ┃ ┃ ┃ ┣ 📜 call.py             # Twilio dialer logic
 ┃ ┃ ┃ ┣ 📜 emergencies.py      # Core emergency Creation/Cancellation
 ┃ ┃ ┃ ┣ 📜 hospitals.py        # Hospital fetching logic
 ┃ ┃ ┃ ┗ ...
 ┃ ┃ ┣ 📜 app.py                # Main backend server entry point
 ┃ ┃ ┣ 📜 config.py             # Server configurations & env loaders
 ┃ ┃ ┗ 📜 db.py                 # MySQL database connection
 ┃ ┣ 📂 database                # SQL Queries and Database schemas
 ┃ ┃ ┗ 📜 schema.sql            # Core database architecture
 ┃ ┣ 📂 frontend                # Vanilla JS, HTML & CSS
 ┃ ┃ ┣ 📂 css                   # Stylesheets 
 ┃ ┃ ┣ 📂 js                    
 ┃ ┃ ┃ ┗ 📜 main.js             # API request wrappers & token logic
 ┃ ┃ ┣ 📜 user_dashboard.html   # Main Dashboard (Tracking, Chat, Maps)
 ┃ ┃ ┣ 📜 login.html            # Authentication view
 ┃ ┃ ┗ ...
 ┃ ┣ 📜 .env                    # SENSITIVE: API Keys (Ignored by Git)
 ┃ ┗ 📜 requirements.txt        # Python backend dependencies
 ┣ 📜 .gitignore                # Protects .env from GitHub
 ┗ 📜 README.md                 # Project instructions
```

---

## 📝 How to Run the Project Again

If you restart your computer or come back to this project in the future, follow these exact 3 steps to boot everything back up:

### 1. Database & Environment Prep
* Make sure your local **MySQL Server** is running (`services.msc` -> `MySQL80` on Windows).
* Create the `resq_db` database and import `database/schema.sql` if it isn't deployed yet.
* Ensure your `.env` file exists directly inside the `project/` folder containing your `GEMINI_API_KEY`, passwords, etc.

### 2. Boot Up the Backend (Terminal 1)
Open a terminal in VS Code, navigate to the `project/` folder, and type:
```powershell
cd project
python -m backend.app
```
*(Leave this terminal window open. The Python Flask API runs on `http://localhost:5000`)*

### 3. Boot Up the Frontend (Terminal 2)
Click the `+` icon to open a second new terminal, navigate to the `project/frontend/` folder, and type:
```powershell
cd project/frontend
python -m http.server 8000
```
*(Leave this open as well. The frontend website is now hosted locally)*

### 🎉 4. Final Step
Open your web browser (Chrome/Edge) and navigate to:
👉 **http://localhost:8000/login.html**
