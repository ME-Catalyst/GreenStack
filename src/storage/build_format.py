"""
IODD Build Format storage handler

Extracts and stores formatting metadata from original IODD files to enable
accurate reconstruction that preserves whitespace and formatting style.
"""

import logging
import re
from datetime import datetime
from typing import Optional, Dict
from .base import BaseSaver

logger = logging.getLogger(__name__)


class BuildFormatSaver(BaseSaver):
    """Handles extraction and storage of IODD formatting metadata"""

    def save(self, device_id: int, data) -> None:
        """Required by BaseSaver interface - delegates to extract_and_save"""
        if data:
            self.extract_and_save(device_id, data)

    def extract_and_save(self, device_id: int, xml_content: str) -> None:
        """
        Extract formatting metadata from IODD XML and save to database

        Args:
            device_id: Database ID of the device
            xml_content: Original raw XML content (as string)
        """
        format_info = self._extract_format_info(xml_content)

        # Delete existing format info for this device
        self._delete_existing('iodd_build_format', device_id)

        query = """
            INSERT INTO iodd_build_format (
                device_id, indent_char, indent_size, xml_declaration,
                namespace_prefix, schema_location, newline_style,
                has_trailing_newline, attribute_quoting, extracted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        self._execute(query, (
            device_id,
            format_info['indent_char'],
            format_info['indent_size'],
            format_info['xml_declaration'],
            format_info['namespace_prefix'],
            format_info['schema_location'],
            format_info['newline_style'],
            1 if format_info['has_trailing_newline'] else 0,
            format_info['attribute_quoting'],
            datetime.utcnow().isoformat(),
        ))

        logger.info(f"Saved build format metadata for device {device_id}: "
                   f"indent={format_info['indent_char']}x{format_info['indent_size']}, "
                   f"newline={format_info['newline_style']}")

    def _extract_format_info(self, xml_content: str) -> Dict:
        """
        Extract formatting details from raw XML content

        Args:
            xml_content: Original XML content

        Returns:
            Dict with formatting metadata
        """
        result = {
            'indent_char': 'tab',
            'indent_size': 1,
            'xml_declaration': None,
            'namespace_prefix': None,
            'schema_location': None,
            'newline_style': 'lf',
            'has_trailing_newline': True,
            'attribute_quoting': 'double',
        }

        # Detect line ending style
        if '\r\n' in xml_content:
            result['newline_style'] = 'crlf'
        elif '\r' in xml_content and '\n' not in xml_content:
            result['newline_style'] = 'cr'
        else:
            result['newline_style'] = 'lf'

        # Extract XML declaration
        xml_decl_match = re.match(r'^(<\?xml[^?]*\?>)', xml_content, re.IGNORECASE)
        if xml_decl_match:
            result['xml_declaration'] = xml_decl_match.group(1)

        # Detect indentation style by looking at first indented line
        lines = xml_content.split('\n')
        for line in lines[1:]:  # Skip first line (usually XML declaration or root)
            if line and line[0] in ' \t':
                # Found an indented line
                indent = ''
                for char in line:
                    if char in ' \t':
                        indent += char
                    else:
                        break

                if '\t' in indent:
                    result['indent_char'] = 'tab'
                    result['indent_size'] = indent.count('\t')
                elif ' ' in indent:
                    result['indent_char'] = 'space'
                    result['indent_size'] = len(indent)
                break

        # Extract namespace prefix
        ns_prefix_match = re.search(r'<(\w+):IODevice\b', xml_content)
        if ns_prefix_match:
            result['namespace_prefix'] = ns_prefix_match.group(1) + ':'
        elif '<IODevice' in xml_content:
            result['namespace_prefix'] = ''  # Default namespace

        # Extract schema location
        schema_match = re.search(r'schemaLocation\s*=\s*["\']([^"\']+)["\']', xml_content)
        if schema_match:
            result['schema_location'] = schema_match.group(1)

        # Detect attribute quoting style
        if "='" in xml_content and '="' not in xml_content:
            result['attribute_quoting'] = 'single'
        else:
            result['attribute_quoting'] = 'double'

        # Check for trailing newline
        result['has_trailing_newline'] = xml_content.endswith('\n') or xml_content.endswith('\r')

        return result

    def get_format(self, device_id: int) -> Optional[Dict]:
        """
        Retrieve stored format metadata for a device

        Args:
            device_id: Database ID of the device

        Returns:
            Dict with format info or None if not found
        """
        cursor = self._get_cursor()
        cursor.execute("""
            SELECT indent_char, indent_size, xml_declaration, namespace_prefix,
                   schema_location, newline_style, has_trailing_newline, attribute_quoting
            FROM iodd_build_format
            WHERE device_id = ?
        """, (device_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return {
            'indent_char': row['indent_char'],
            'indent_size': row['indent_size'],
            'xml_declaration': row['xml_declaration'],
            'namespace_prefix': row['namespace_prefix'],
            'schema_location': row['schema_location'],
            'newline_style': row['newline_style'],
            'has_trailing_newline': bool(row['has_trailing_newline']),
            'attribute_quoting': row['attribute_quoting'],
        }
