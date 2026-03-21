# How to Run ResQ Admin System

The system is currently running in your background terminals.

## 1. Access the Application
Open your web browser and go to:
👉 **http://localhost:8000/login.html**

## 2. Login Credentials
Use the following account to access the Admin Dashboard:
*   **Email**: `admin@resq.com`
*   **Password**: `password123`

## 3. Managing the System (If you restart)
If you close the terminals, run these commands in separate terminals from the project root `c:\my projects\New folder (4)`:

**Terminal 1 (Backend API):**
```powershell
cd project
python -m backend.app
```

**Terminal 2 (Frontend Server):**
```powershell
cd project/frontend
python -m http.server 8000
```
