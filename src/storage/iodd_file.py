"""
IODD File storage handler

Manages IODD XML file content and metadata.
"""

import logging
from .base import BaseSaver

logger = logging.getLogger(__name__)


class IODDFileSaver(BaseSaver):
    """Handles IODD file storage"""

    def save(self, device_id: int, profile) -> None:
        """
        Save IODD file content and metadata

        Args:
            device_id: Database ID of the device
            profile: DeviceProfile object with raw XML and metadata
        """
        # Delete existing
        self._delete_existing('iodd_files', device_id)

        # Save IODD file content
        query = """
            INSERT INTO iodd_files (
                device_id, file_name, xml_content, schema_version,
                stamp_crc, checker_name, checker_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        file_name = f"{getattr(profile.device_info, 'product_name', 'device')}.xml"

        params = (
            device_id,
            file_name,
            getattr(profile, 'raw_xml', None),
            getattr(profile, 'schema_version', None),
            getattr(profile, 'stamp_crc', None),
            getattr(profile, 'checker_name', None),
            getattr(profile, 'checker_version', None),
        )

        self._execute(query, params)
        logger.info(f"Saved IODD file for device {device_id}")
