import re

file_path = r'F:\github\GreenStack\frontend\src\content\docs\user-guide\Features.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the line about incomplete EDS revision comparison
old_text = '''              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• User authentication and authorization</li>
                <li>• Multi-user support with permissions</li>
                <li>• Real-time device connectivity (IO-Link, EtherNet/IP)</li>
                <li>• Live telemetry monitoring</li>
                <li>• MQTT broker integration</li>
                <li>• Advanced rate limiting (use reverse proxy)</li>
                <li>• EDS revision comparison (toggle exists but incomplete)</li>
              </ul>'''

new_text = '''              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• User authentication and authorization</li>
                <li>• Multi-user support with permissions</li>
                <li>• Real-time device connectivity (IO-Link, EtherNet/IP)</li>
                <li>• Live telemetry monitoring</li>
                <li>• MQTT broker integration</li>
                <li>• Advanced rate limiting (use reverse proxy)</li>
              </ul>'''

if old_text in content:
    content = content.replace(old_text, new_text)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print('[OK] Removed outdated EDS revision comparison line from Features.jsx')
else:
    print('[INFO] Line not found - may have already been updated')
