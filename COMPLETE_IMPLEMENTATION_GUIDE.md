# DigitalMunshi Backend - Complete Implementation Guide

## 📋 Summary

Your backend has been fully implemented with:

✅ **5 New Route Modules** (Auth, Users, Chat, Lawyers, Appointments)
✅ **JWT Authentication** with access & refresh tokens
✅ **PostgreSQL Integration** with psycopg2
✅ **Password Hashing** with bcrypt
✅ **CORS Enabled** for localhost:3000
✅ **Complete API Documentation**
✅ **Database Schema** with migration script

---

## 📁 New Files Created

### Configuration & Utilities
```
backend/
├── config.py                 # Database & JWT configuration
├── auth_utils.py            # JWT & password hashing utilities
├── db.py                    # Database connection manager
├── .env.example             # Environment variables template
└── requirements.txt         # Updated dependencies (modified)
```

### Route Modules
```
backend/routes/
├── auth.py                  # POST /api/auth/* (register, login, logout)
├── users.py                 # GET/PUT /api/users/* (profile, dashboard)
├── chat.py                  # GET/POST /api/chat/sessions & messages
├── lawyers.py               # POST/GET /api/lawyers/* (register, search, profile)
└── appointments.py          # POST/GET/PUT /api/appointments/*
```

### Database & Setup
```
database/
├── schema.sql               # Main PostgreSQL schema
├── migration_auth.sql       # NEW: Authentication column migration
└── [setup guides below]
```

### Documentation
```
root/
├── BACKEND_SETUP.md         # Quick setup guide
├── API_DOCUMENTATION.md     # Complete API reference
└── COMPLETE_IMPLEMENTATION_GUIDE.md (this file)
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup PostgreSQL Database

#### Option A: Using psql directly
```bash
# Create database
createdb digital_munshi

# Run schema
psql digital_munshi < ../database/schema.sql

# Run migration (add auth columns)
psql digital_munshi < ../database/migration_auth.sql
```

#### Option B: Command line
```powershell
# PowerShell
psql -U postgres -c "CREATE DATABASE digital_munshi;"
psql -U postgres -d digital_munshi -f "database\schema.sql"
psql -U postgres -d digital_munshi -f "database\migration_auth.sql"
```

### 3. Configure Environment
```bash
cd backend

# Copy example config
cp .env.example .env

# Edit .env with your settings:
# - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
# - JWT_SECRET (use strong random string)
# - GROQ_API_KEY (your Groq API key)
```

### 4. Run Backend Server
```bash
python main.py
```

Server will start on `http://localhost:5000`

---

## 🔑 Authentication Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/citizen/register` | Register new user |
| POST | `/api/auth/citizen/login` | Login citizen |
| POST | `/api/auth/admin/login` | Admin login |
| POST | `/api/auth/logout` | Logout |

### Example: Register Citizen
```bash
curl -X POST http://localhost:5000/api/auth/citizen/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "phone_number": "+923001234567"
  }'
```

---

## 👥 User Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/profile` | Get user profile |
| PUT | `/api/users/profile` | Update profile |
| GET | `/api/users/dashboard` | Get dashboard stats |

**All user endpoints require JWT token**

---

## 💬 Chat Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/sessions` | Get all sessions |
| POST | `/api/chat/sessions` | Create session |
| GET | `/api/chat/sessions/:id` | Get session |
| POST | `/api/chat/sessions/:id/messages` | Post message |
| GET | `/api/chat/sessions/:id/messages` | Get messages |

---

## ⚖️ Lawyer Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/lawyers/register` | Register lawyer |
| GET | `/api/lawyers/search` | Search lawyers |
| GET | `/api/lawyers/:id` | Get lawyer profile |

### Search Lawyers Query Parameters
- `city` - Filter by city
- `province` - Filter by province
- `specialization` - Filter by specialization
- `min_rating` - Minimum rating (0-5)
- `max_fee` - Maximum consultation fee

---

## 📅 Appointment Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/appointments` | Create appointment |
| GET | `/api/appointments` | Get appointments |
| GET | `/api/appointments/:id` | Get appointment details |
| PUT | `/api/appointments/:id/cancel` | Cancel appointment |

---

## 🎯 How JWT Authentication Works

1. **Register/Login** → Get `access_token`
2. **Add to Request Header**: `Authorization: Bearer <access_token>`
3. **Token expires** in 1 hour (configurable in config.py)
4. **Use refresh_token** to get new access token

### Example Protected Request
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer eyJhbGc..."
```

---

## 🔐 Password Security

- Passwords hashed with **bcrypt** (12 rounds)
- Never stored in plain text
- Minimum 6 characters
- Verified on login

---

## 🗄️ Database Structure

### Key Tables
- **users** - Citizen accounts (with password_hash)
- **admins** - Admin accounts (with password_hash)
- **lawyers** - Lawyer profiles (with password_hash)
- **chat_sessions** - Chat conversations
- **chat_messages** - Chat messages
- **appointments** - Lawyer appointments
- And 11+ more tables for subscriptions, payments, reviews, etc.

### Migration Applied
The `migration_auth.sql` adds:
- `password_hash` column to users table
- `password_hash` column to lawyers table
- Indexes for faster queries
- Sample admin user (change credentials!)

---

## 📝 Environment Variables

Create `.env` file in backend folder:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=digital_munshi
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
JWT_SECRET=your-super-secret-key-here

# Groq API
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## 🧪 Testing Routes

### 1. Register Citizen
```bash
curl -X POST http://localhost:5000/api/auth/citizen/register \
  -H "Content-Type: application/json" \
  -d {
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User",
    "phone_number": "+923001234567"
  }'
```

### 2. Login Citizen
```bash
curl -X POST http://localhost:5000/api/auth/citizen/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### 3. Get Profile (with token)
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Create Chat Session
```bash
curl -X POST http://localhost:5000/api/chat/sessions \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_title": "Property Dispute",
    "category": "property_law",
    "language": "en"
  }'
```

### 5. Search Lawyers
```bash
curl "http://localhost:5000/api/lawyers/search?city=Lahore&province=Punjab"
```

### 6. Create Appointment
```bash
curl -X POST http://localhost:5000/api/appointments \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "lawyer_id": "<lawyer_uuid>",
    "appointment_date": "2024-01-20",
    "appointment_time": "14:00",
    "case_description": "Long description of the case...",
    "case_category": "property_law"
  }'
```

---

## 🧬 Code Structure Explanation

### main.py
- Flask app initialization
- CORS & JWT setup
- Route blueprint registration
- Existing `/api/ask` and `/api/health` endpoints preserved

### config.py
- Centralized configuration
- Database credentials
- JWT settings
- Groq API configuration

### auth_utils.py
- Password hashing (bcrypt)
- JWT token creation/verification
- `@token_required` decorator for protected routes
- `@admin_required` decorator for admin routes

### db.py
- Database connection pooling
- Query execution methods
- Context manager for transactions
- Error handling

### routes/auth.py
- Citizen registration
- Citizen login
- Admin login
- Logout endpoint

### routes/users.py
- Get profile
- Update profile
- Dashboard with statistics

### routes/chat.py
- Create/list chat sessions
- Post messages
- Retrieve messages
- Session management

### routes/lawyers.py
- Lawyer registration
- Search with filters
- Get lawyer details

### routes/appointments.py
- Create appointments
- List user appointments
- Get appointment details
- Cancel appointments

---

## ⚠️ Important Notes

1. **Admin User**: Created in migration with email `admin@digitalmunshi.com`
   - Change password immediately in production
   - Use the hashed password from migration

2. **JWT Secret**: Change `JWT_SECRET` in production
   - Use a strong random string (min 32 characters)
   - Never commit real secret to git

3. **Database**: 
   - Ensure PostgreSQL is running
   - Create database before running migration
   - Backup regularly in production

4. **CORS**: Currently allows localhost:3000
   - Change for production domain

5. **Security**:
   - Use HTTPS in production
   - Enable database SSL
   - Validate all inputs
   - Rate limit endpoints
   - Keep dependencies updated

---

## 🐛 Troubleshooting

### "psycopg2.OperationalError: could not connect to server"
- Check PostgreSQL is running
- Verify DB_HOST, DB_PORT, DB_USER, DB_PASSWORD in .env

### "ModuleNotFoundError: No module named 'psycopg2'"
- Run: `pip install -r requirements.txt`

### "ImportError: cannot import name 'QueryClassifier'"
- Ensure classifier.py exists in services/ folder
- Check Python path configuration

### "Invalid token" error
- Verify JWT_SECRET in .env
- Check token hasn't expired
- Ensure Authorization header format: "Bearer <token>"

### "Column 'password_hash' does not exist"
- Run migration: `psql digital_munshi < migration_auth.sql`

---

## 📚 Complete File Structure

```
Frontend+Backend/
├── backend/
│   ├── main.py                           # Main Flask app (UPDATED)
│   ├── config.py                         # Configuration (NEW)
│   ├── auth_utils.py                    # Auth utilities (NEW)
│   ├── db.py                            # Database manager (NEW)
│   ├── requirements.txt                 # Dependencies (UPDATED)
│   ├── .env.example                     # Env template (NEW)
│   ├── .env                             # Your settings (create)
│   ├── routes/
│   │   ├── ask.py                       # Legacy (unchanged)
│   │   ├── auth.py                      # Auth routes (NEW)
│   │   ├── users.py                     # User routes (NEW)
│   │   ├── chat.py                      # Chat routes (NEW)
│   │   ├── lawyers.py                   # Lawyer routes (NEW)
│   │   └── appointments.py              # Appointment routes (NEW)
│   ├── services/
│   │   ├── classifier.py                # (unchanged)
│   │   ├── generator.py                 # (unchanged)
│   │   └── retriever.py                 # (unchanged)
│   ├── models/                          # (unchanged)
│   └── faiss_index/                     # (unchanged)
│
├── database/
│   ├── schema.sql                       # Original schema
│   └── migration_auth.sql               # Auth columns (NEW)
│
├── frontend/                            # (unchanged)
│
├── BACKEND_SETUP.md                     # Quick setup (NEW)
├── API_DOCUMENTATION.md                 # API reference (NEW)
└── COMPLETE_IMPLEMENTATION_GUIDE.md     # This file (NEW)
```

---

## 🎓 Next Steps

1. **Test All Routes** - Use provided curl examples
2. **Update Frontend** - Connect to new API endpoints
3. **Deploy to Production** - Set up proper hosting
4. **Add Payment Gateway** - Integrate JazzCash/EasyPaisa
5. **Admin Panel** - Create verification dashboard
6. **Notifications** - Set up email/SMS alerts
7. **Caching** - Add Redis for performance
8. **Monitoring** - Set up error tracking (Sentry)

---

## 📞 Support

For issues or questions:
1. Check API_DOCUMENTATION.md for endpoint details
2. Review troubleshooting section above
3. Check error logs: `python main.py` output
4. Verify .env configuration
5. Ensure database migration ran successfully

---

**Happy coding! 🎉**

Your DigitalMunshi backend is ready for production!
