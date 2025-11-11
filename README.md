# IODD Management System

A comprehensive Python-based tool for managing IO-Link Device Description (IODD) files with automatic adapter generation capabilities for various platforms including Node-RED.

## Features

- **IODD File Management**: Import, store, and manage IODD XML files and packages
- **Intelligent Parsing**: Extract device parameters, process data, and metadata
- **Database Storage**: SQLite-based storage with full device profile persistence
- **Adapter Generation**: Automatically generate platform-specific adapters
- **REST API**: Full-featured API for integration with other systems
- **Extensible Architecture**: Plugin-based system for adding new platforms

## Supported Platforms

### Currently Implemented
- ✅ **Node-RED**: Generate custom Node-RED nodes with full device interface

### Planned
- 🚧 Python device drivers
- 🚧 MQTT bridge adapters
- 🚧 OPC UA server configurations
- 🚧 Modbus mappings
- 🚧 REST API clients

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/iodd-manager.git
cd iodd-manager

# Install dependencies
pip install -r requirements.txt

# Initialize the system
python iodd_manager.py list
```

## Quick Start

### Command Line Interface

#### Import an IODD file
```bash
# Import a standalone IODD XML file
python iodd_manager.py import device_description.xml

# Import an IODD package (.iodd file)
python iodd_manager.py import sensor_package.iodd
```

#### List imported devices
```bash
python iodd_manager.py list
```

#### Generate a Node-RED adapter
```bash
python iodd_manager.py generate 1 --platform node-red --output ./generated
```

### REST API

#### Start the API server
```bash
python api.py
# or
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

#### API Examples

##### Upload an IODD file
```bash
curl -X POST "http://localhost:8000/api/iodd/upload" \
  -F "file=@device.xml"
```

##### List all devices
```bash
curl "http://localhost:8000/api/iodd"
```

##### Generate Node-RED adapter
```bash
curl -X POST "http://localhost:8000/api/generate/adapter" \
  -H "Content-Type: application/json" \
  -d '{"device_id": 1, "platform": "node-red"}'
```

##### Download generated adapter
```bash
curl "http://localhost:8000/api/generate/1/node-red/download" \
  --output adapter.zip
```

### Python API

```python
from iodd_manager import IODDManager

# Initialize the manager
manager = IODDManager()

# Import an IODD file
device_id = manager.import_iodd("path/to/device.xml")
print(f"Imported device with ID: {device_id}")

# List all devices
devices = manager.list_devices()
for device in devices:
    print(f"{device['id']}: {device['product_name']}")

# Generate a Node-RED adapter
output_dir = manager.generate_adapter(
    device_id=1,
    platform="node-red",
    output_path="./generated"
)
print(f"Generated adapter in: {output_dir}")
```

## Generated Node-RED Node Structure

When generating a Node-RED adapter, the system creates:

```
generated/
└── node-red/
    └── device_1/
        ├── package.json          # NPM package configuration
        ├── device-name.js        # Node logic implementation
        ├── device-name.html      # Node UI configuration
        └── README.md            # Documentation
```

### Installing Generated Node-RED Nodes

```bash
cd generated/node-red/device_1
npm link

cd ~/.node-red
npm link node-red-contrib-device-name

# Restart Node-RED
node-red-restart
```

## Architecture Overview

### Core Components

1. **IODD Parser**: Extracts device information from XML
2. **Storage Manager**: SQLite database for persistence
3. **Adapter Generators**: Platform-specific code generators
4. **REST API**: FastAPI-based web service
5. **CLI Interface**: Command-line tool for management

### Database Schema

```sql
devices              # Device metadata and identification
├── id (PK)
├── vendor_id
├── device_id
├── product_name
└── import_date

parameters           # Device parameters
├── id (PK)
├── device_id (FK)
├── index
├── name
├── data_type
└── access_rights

generated_adapters   # Generated adapter code
├── id (PK)
├── device_id (FK)
├── platform
└── code_content
```

## Extending the System

### Adding a New Platform Generator

```python
from iodd_manager import AdapterGenerator, DeviceProfile

class MyPlatformGenerator(AdapterGenerator):
    @property
    def platform_name(self) -> str:
        return "my-platform"
    
    def generate(self, profile: DeviceProfile) -> Dict[str, str]:
        # Generate platform-specific files
        return {
            "main.ext": "generated code",
            "config.json": "configuration"
        }

# Register the generator
manager.generators['my-platform'] = MyPlatformGenerator()
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=iodd_manager tests/

# Run specific test file
pytest tests/test_parser.py
```

## Project Structure

```
iodd-manager/
├── iodd_manager.py      # Core implementation
├── api.py               # REST API
├── requirements.txt     # Python dependencies
├── iodd_storage/       # IODD file storage
├── generated/          # Generated adapters
├── tests/              # Test suite
└── README.md           # Documentation
```

## Roadmap

### Phase 1 (Complete) ✅
- Basic IODD parsing
- SQLite storage
- Node-RED generation
- REST API

### Phase 2 (In Progress) 🚧
- Enhanced validation
- Multi-version IODD support
- Python driver generation
- Web UI

### Phase 3 (Planned) 📋
- MQTT bridge generation
- OPC UA support
- Device simulation
- Cloud deployment

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review the API docs at `/docs`

## Acknowledgments

- IO-Link Community for IODD specifications
- Contributors and testers
- Industrial automation community

## Example IODD Files

You can find sample IODD files from various manufacturers:
- [IO-Link Community](https://ioddfinder.io-link.com/)
- Vendor websites (Siemens, Balluff, IFM, etc.)

## Performance Considerations

- **Parsing Speed**: ~100ms for typical IODD files
- **Generation Time**: <5 seconds per adapter
- **Storage**: ~10KB per device profile
- **API Response**: <200ms for most endpoints

## Security Notes

- Input validation on all uploaded files
- SQL injection protection via parameterized queries
- API authentication ready (implement as needed)
- Generated code sandboxing recommended

---

**Version**: 1.0.0  
**Status**: Production Ready (Core Features)  
**Python**: 3.10+  
**License**: MIT