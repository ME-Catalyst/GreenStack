# GreenStack Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common issues in GreenStack.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [IODD Import Problems](#iodd-import-problems)
3. [EDS Import Problems](#eds-import-problems)
4. [Database Issues](#database-issues)
5. [API/Backend Issues](#apibackend-issues)
6. [Frontend Issues](#frontend-issues)
7. [Performance Problems](#performance-problems)
8. [File Upload Issues](#file-upload-issues)
9. [Parser Quality Assurance Issues](#parser-quality-assurance-issues)
10. [Production Deployment Issues](#production-deployment-issues)

---

## Installation Issues

### Problem: Dependencies fail to install

**Symptoms:**
- `npm install` fails with errors
- `pip install` shows dependency conflicts
- Missing packages errors

**Diagnosis:**

```bash
# Check Node.js version
node --version  # Should be >= 18.x

# Check Python version
python --version  # Should be >= 3.9

# Check npm version
npm --version  # Should be >= 9.x
```

**Solutions:**

1. **Update Node.js and npm:**
   ```bash
   # Using nvm (recommended)
   nvm install 18
   nvm use 18
   ```

2. **Clean install frontend dependencies:**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Clean install backend dependencies:**
   ```bash
   cd backend
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

4. **Fix Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

**Prevention:**
- Use specific versions in `package.json` and `requirements.txt`
- Document exact environment setup
- Use Docker for consistent environments

---

## IODD Import Problems

### Problem: IODD file fails to parse

**Symptoms:**
- "Failed to parse IODD file" error
- XML parsing errors
- Missing required fields

**Diagnosis:**

```bash
# Check file integrity
file your-iodd.xml

# Validate XML structure
xmllint --noout your-iodd.xml

# Check file encoding
file -i your-iodd.xml

# View parser logs
tail -f logs/greenstack.log | grep IODD
```

**Solutions:**

1. **Invalid XML structure:**
   - Open file in XML editor to check for errors
   - Ensure proper XML declaration: `<?xml version="1.0" encoding="UTF-8"?>`
   - Validate against IODD schema

2. **Encoding issues:**
   ```bash
   # Convert to UTF-8
   iconv -f ISO-8859-1 -t UTF-8 input.xml > output.xml
   ```

3. **Unsupported IODD version:**
   - Check IODD schema version in XML
   - GreenStack supports IODD 1.0, 1.1
   - Update parser if needed

4. **Corrupted ZIP file:**
   ```bash
   # Test ZIP integrity
   unzip -t your-iodd.zip

   # Extract and inspect
   unzip your-iodd.zip -d temp/
   ```

**Prevention:**
- Validate IODD files before importing
- Use IODD Checker tool from IO-Link consortium
- Keep parser updated with latest schemas

### Problem: Duplicate device error

**Symptoms:**
- "Device already exists" message
- Import succeeds but no new data appears

**Diagnosis:**

```sql
-- Check for existing device
SELECT * FROM devices
WHERE vendor_id = YOUR_VENDOR_ID
AND device_id = YOUR_DEVICE_ID;
```

**Solutions:**

1. **Intentional re-import (merge assets):**
   - This is expected behavior
   - New assets will be merged
   - Existing data preserved

2. **Force new import:**
   ```sql
   -- Delete existing device first (CAUTION: loses data)
   DELETE FROM devices WHERE id = DEVICE_ID;
   ```

3. **Update existing device:**
   - Delete device from Admin Console
   - Re-import with updated IODD

**Prevention:**
- Use version control for IODD files
- Document device import history
- Check device list before importing

---

## EDS Import Problems

### Problem: EDS file import fails

**Symptoms:**
- "Failed to parse EDS file" error
- Invalid format errors
- Missing required sections

**Diagnosis:**

```bash
# Check file format
file your-file.eds

# View file structure
head -n 50 your-file.eds

# Check for required sections
grep -E "\[Device\]|\[Assembly\]|\[Params\]" your-file.eds
```

**Solutions:**

1. **Invalid EDS format:**
   - Ensure file follows ODVA EDS specification
   - Check for proper section headers
   - Validate with EDS checker tool

2. **Missing required fields:**
   ```ini
   # Required in [Device] section:
   VendCode=
   ProdCode=
   Revision=
   ProdName=
   ```

3. **Encoding issues:**
   ```bash
   # Convert to ASCII
   iconv -f UTF-8 -t ASCII//TRANSLIT input.eds > output.eds
   ```

4. **File extension issues:**
   - Must be `.eds` or `.xml` (for EDS v2)
   - Check file isn't actually text file with wrong extension

**Prevention:**
- Use official EDS creation tools
- Validate before exporting from device tools
- Keep EDS specification reference handy

### Problem: EDS parameters not displaying

**Symptoms:**
- EDS imports successfully
- Parameters tab shows empty or incomplete data
- Some parameters missing

**Diagnosis:**

```sql
-- Check parameter count
SELECT COUNT(*) FROM eds_parameters WHERE eds_file_id = YOUR_EDS_ID;

-- View parameter details
SELECT * FROM eds_parameters
WHERE eds_file_id = YOUR_EDS_ID
ORDER BY parameter_number;

-- Check for parsing errors in logs
grep "EDS.*parameter" logs/greenstack.log
```

**Solutions:**

1. **Missing [Params] section:**
   - Add required parameters to EDS file
   - Reimport file

2. **Parameter format issues:**
   ```ini
   # Correct format:
   Param1=
   {
       1,    # Parameter number
       "Name",
       DATA_TYPE,
       ACCESS_RULE,
       ...
   }
   ```

3. **Database constraint violations:**
   - Check for duplicate parameter numbers
   - Ensure all required fields present

**Prevention:**
- Use EDS templates from device manufacturer
- Validate parameter sections before import
- Test with small EDS files first

---

## Database Issues

### Problem: Database locked error

**Symptoms:**
- "Database is locked" error
- Operations timeout
- Concurrent access issues

**Diagnosis:**

```bash
# Check for active connections
lsof | grep greenstack.db  # Linux/Mac
handle | findstr greenstack.db  # Windows

# Check database integrity
sqlite3 greenstack.db "PRAGMA integrity_check;"

# Check for locks
sqlite3 greenstack.db ".timeout 1000"
```

**Solutions:**

1. **Close competing connections:**
   ```bash
   # Find and kill processes
   ps aux | grep greenstack
   kill -9 PID
   ```

2. **Enable WAL mode (recommended):**
   ```sql
   PRAGMA journal_mode=WAL;
   ```

3. **Increase timeout:**
   ```python
   # In code
   conn = sqlite3.connect('greenstack.db', timeout=30.0)
   ```

4. **Restart backend:**
   ```bash
   pkill -f "uvicorn.*greenstack"
   python -m uvicorn src.api:app --reload
   ```

**Prevention:**
- Always use context managers for connections
- Implement connection pooling
- Enable WAL mode by default
- Close connections promptly

### Problem: Database corruption

**Symptoms:**
- "Database disk image is malformed"
- Query errors
- Data inconsistencies

**Diagnosis:**

```bash
# Check integrity
sqlite3 greenstack.db "PRAGMA integrity_check;"

# Check for journal files
ls -la *.db*

# Check file permissions
ls -la greenstack.db
```

**Solutions:**

1. **Attempt recovery:**
   ```bash
   # Backup first!
   cp greenstack.db greenstack.db.backup

   # Try to recover
   sqlite3 greenstack.db ".recover" | sqlite3 greenstack-recovered.db
   ```

2. **Export and reimport:**
   ```bash
   # Export to SQL
   sqlite3 greenstack.db .dump > backup.sql

   # Create new database
   rm greenstack.db
   sqlite3 greenstack.db < backup.sql
   ```

3. **Restore from backup:**
   ```bash
   # Use most recent backup
   cp backups/greenstack-YYYYMMDD.db greenstack.db
   ```

**Prevention:**
- Regular automated backups (see Disaster Recovery)
- Use WAL mode
- Monitor disk space
- Graceful shutdown procedures

### Problem: Slow database queries

**Symptoms:**
- API responses taking > 5 seconds
- UI freezing during data loading
- High CPU usage

**Diagnosis:**

```sql
-- Enable query timing
.timer on

-- Check table sizes
SELECT name, COUNT(*) FROM sqlite_master
JOIN pragma_table_info(name)
GROUP BY name;

-- Analyze query plan
EXPLAIN QUERY PLAN
SELECT * FROM devices WHERE vendor_id = 123;

-- Check for missing indexes
SELECT * FROM sqlite_master WHERE type='index';
```

**Solutions:**

1. **Add missing indexes:**
   ```sql
   -- Common indexes
   CREATE INDEX idx_devices_vendor_device
   ON devices(vendor_id, device_id);

   CREATE INDEX idx_parameters_device
   ON parameters(device_id);

   CREATE INDEX idx_eds_files_vendor_product
   ON eds_files(vendor_code, product_code);
   ```

2. **Optimize database:**
   ```sql
   VACUUM;
   ANALYZE;
   REINDEX;
   ```

3. **Implement pagination:**
   ```sql
   -- Instead of SELECT *
   SELECT * FROM devices
   ORDER BY import_date DESC
   LIMIT 100 OFFSET 0;
   ```

4. **Use connection pooling:**
   - Implement in FastAPI with SQLAlchemy
   - Reuse connections

**Prevention:**
- Create indexes during schema creation
- Regular VACUUM operations
- Monitor query performance
- Implement caching for frequent queries

---

## API/Backend Issues

### Problem: Backend won't start

**Symptoms:**
- `uvicorn` command fails
- Port already in use
- Import errors

**Diagnosis:**

```bash
# Check if port 8000 is in use
netstat -tulpn | grep :8000  # Linux
netstat -ano | findstr :8000  # Windows

# Test Python imports
python -c "from src.api import app; print('Success')"

# Check for Python errors
python -m uvicorn src.api:app --reload 2>&1 | tee error.log
```

**Solutions:**

1. **Port already in use:**
   ```bash
   # Find and kill process
   lsof -ti:8000 | xargs kill -9  # Linux/Mac

   # Or use different port
   uvicorn src.api:app --port 8001
   ```

2. **Import errors:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall

   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **Database initialization:**
   ```bash
   # Ensure database exists
   python -c "from src.greenstack import IODDManager; m = IODDManager(); print('DB initialized')"
   ```

**Prevention:**
- Use process manager (systemd, supervisor)
- Implement health checks
- Log startup sequence
- Use virtual environments

### Problem: CORS errors

**Symptoms:**
- "Access-Control-Allow-Origin" errors in browser
- API requests fail from frontend
- OPTIONS preflight fails

**Diagnosis:**

```bash
# Check CORS configuration
grep -r "CORSMiddleware" src/

# Test with curl
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8000/api/iodd/files
```

**Solutions:**

1. **Update CORS origins:**
   ```python
   # src/api.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "http://localhost:3000",
           "https://your-domain.com"
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **For development (ALL origins):**
   ```python
   allow_origins=["*"]  # Only for development!
   ```

3. **Check frontend proxy:**
   ```javascript
   // vite.config.js
   server: {
     proxy: {
       '/api': 'http://localhost:8000'
     }
   }
   ```

**Prevention:**
- Configure CORS early
- Document allowed origins
- Use environment variables for production
- Test CORS in staging environment

### Problem: 500 Internal Server Error

**Symptoms:**
- API returns 500 status
- Generic error message
- No detailed error info

**Diagnosis:**

```bash
# Check backend logs
tail -f logs/greenstack.log

# Enable debug mode
export DEBUG=1
uvicorn src.api:app --reload --log-level debug

# Test specific endpoint
curl -v http://localhost:8000/api/health
```

**Solutions:**

1. **Check exception logs:**
   - Look for Python tracebacks
   - Identify failing line/function
   - Fix underlying issue

2. **Database connection issue:**
   ```python
   # Check if database accessible
   try:
       conn = sqlite3.connect('greenstack.db')
       conn.close()
   except Exception as e:
       print(f"DB Error: {e}")
   ```

3. **Missing file/resource:**
   - Check file paths
   - Verify permissions
   - Ensure required files exist

**Prevention:**
- Implement proper error handling
- Log all exceptions
- Return meaningful error messages
- Use try-catch blocks

---

## Frontend Issues

### Problem: White screen / blank page

**Symptoms:**
- Page loads but shows nothing
- Console shows errors
- React doesn't mount

**Diagnosis:**

```bash
# Check browser console (F12)
# Look for:
# - JavaScript errors
# - Network failures
# - Module loading issues

# Check dev server
npm run dev 2>&1 | tee error.log

# Verify build
npm run build && ls -la dist/
```

**Solutions:**

1. **Clear cache and rebuild:**
   ```bash
   rm -rf node_modules dist .vite
   npm install
   npm run dev
   ```

2. **Check React mounting:**
   ```javascript
   // Check index.html has root div
   <div id="root"></div>

   // Check main.jsx
   ReactDOM.createRoot(document.getElementById('root')).render(...)
   ```

3. **Fix import errors:**
   - Check all import statements
   - Verify file paths
   - Ensure exports match imports

**Prevention:**
- Enable error boundaries
- Add loading states
- Implement fallback UI
- Test build before deploying

### Problem: API calls fail from frontend

**Symptoms:**
- Network errors in console
- 404 errors for API endpoints
- Timeout errors

**Diagnosis:**

```javascript
// Check API base URL
console.log('API URL:', import.meta.env.VITE_API_URL);

// Test API directly
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(console.log);
```

**Solutions:**

1. **Update API base URL:**
   ```javascript
   // src/App.jsx or config
   const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```

2. **Create .env file:**
   ```bash
   # .env.development
   VITE_API_URL=http://localhost:8000

   # .env.production
   VITE_API_URL=https://api.your-domain.com
   ```

3. **Use proxy in development:**
   ```javascript
   // vite.config.js
   export default {
     server: {
       proxy: {
         '/api': 'http://localhost:8000'
       }
     }
   }
   ```

**Prevention:**
- Use environment variables
- Centralize API configuration
- Add request/response interceptors
- Implement retry logic

---

## Performance Problems

### Problem: Slow page load times

**Symptoms:**
- Initial load takes > 5 seconds
- Large bundle size
- Slow Time to Interactive

**Diagnosis:**

```bash
# Check bundle size
npm run build
ls -lh dist/assets/*.js

# Analyze bundle
npm install -g source-map-explorer
source-map-explorer dist/assets/*.js

# Run Lighthouse audit
lighthouse http://localhost:5173 --view
```

**Solutions:**

1. **Code splitting:**
   ```javascript
   // Lazy load routes
   const AdminConsole = lazy(() => import('./components/AdminConsole'));
   ```

2. **Optimize images:**
   ```bash
   # Use WebP format
   # Compress images
   npm install -g imagemin-cli
   imagemin src/assets/*.png --plugin=webp > dist/assets/
   ```

3. **Enable production build:**
   ```bash
   npm run build -- --mode production
   ```

4. **Implement caching:**
   - Service worker
   - localStorage for data
   - CDN for static assets

**Prevention:**
- Monitor bundle size in CI
- Use code splitting
- Optimize images before adding
- Regular performance audits

### Problem: High memory usage

**Symptoms:**
- Backend consuming > 1GB RAM
- Memory grows over time
- Out of memory errors

**Diagnosis:**

```bash
# Monitor process memory
ps aux | grep uvicorn

# Check for memory leaks
pip install memory_profiler
python -m memory_profiler src/api.py

# Monitor in real-time
htop
```

**Solutions:**

1. **Close database connections:**
   ```python
   # Always use context managers
   with sqlite3.connect('greenstack.db') as conn:
       # operations
       pass  # Connection auto-closed
   ```

2. **Limit result sets:**
   ```sql
   -- Add LIMIT to queries
   SELECT * FROM devices LIMIT 1000;
   ```

3. **Implement pagination:**
   ```python
   @app.get("/api/devices")
   def get_devices(page: int = 0, limit: int = 100):
       offset = page * limit
       # Return paginated results
   ```

4. **Clear caches periodically:**
   ```python
   import gc
   gc.collect()  # Force garbage collection
   ```

**Prevention:**
- Profile memory usage
- Set resource limits
- Monitor in production
- Implement proper cleanup

---

## File Upload Issues

### Problem: Large file upload fails

**Symptoms:**
- Upload times out
- 413 Request Entity Too Large
- Upload progress stuck at 100%

**Diagnosis:**

```bash
# Check file size
ls -lh your-file.zip

# Test with smaller file
dd if=/dev/zero of=test.zip bs=1M count=10
```

**Solutions:**

1. **Increase backend limit:**
   ```python
   # FastAPI (in api.py)
   app.add_middleware(
       ...
       max_request_size=100_000_000  # 100 MB
   )
   ```

2. **Increase Nginx limit:**
   ```nginx
   client_max_body_size 100M;
   ```

3. **Increase timeout:**
   ```nginx
   client_body_timeout 300s;
   proxy_read_timeout 300s;
   ```

4. **Frontend timeout:**
   ```javascript
   await axios.post(url, data, {
     timeout: 300000  // 5 minutes
   });
   ```

**Prevention:**
- Document file size limits
- Show upload progress
- Implement chunked uploads for very large files
- Validate file size before upload

---

## Parser Quality Assurance Issues

### Problem: PQA reports parsing errors

**Symptoms:**
- Red status in PQA dashboard
- Missing required fields
- Schema validation errors

**Diagnosis:**

```bash
# Check PQA results
curl http://localhost:8000/api/admin/pqa/results

# View specific device errors
curl http://localhost:8000/api/admin/pqa/device/DEVICE_ID
```

**Solutions:**

1. **Missing required fields:**
   - Update IODD/EDS to include required fields
   - Fix parser to handle optional fields gracefully

2. **Schema validation:**
   - Ensure IODD conforms to schema version
   - Update schema definitions if needed

3. **Data type mismatches:**
   - Check parameter data types
   - Ensure proper type conversion in parser

**Prevention:**
- Run PQA before importing files
- Validate with official checkers
- Keep parser schema up to date
- Add unit tests for edge cases

---

## Production Deployment Issues

### Problem: SSL certificate errors

**Symptoms:**
- "Certificate not valid" in browser
- HTTPS connection fails
- Certificate expired warnings

**Diagnosis:**

```bash
# Check certificate
openssl x509 -in /etc/letsencrypt/live/domain/cert.pem -text -noout

# Test SSL
curl -vI https://your-domain.com

# Check certificate expiry
certbot certificates
```

**Solutions:**

1. **Renew certificate:**
   ```bash
   sudo certbot renew
   sudo systemctl reload nginx
   ```

2. **Fix permissions:**
   ```bash
   sudo chown -R root:root /etc/letsencrypt
   sudo chmod 755 /etc/letsencrypt/live
   sudo chmod 755 /etc/letsencrypt/archive
   ```

3. **Fix certificate chain:**
   ```bash
   # Use fullchain, not cert
   ssl_certificate /etc/letsencrypt/live/domain/fullchain.pem;
   ```

**Prevention:**
- Enable auto-renewal cron job
- Monitor certificate expiry
- Test renewal with --dry-run
- Set up expiry alerts

---

## Getting Help

If this guide doesn't solve your issue:

1. **Check logs:**
   - Backend: `logs/greenstack.log`
   - Frontend: Browser console (F12)
   - Nginx: `/var/log/nginx/greenstack-error.log`

2. **Search GitHub issues:**
   https://github.com/anthropics/greenstack/issues

3. **Create detailed bug report:**
   - Include error messages
   - Steps to reproduce
   - Environment details (OS, versions)
   - Relevant logs

4. **Community support:**
   - GitHub Discussions
   - Stack Overflow (tag: greenstack)

5. **Contact support:**
   support@greenstack.io

---

## Additional Resources

- [Installation Guide](../README.md)
- [API Documentation](http://localhost:8000/docs)
- [Disaster Recovery Plan](./DISASTER_RECOVERY.md)
- [SSL/TLS Setup](../deployment/nginx/README.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

**Last Updated:** 2025-01-18
**Version:** 1.0.0
