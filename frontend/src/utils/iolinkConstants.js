/**
 * IO-Link Constants and Decoders
 *
 * Provides translation utilities for IO-Link specification constants
 * including bitrates, profile characteristics, wire colors, and more
 */

/**
 * IO-Link Communication Bitrates
 * COM1, COM2, COM3 standard rates
 */
export const IOLINK_BITRATES = {
  'COM1': { rate: 4800, unit: 'bps', display: '4.8 kbps', description: 'COM1 - 4.8 kbit/s' },
  'COM2': { rate: 38400, unit: 'bps', display: '38.4 kbps', description: 'COM2 - 38.4 kbit/s' },
  'COM3': { rate: 230400, unit: 'bps', display: '230.4 kbps', description: 'COM3 - 230.4 kbit/s' },
};

/**
 * Translate COM bitrate to human-readable format
 * @param {string} comRate - COM1, COM2, or COM3
 * @returns {string} Human-readable bitrate
 */
export function translateBitrate(comRate) {
  if (!comRate) return 'Unknown';
  const normalized = comRate.toUpperCase();
  const bitrate = IOLINK_BITRATES[normalized];
  return bitrate ? bitrate.display : comRate;
}

/**
 * Get full bitrate info
 * @param {string} comRate - COM1, COM2, or COM3
 * @returns {object} Bitrate information
 */
export function getBitrateInfo(comRate) {
  if (!comRate) return null;
  const normalized = comRate.toUpperCase();
  return IOLINK_BITRATES[normalized] || { rate: 0, unit: 'bps', display: comRate, description: comRate };
}

/**
 * IO-Link Profile Characteristics
 * Decodes profile characteristic bit flags
 */
export const PROFILE_CHARACTERISTICS = {
  1: { name: 'Smart Sensor Profile', description: 'Device supports Smart Sensor Profile' },
  2: { name: 'Device Access Locks', description: 'Device supports access lock mechanism' },
  4: { name: 'DI/DO Function', description: 'Device supports digital input/output switching' },
  8: { name: 'NFC', description: 'Device has NFC interface' },
  16: { name: 'AutoComm', description: 'Device supports automatic communication mode switching' },
  32: { name: 'Measurement Value Scaling', description: 'Device supports measurement value scaling' },
  49: { name: 'Firmware Update', description: 'Device supports firmware updates via IO-Link' },
  64: { name: 'Condition Monitoring', description: 'Device provides condition monitoring data' },
  128: { name: 'Energy Saving Mode', description: 'Device supports energy saving modes' },
  256: { name: 'Multi-Sensor', description: 'Device has multiple integrated sensors' },
  512: { name: 'iQ-Sensor', description: 'SICK iQ-Sensor profile' },
  1024: { name: 'Safety Profile', description: 'Device supports safety functions' },
  2048: { name: 'IO-Link Wireless', description: 'Device supports wireless IO-Link' },
  4096: { name: 'OPC UA Companion Spec', description: 'Device supports OPC UA companion specification' },
  8192: { name: 'Asset Management', description: 'Device provides asset management data' },
  16384: { name: 'Identification & Diagnosis', description: 'Enhanced identification and diagnostic features' },
  32768: { name: 'Reserved', description: 'Reserved for future use' },
};

/**
 * Decode profile characteristics bit field
 * @param {number|string} characteristics - Bit field or space-separated values
 * @returns {array} Array of characteristic objects
 */
export function decodeProfileCharacteristics(characteristics) {
  if (!characteristics) return [];

  // Handle space-separated values (e.g., "49 16384")
  if (typeof characteristics === 'string') {
    return characteristics.split(/\s+/).map(num => {
      const code = parseInt(num);
      const char = PROFILE_CHARACTERISTICS[code];
      return char ? { code, ...char } : { code, name: `Unknown (${code})`, description: 'Unknown profile characteristic' };
    });
  }

  // Handle bit field
  const result = [];
  Object.entries(PROFILE_CHARACTERISTICS).forEach(([bit, info]) => {
    const bitValue = parseInt(bit);
    if (characteristics & bitValue) {
      result.push({ code: bitValue, ...info });
    }
  });

  return result;
}

/**
 * IO-Link Wire Colors (M12 connectors)
 * Standard color codes for M12 5-pin and 8-pin connectors
 */
export const WIRE_COLORS = {
  'BN': { name: 'Brown', hex: '#8B4513', function: 'L+ (Supply voltage positive)' },
  'WH': { name: 'White', hex: '#FFFFFF', function: 'Optional/Other' },
  'BU': { name: 'Blue', hex: '#0000FF', function: 'L- (Supply voltage negative)' },
  'BK': { name: 'Black', hex: '#000000', function: 'C/Q (Communication line / Switching output)' },
  'GY': { name: 'Gray', hex: '#808080', function: 'NC (Not connected) or optional' },
  'PK': { name: 'Pink', hex: '#FFC0CB', function: 'Optional/Other' },
  'YE': { name: 'Yellow', hex: '#FFFF00', function: 'Optional/Other' },
  'GN': { name: 'Green', hex: '#008000', function: 'PE (Protective earth)' },
  'RD': { name: 'Red', hex: '#FF0000', function: 'Optional/Other' },
  'VT': { name: 'Violet', hex: '#8B00FF', function: 'Optional/Other' },
};

/**
 * Get wire color information
 * @param {string} colorCode - Two-letter color code (e.g., 'BN', 'WH')
 * @returns {object} Color information
 */
export function getWireColorInfo(colorCode) {
  if (!colorCode) return null;
  const normalized = colorCode.toUpperCase();
  return WIRE_COLORS[normalized] || { name: colorCode, hex: '#CCCCCC', function: 'Unknown' };
}

/**
 * IO-Link Access Rights
 */
export const ACCESS_RIGHTS = {
  'ro': { label: 'Read Only', description: 'Parameter can only be read', icon: '🔒', color: 'blue' },
  'wo': { label: 'Write Only', description: 'Parameter can only be written', icon: '✏️', color: 'orange' },
  'rw': { label: 'Read/Write', description: 'Parameter can be read and written', icon: '🔓', color: 'green' },
};

/**
 * Get access rights information
 * @param {string} accessRight - Access right code ('ro', 'wo', 'rw')
 * @returns {object} Access rights information
 */
export function getAccessRightInfo(accessRight) {
  if (!accessRight) return null;
  const normalized = accessRight.toLowerCase();
  return ACCESS_RIGHTS[normalized] || { label: accessRight, description: 'Unknown access right', icon: '❓', color: 'gray' };
}

/**
 * IO-Link Data Types
 */
export const DATA_TYPES = {
  'BooleanT': { display: 'Boolean', description: 'True/False value', size: 1 },
  'IntegerT': { display: 'Integer', description: 'Signed integer', size: 'variable' },
  'UIntegerT': { display: 'Unsigned Integer', description: 'Unsigned integer', size: 'variable' },
  'Float32T': { display: 'Float', description: '32-bit floating point', size: 32 },
  'StringT': { display: 'String', description: 'Text string', size: 'variable' },
  'OctetStringT': { display: 'Octet String', description: 'Binary data', size: 'variable' },
  'TimeT': { display: 'Time', description: 'Time value', size: 'variable' },
  'RecordT': { display: 'Record', description: 'Structured data', size: 'variable' },
  'ArrayT': { display: 'Array', description: 'Array of values', size: 'variable' },
};

/**
 * Get data type display name
 * @param {string} dataType - IO-Link data type
 * @returns {string} Human-readable data type
 */
export function getDataTypeDisplay(dataType) {
  if (!dataType) return 'Unknown';
  const type = DATA_TYPES[dataType];
  return type ? type.display : dataType;
}

/**
 * Connection Types (M12, M8, etc.)
 */
export const CONNECTION_TYPES = {
  'M12-4': { pins: 4, type: 'M12', description: 'M12 4-pin connector (A-coded)' },
  'M12-5': { pins: 5, type: 'M12', description: 'M12 5-pin connector (B-coded for fieldbus)' },
  'M12-8': { pins: 8, type: 'M12', description: 'M12 8-pin connector' },
  'M8-3': { pins: 3, type: 'M8', description: 'M8 3-pin connector' },
  'M8-4': { pins: 4, type: 'M8', description: 'M8 4-pin connector' },
  '7/8"': { pins: 5, type: '7/8"', description: '7/8" connector' },
};

/**
 * Get connection type info
 * @param {string} connectionType - Connection type string
 * @returns {object} Connection information
 */
export function getConnectionTypeInfo(connectionType) {
  if (!connectionType) return null;
  return CONNECTION_TYPES[connectionType] || { pins: 0, type: connectionType, description: connectionType };
}

/**
 * SIO Mode Functions
 */
export const SIO_MODES = {
  'SIO_DI': 'Digital Input',
  'SIO_DO': 'Digital Output',
  'SIO_INOUT': 'Input/Output',
  'NC': 'Not Connected'
};

/**
 * Get SIO mode display name
 * @param {string} sioMode - SIO mode code
 * @returns {string} Human-readable SIO mode
 */
export function getSIOModeDisplay(sioMode) {
  return SIO_MODES[sioMode] || sioMode;
}

/**
 * Format cycle time (microseconds to milliseconds)
 * @param {number} microseconds - Time in microseconds
 * @returns {string} Formatted time string
 */
export function formatCycleTime(microseconds) {
  if (!microseconds) return 'N/A';
  const ms = microseconds / 1000;
  if (ms < 1) return `${microseconds} µs`;
  if (ms < 1000) return `${ms.toFixed(1)} ms`;
  return `${(ms / 1000).toFixed(2)} s`;
}

/**
 * Decode M-Sequence capability
 * @param {number} mSequence - M-Sequence value (number of bytes)
 * @returns {string} Description
 */
export function decodeMSequence(mSequence) {
  if (!mSequence) return 'Not specified';
  if (mSequence <= 8) return `${mSequence} bytes (minimum)`;
  if (mSequence <= 32) return `${mSequence} bytes (standard)`;
  return `${mSequence} bytes (extended)`;
}

export default {
  IOLINK_BITRATES,
  PROFILE_CHARACTERISTICS,
  WIRE_COLORS,
  ACCESS_RIGHTS,
  DATA_TYPES,
  CONNECTION_TYPES,
  SIO_MODES,
  translateBitrate,
  getBitrateInfo,
  decodeProfileCharacteristics,
  getWireColorInfo,
  getAccessRightInfo,
  getDataTypeDisplay,
  getConnectionTypeInfo,
  getSIOModeDisplay,
  formatCycleTime,
  decodeMSequence
};
