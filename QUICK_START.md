# 🚀 IODD Manager - QUICK START

## Installation in 30 Seconds!

### Windows Users:
1. Extract the ZIP file
2. Double-click `setup.bat`
3. That's it! The browser will open automatically

### Mac/Linux Users:
1. Extract the ZIP file
2. Open terminal in the folder
3. Run: `bash setup.sh` or `python3 start.py`
4. Browser opens automatically

## Manual Start (All Platforms)
```bash
# Simple start
python start.py

# Or if you have python3
python3 start.py
```

## What You Get

✨ **Beautiful Web Interface** at http://localhost:3000
- Drag & drop IODD files
- 3D visualizations
- Real-time charts
- One-click adapter generation

📡 **REST API** at http://localhost:8000
- Full CRUD operations
- Swagger docs at /docs
- JSON responses

## First Steps

1. **Upload an IODD**: 
   - Click the "+" button or drag & drop
   - Supports .xml and .iodd files

2. **View Devices**:
   - See all your devices in a beautiful grid
   - Click for detailed parameters

3. **Generate Adapters**:
   - Select a device
   - Choose Node-RED platform
   - Get instant code generation

## File Structure
```
iodd-manager/
├── setup.bat           # Windows quick setup
├── setup.sh           # Mac/Linux quick setup  
├── start.py           # Main launcher
├── iodd_manager.py    # Core system
├── api.py             # REST API server
├── frontend/
│   └── index.html     # Complete web interface
└── requirements.txt   # Python dependencies
```

## Need Help?

- Check the README.md for detailed documentation
- API docs at http://localhost:8000/docs
- All files are self-documented

## Stop the Application

Press `Ctrl+C` in the terminal window

---
Enjoy your professional IODD Management System! 🎉
