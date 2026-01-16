# Database Migrations

## How to Apply Migrations to Railway (Production)

### Method 1: Using Railway CLI (Recommended)

1. Install Railway CLI if you haven't:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Link to your project:
```bash
railway link
```

4. Connect to database and run migration:
```bash
railway run psql $DATABASE_URL -f migrations/001_add_broadcast_features.sql
```

### Method 2: Using Railway Dashboard

1. Go to your Railway project dashboard
2. Click on your PostgreSQL service
3. Click "Data" tab
4. Click "Query" button
5. Copy and paste the contents of `001_add_broadcast_features.sql`
6. Click "Run Query"

### Method 3: Using pgAdmin or DBeaver

1. Get your DATABASE_URL from Railway:
   - Go to PostgreSQL service → Variables → DATABASE_URL
   
2. Connect using the connection string in your database client

3. Run the SQL migration file

## Migration Files

- `001_add_broadcast_features.sql` - Adds broadcast features (can_broadcast column, telegram bot columns, broadcast table)

## Verification

After running the migration, verify it worked:

```sql
-- Check if can_broadcast column exists
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'subscriptionplan';

-- Check if broadcast table exists
SELECT table_name 
FROM information_schema.tables 
WHERE table_name = 'broadcast';

-- Check telegram columns in shop
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'shop' 
AND column_name IN ('telegram_bot_token', 'is_bot_active');
```
