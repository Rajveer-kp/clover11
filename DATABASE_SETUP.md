# Free Database Setup for Vercel

## Option 1: Neon (Recommended)

1. **Sign up at [neon.tech](https://neon.tech)**
2. **Create a new project**
3. **Copy the connection string** (looks like):
   ```
   postgresql://username:password@hostname.neon.tech/dbname?sslmode=require
   ```
4. **Add to Vercel environment variables as `DATABASE_URL`**

**Benefits:**
- ✅ 3GB free storage
- ✅ Serverless PostgreSQL
- ✅ Excellent for Vercel
- ✅ Auto-scaling

## Option 2: Supabase

1. **Sign up at [supabase.com](https://supabase.com)**
2. **Create new project**
3. **Go to Settings → Database**
4. **Copy PostgreSQL connection string**
5. **Add to Vercel as `DATABASE_URL`**

**Benefits:**
- ✅ 500MB free storage
- ✅ Real-time features
- ✅ Built-in auth (optional)
- ✅ Dashboard for data management

## Quick Setup Commands

After getting your DATABASE_URL, test the connection:

```python
# Test database connection
import os
from sqlalchemy import create_engine

DATABASE_URL = "your-database-url-here"
engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("✅ Database connection successful!")
    connection.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

## Environment Variables for Vercel

```bash
SECRET_KEY=your-secret-key-generate-a-strong-one
GOOGLE_CLIENT_ID=your-google-client-id-from-console
GOOGLE_CLIENT_SECRET=your-google-client-secret
DATABASE_URL=postgresql://username:password@hostname/database
FLASK_ENV=production
```

## Generate Strong SECRET_KEY

Run this in Python to generate a secure secret key:

```python
import secrets
print(secrets.token_hex(32))
```

Copy the output and use it as your SECRET_KEY.
