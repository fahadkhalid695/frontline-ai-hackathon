# 🔧 Troubleshooting Guide

## ❌ "Failed to process emergency. Please try again."

This error occurs when the frontend can't communicate with the backend. Here's how to fix it:

### 🔍 **Step 1: Check if Backend is Running**

Open a terminal and run:
```bash
# Check if backend is running
curl http://localhost:5000/health

# If you get a response, backend is running ✅
# If you get "connection refused", backend is not running ❌
```

### 🚀 **Step 2: Start the Backend**

#### Option A: Use Debug Backend (Recommended for troubleshooting)
```bash
python debug-backend.py
```

#### Option B: Use Regular Backend
```bash
python app.py
```

#### Option C: Use Startup Scripts
```bash
# Windows
start-local.bat

# Linux/Mac
./start-local.sh
```

### 🔍 **Step 3: Verify Backend is Working**

Test the API directly:
```bash
curl -X POST http://localhost:5000/api/emergency \
  -H "Content-Type: application/json" \
  -d '{
    "action": "triage",
    "case_data": {
      "symptoms": "test",
      "emergency_type": "medical",
      "location": "Lahore"
    }
  }'
```

### 🔍 **Step 4: Check for Port Conflicts**

If port 5000 is busy:
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

**Fix**: Kill the process using port 5000 or change the port in both:
- `app.py` (line: `app.run(debug=True, host='0.0.0.0', port=5000)`)
- `frontend/app/page.tsx` (line: `fetch('http://localhost:5000/api/emergency'`)

### 🔍 **Step 5: Check Frontend Configuration**

Verify the API URL in `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 🔍 **Step 6: Browser Network Tab**

1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Submit the form
4. Look for the API call to `/api/emergency`
5. Check the error details

### 🔍 **Common Issues and Fixes:**

#### Issue 1: "Connection Refused"
**Cause**: Backend not running
**Fix**: Start backend with `python app.py`

#### Issue 2: "CORS Error"
**Cause**: CORS not properly configured
**Fix**: Ensure `flask-cors` is installed: `pip install flask-cors`

#### Issue 3: "404 Not Found"
**Cause**: Wrong API endpoint
**Fix**: Verify URL is `http://localhost:5000/api/emergency`

#### Issue 4: "500 Internal Server Error"
**Cause**: Backend error (missing dependencies, import issues)
**Fix**: Check backend logs, install missing packages

#### Issue 5: "Timeout"
**Cause**: Backend taking too long
**Fix**: Check if all agents are working: `curl http://localhost:5000/api/test-agents`

### 🛠️ **Quick Fix Commands:**

```bash
# 1. Install missing dependencies
pip install flask flask-cors requests python-dateutil

# 2. Start debug backend
python debug-backend.py

# 3. Test health
curl http://localhost:5000/health

# 4. Test emergency endpoint
curl -X POST http://localhost:5000/api/emergency \
  -H "Content-Type: application/json" \
  -d '{"action":"triage","case_data":{"symptoms":"test","emergency_type":"medical","location":"Lahore"}}'
```

### 📋 **Checklist:**

- [ ] Backend server is running (`python app.py`)
- [ ] Health check works (`curl http://localhost:5000/health`)
- [ ] No port conflicts (port 5000 is free)
- [ ] Dependencies installed (`pip install -r requirements-local.txt`)
- [ ] Frontend is running (`npm run dev` in frontend folder)
- [ ] Browser can access both frontend (3000) and backend (5000)

### 🆘 **Still Not Working?**

Run the comprehensive check:
```bash
python check-and-fix.py
```

This will identify and fix most common issues automatically.

### 📞 **Get Detailed Error Info:**

1. Start debug backend: `python debug-backend.py`
2. Check browser console (F12 → Console)
3. Check backend logs in terminal
4. Look for specific error messages

The debug backend provides detailed logging to help identify the exact issue.