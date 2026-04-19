# 🚀 Skill Bot API Setup Guide

## Files Created in skill_bot/

✅ **app.py** - Flask API with all routes  
✅ **requirements.txt** - Python dependencies  

---

## 🎯 Quick Start

### Step 1: Install Dependencies
```bash
cd skill_bot
pip install -r requirements.txt
```

### Step 2: Run Flask API
```bash
cd skill_bot
python app.py
```

**Expected Output:**
```
Starting Skill Bot API Server...
🚀 Running on http://localhost:5000

Available Endpoints:
  GET  /api/options          - Get fields and cities
  POST /api/audit            - Market audit
  POST /api/projects         - Project recommendations
  POST /api/roadmap          - Learning roadmap
  POST /api/interview        - Interview challenge
  GET  /api/powerbi          - PowerBI insights
  GET  /health               - Health check
```

### Step 3: Start React (New Terminal)
```bash
cd package
npm start
```

### Step 4: Access Market Audit
```
http://localhost:3000/#/market-audit
```

---

## 📡 API Endpoints Available

### 1. GET /api/options
Returns fields and cities for dropdowns
```bash
curl http://localhost:5000/api/options
```

### 2. POST /api/audit
Market audit request
```bash
curl -X POST http://localhost:5000/api/audit \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmed","city":"Lahore","field":"CS"}'
```

### 3. POST /api/projects
Project recommendations
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"field":"AI","level":"Easy"}'
```

### 4. POST /api/roadmap
Learning roadmap
```bash
curl -X POST http://localhost:5000/api/roadmap \
  -H "Content-Type: application/json" \
  -d '{"name":"Ahmed","choice":"CS"}'
```

### 5. POST /api/interview
Interview challenge
```bash
curl -X POST http://localhost:5000/api/interview \
  -H "Content-Type: application/json" \
  -d '{"user_input":"What is REST API?"}'
```

### 6. GET /api/powerbi
PowerBI insights
```bash
curl http://localhost:5000/api/powerbi
```

### 7. GET /health
Health check
```bash
curl http://localhost:5000/health
```

---

## 📂 File Structure

```
React-Vora-v1.1-31-May-2022/
├── skill_bot/
│   ├── app.py                    ⭐ Flask API
│   ├── requirements.txt          ⭐ Dependencies
│   ├── main.py                   (existing)
│   ├── assesment.py              (existing, no Streamlit)
│   ├── projects.py               (existing, no Streamlit)
│   ├── roadmap.py                (existing, no Streamlit)
│   ├── powerbi.py                (existing, no Streamlit)
│   ├── skill_chatbot.py          (existing, no Streamlit)
│   ├── project_bot.py            (existing, no Streamlit)
│   ├── ddata.py                  (existing)
│   └── ...
│
└── package/
    ├── src/jsx/pages/SkillBot/
    │   └── MarketAudit.js        (React component)
    └── .env                       (already configured)
```

---

## ✅ What's Inside

### app.py Includes:
- ✅ 7 API endpoints
- ✅ CORS enabled
- ✅ Market audit with data from ddata.py
- ✅ All 5 skill bot modules (projects, roadmap, interview, powerbi)
- ✅ Error handling
- ✅ Health check

### requirements.txt Includes:
- ✅ Flask 2.3.0
- ✅ Flask-CORS 4.0.0
- ✅ python-dotenv
- ✅ pandas
- ✅ scikit-learn
- ✅ groq

---

## 🔗 Integration

React frontend automatically connects to:
- `http://localhost:5000/api/options` ← Get form dropdowns
- `http://localhost:5000/api/audit` ← Submit audit

No need to configure anything else! The React app is already set to use port 5000.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| Port 5000 in use | Kill the process or change port in app.py |
| "Connection refused" | Make sure Flask is running |
| CORS error | Flask-CORS is already enabled |

---

## 📋 Commands Summary

```bash
# Install
cd skill_bot && pip install -r requirements.txt

# Run API
cd skill_bot && python app.py

# Run React (new terminal)
cd package && npm start

# Test API
curl http://localhost:5000/health
curl http://localhost:5000/api/options

# Access app
http://localhost:3000/#/market-audit
```

---

All set! No backend folder needed. Everything is in skill_bot now! 🎉
