"""
Document and Adapter Generation Module

This module contains classes for generating Node-RED nodes and other adapter formats
from IODD device profiles.
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Dict

from jinja2 import Template

from src.models import DeviceProfile

logger = logging.getLogger(__name__)


class AdapterGenerator(ABC):
    """Abstract base class for adapter generators"""

    @abstractmethod
    def generate(self, profile: DeviceProfile) -> Dict[str, str]:
        """Generate adapter code for the device profile"""
        pass

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform name"""
        pass

    def validate(self, code: Dict[str, str]) -> bool:
        """Validate generated code"""
        return all(code.values())


class NodeREDGenerator(AdapterGenerator):
    """Generate Node-RED nodes from IODD profiles"""

    @property
    def platform_name(self) -> str:
        return "node-red"

    def generate(self, profile: DeviceProfile) -> Dict[str, str]:
        """Generate Node-RED node package"""
        logger.info(f"Generating Node-RED node for {profile.device_info.product_name}")

        safe_name = self._make_safe_name(profile.device_info.product_name)

        return {
            'package.json': self._generate_package_json(profile, safe_name),
            f'{safe_name}.js': self._generate_node_js(profile, safe_name),
            f'{safe_name}.html': self._generate_node_html(profile, safe_name),
            'README.md': self._generate_readme(profile, safe_name)
        }

    def _make_safe_name(self, name: str) -> str:
        """Convert name to safe identifier"""
        import re
        safe = re.sub(r'[^a-zA-Z0-9]', '-', name.lower())
        safe = re.sub(r'-+', '-', safe).strip('-')
        return safe

    def _generate_package_json(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate package.json for Node-RED node"""
        package = {
            "name": f"node-red-contrib-{safe_name}",
            "version": "1.0.0",
            "description": f"Node-RED node for {profile.device_info.product_name} IO-Link device",
            "keywords": ["node-red", "io-link", profile.vendor_info.name, safe_name],
            "node-red": {
                "nodes": {
                    safe_name: f"{safe_name}.js"
                }
            },
            "author": "Greenstack",
            "license": "MIT"
        }
        return json.dumps(package, indent=2)

    def _generate_node_js(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate Node.js code for the node"""
        template = Template("""
module.exports = function(RED) {
    function {{ node_name }}Node(config) {
        RED.nodes.createNode(this, config);
        var node = this;

        // Configuration
        this.deviceId = {{ device_id }};
        this.vendorId = {{ vendor_id }};
        this.productName = "{{ product_name }}";

        // Parameters
        {% for param in parameters %}
        this.param_{{ param.name | replace(' ', '_') }} = config.param_{{ param.name | replace(' ', '_') }};
        {% endfor %}

        // Process Data Configuration
        this.processDataIn = {
            totalBits: {{ process_data.total_input_bits }},
            data: [
                {% for pd in process_data.inputs %}
                { index: {{ pd.index }}, name: "{{ pd.name }}", bits: {{ pd.bit_length }} },
                {% endfor %}
            ]
        };

        this.processDataOut = {
            totalBits: {{ process_data.total_output_bits }},
            data: [
                {% for pd in process_data.outputs %}
                { index: {{ pd.index }}, name: "{{ pd.name }}", bits: {{ pd.bit_length }} },
                {% endfor %}
            ]
        };

        // Handle input messages
        node.on('input', function(msg) {
            try {
                // Parse IO-Link communication
                if (msg.topic === 'read') {
                    // Read parameter
                    var paramIndex = msg.payload.index;
                    // TODO: Implement IO-Link read
                    node.send({
                        payload: {
                            index: paramIndex,
                            value: 0 // Placeholder
                        }
                    });
                } else if (msg.topic === 'write') {
                    // Write parameter
                    var paramIndex = msg.payload.index;
                    var value = msg.payload.value;
                    // TODO: Implement IO-Link write
                    node.send({
                        payload: {
                            index: paramIndex,
                            value: value,
                            status: 'written'
                        }
                    });
                } else if (msg.topic === 'processdata') {
                    // Handle process data
                    // TODO: Implement process data handling
                    node.send({
                        payload: {
                            inputs: node.processDataIn,
                            outputs: node.processDataOut
                        }
                    });
                }

                node.status({fill:"green", shape:"dot", text:"connected"});
            } catch(err) {
                node.error(err);
                node.status({fill:"red", shape:"ring", text:"error"});
            }
        });

        node.on('close', function() {
            // Cleanup
        });
    }

    RED.nodes.registerType("{{ node_name }}", {{ node_name }}Node);
}
""")

        return template.render(
            node_name=safe_name,
            device_id=profile.device_info.device_id,
            vendor_id=profile.device_info.vendor_id,
            product_name=profile.device_info.product_name,
            parameters=profile.parameters[:10],  # Limit to first 10 parameters for simplicity
            process_data=profile.process_data
        )

    def _generate_node_html(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate HTML configuration interface for the node"""
        template = Template("""
<script type="text/javascript">
    RED.nodes.registerType('{{ node_name }}', {
        category: 'IO-Link',
        color: '#3FADB5',
        defaults: {
            name: {value: ""},
            {% for param in parameters %}
            {% if param.access_rights.value in ['rw', 'wo'] %}
            param_{{ param.name | replace(' ', '_') }}: {value: "{{ param.default_value or '' }}"},
            {% endif %}
            {% endfor %}
        },
        inputs: 1,
        outputs: 1,
        icon: "serial.png",
        label: function() {
            return this.name || "{{ product_name }}";
        },
        paletteLabel: "{{ product_name }}"
    });
</script>

<script type="text/x-red" data-template-name="{{ node_name }}">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>

    <h4>Device Information</h4>
    <div class="form-row">
        <label>Product:</label>
        <span>{{ product_name }}</span>
    </div>
    <div class="form-row">
        <label>Vendor:</label>
        <span>{{ vendor_name }}</span>
    </div>
    <div class="form-row">
        <label>Device ID:</label>
        <span>{{ device_id }}</span>
    </div>

    <h4>Configurable Parameters</h4>
    {% for param in parameters %}
    {% if param.access_rights.value in ['rw', 'wo'] %}
    <div class="form-row">
        <label for="node-input-param_{{ param.name | replace(' ', '_') }}">
            <i class="fa fa-cog"></i> {{ param.name }}
        </label>
        <input type="text" id="node-input-param_{{ param.name | replace(' ', '_') }}"
               placeholder="{{ param.default_value or '' }}">
        {% if param.description %}
        <div class="form-tips">{{ param.description }}</div>
        {% endif %}
    </div>
    {% endif %}
    {% endfor %}
</script>

<script type="text/x-red" data-help-name="{{ node_name }}">
    <p>Node-RED node for {{ product_name }} IO-Link device.</p>

    <h3>Inputs</h3>
    <dl class="message-properties">
        <dt>topic <span class="property-type">string</span></dt>
        <dd>Command type: "read", "write", or "processdata"</dd>
        <dt>payload <span class="property-type">object</span></dt>
        <dd>Command parameters (index, value)</dd>
    </dl>

    <h3>Outputs</h3>
    <dl class="message-properties">
        <dt>payload <span class="property-type">object</span></dt>
        <dd>Response data from the device</dd>
    </dl>

    <h3>Device Parameters</h3>
    <ul>
    {% for param in parameters %}
        <li><b>{{ param.name }}</b> (Index: {{ param.index }}, Type: {{ param.data_type.value }}, Access: {{ param.access_rights.value }})</li>
    {% endfor %}
    </ul>

    <h3>Process Data</h3>
    <p>Input: {{ process_data.total_input_bits }} bits</p>
    <p>Output: {{ process_data.total_output_bits }} bits</p>
</script>
""")

        return template.render(
            node_name=safe_name,
            product_name=profile.device_info.product_name,
            vendor_name=profile.vendor_info.name,
            device_id=profile.device_info.device_id,
            parameters=profile.parameters[:10],  # Limit for UI simplicity
            process_data=profile.process_data
        )

    def _generate_readme(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate README.md for the node package"""
        template = Template("""
# node-red-contrib-{{ safe_name }}

Node-RED node for {{ product_name }} IO-Link device.

## Installation

```bash
npm install node-red-contrib-{{ safe_name }}
```

## Device Information

- **Product**: {{ product_name }}
- **Vendor**: {{ vendor_name }}
- **Vendor ID**: {{ vendor_id }}
- **Device ID**: {{ device_id }}
- **IODD Version**: {{ iodd_version }}

## Usage

This node provides access to the {{ product_name }} IO-Link device parameters and process data.

### Supported Operations

1. **Read Parameter**: Send a message with `topic: "read"` and `payload.index: <parameter_index>`
2. **Write Parameter**: Send a message with `topic: "write"`, `payload.index: <parameter_index>` and `payload.value: <value>`
3. **Process Data**: Send a message with `topic: "processdata"` to get current process data configuration

## Parameters

The device supports {{ param_count }} parameters with various access rights.

## Process Data

- **Input**: {{ input_bits }} bits
- **Output**: {{ output_bits }} bits

## License

MIT
""")

        return template.render(
            safe_name=safe_name,
            product_name=profile.device_info.product_name,
            vendor_name=profile.vendor_info.name,
            vendor_id=profile.device_info.vendor_id,
            device_id=profile.device_info.device_id,
            iodd_version=profile.iodd_version,
            param_count=len(profile.parameters),
            input_bits=profile.process_data.total_input_bits,
            output_bits=profile.process_data.total_output_bits
        )


# Import flow generators
from src.generation.nodered_flows import (
    NodeREDFlowGenerator,
    generate_monitoring_flow,
    generate_control_flow
)

__all__ = [
    'AdapterGenerator',
    'NodeREDGenerator',
    'NodeREDFlowGenerator',
    'generate_monitoring_flow',
    'generate_control_flow'
]
