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
  return IOLINK_BITRATES[normalized] || null;
}

/**
 * Profile Characteristics
 * Decode profile characteristics bitfield
 */
export const PROFILE_CHARACTERISTICS = {
  0x01: 'ISDU Communication',
  0x02: 'Process Data',
  0x04: 'Diagnosis',
  0x08: 'Events',
  0x10: 'Configuration',
  0x20: 'Parameter Server',
  0x40: 'Condition Monitoring',
  0x80: 'Reserved'
};

/**
 * Decode profile characteristics bitfield
 * @param {number} value - Bitfield value
 * @returns {string[]} Array of supported characteristics
 */
export function decodeProfileCharacteristics(value) {
  if (!value) return [];
  const characteristics = [];
  for (const [bit, desc] of Object.entries(PROFILE_CHARACTERISTICS)) {
    if (value & parseInt(bit)) {
      characteristics.push(desc);
    }
  }
  return characteristics;
}

/**
 * Wire Color Codes
 * Standard IO-Link wire color assignments
 */
export const WIRE_COLORS = {
  1: { color: 'Brown', signal: 'L+', description: 'Power Supply +24V' },
  2: { color: 'White', signal: 'C/Q', description: 'Communication/DI' },
  3: { color: 'Blue', signal: 'L-', description: 'Ground 0V' },
  4: { color: 'Black', signal: 'C/Q', description: 'Communication/DO' },
  5: { color: 'Gray', signal: 'NC', description: 'Not Connected' }
};

/**
 * Get wire color information
 * @param {number} pin - Pin number (1-5)
 * @returns {object} Wire color information
 */
export function getWireColorInfo(pin) {
  return WIRE_COLORS[pin] || { color: 'Unknown', signal: '?', description: 'Unknown pin' };
}

/**
 * Format cycle time in microseconds to human-readable
 * @param {number} microseconds - Cycle time in μs
 * @returns {string} Formatted cycle time
 */
export function formatCycleTime(microseconds) {
  if (!microseconds || microseconds === 0) return 'N/A';
  if (microseconds < 1000) return `${microseconds} μs`;
  if (microseconds < 1000000) return `${(microseconds / 1000).toFixed(1)} ms`;
  return `${(microseconds / 1000000).toFixed(2)} s`;
}

/**
 * Access Rights
 * IO-Link parameter access rights
 */
export const ACCESS_RIGHTS = {
  'ro': { display: 'Read Only', description: 'Parameter can only be read', icon: '👁️' },
  'rw': { display: 'Read/Write', description: 'Parameter can be read and written', icon: '✏️' },
  'wo': { display: 'Write Only', description: 'Parameter can only be written', icon: '📝' }
};

/**
 * Get access right information
 * @param {string} right - Access right code (ro, rw, wo)
 * @returns {object} Access right information
 */
export function getAccessRightInfo(right) {
  if (!right) return { display: 'Unknown', description: 'Unknown access right', icon: '❓' };
  const normalized = right.toLowerCase();
  return ACCESS_RIGHTS[normalized] || { display: right, description: 'Custom access right', icon: '?' };
}

/**
 * Data Types
 * IO-Link data type definitions
 */
export const DATA_TYPES = {
  'UIntegerT': { display: 'Unsigned Integer', size: 'Variable', description: 'Unsigned integer value' },
  'IntegerT': { display: 'Signed Integer', size: 'Variable', description: 'Signed integer value' },
  'BooleanT': { display: 'Boolean', size: '1 bit', description: 'True/false value' },
  'Float32T': { display: 'Float32', size: '32 bits', description: '32-bit floating point' },
  'OctetStringT': { display: 'Octet String', size: 'Variable', description: 'Byte array' },
  'StringT': { display: 'String', size: 'Variable', description: 'Text string' },
  'TimeT': { display: 'Time', size: '32 bits', description: 'Time value' },
  'TimeSpanT': { display: 'TimeSpan', size: '32 bits', description: 'Duration value' },
  'RecordT': { display: 'Record', size: 'Variable', description: 'Structured data' },
  'ArrayT': { display: 'Array', size: 'Variable', description: 'Array of values' }
};

/**
 * Get data type display information
 * @param {string} dataType - Data type identifier
 * @returns {object} Data type information
 */
export function getDataTypeDisplay(dataType) {
  if (!dataType) return { display: 'Unknown', size: '?', description: 'Unknown data type' };
  return DATA_TYPES[dataType] || { display: dataType, size: '?', description: 'Custom data type' };
}

/**
 * M-Sequence Capability
 * Master-Sequence types for cyclic communication
 */
export const M_SEQUENCES = {
  0: 'TYPE_0 (Reserved)',
  1: 'TYPE_1_1 (1 byte PD in/out)',
  2: 'TYPE_1_2 (2 bytes PD in/out)',
  17: 'TYPE_1_V (Variable PD length)',
  18: 'TYPE_2_1 (Isdu capable, 1 byte PD)',
  19: 'TYPE_2_2 (Isdu capable, 2 bytes PD)',
  33: 'TYPE_2_V (Isdu capable, variable PD)'
};

/**
 * Decode M-Sequence capability
 * @param {number} value - M-Sequence type value
 * @returns {string} M-Sequence description
 */
export function decodeMSequence(value) {
  return M_SEQUENCES[value] || `Unknown M-Sequence (${value})`;
}

/**
 * Connection Types
 * Physical connection interface types
 */
export const CONNECTION_TYPES = {
  'M12': { display: 'M12 Connector', pins: [3, 4, 5, 8, 12], description: 'M12 circular connector' },
  'M8': { display: 'M8 Connector', pins: [3, 4], description: 'M8 circular connector' },
  'Cable': { display: 'Cable Connection', pins: [], description: 'Direct cable connection' },
  '7/8"': { display: '7/8" Connector', pins: [3, 4, 5], description: '7/8 inch circular connector' }
};

/**
 * Get connection type information
 * @param {string} type - Connection type identifier
 * @returns {object} Connection type information
 */
export function getConnectionTypeInfo(type) {
  if (!type) return { display: 'Unknown', pins: [], description: 'Unknown connection type' };
  return CONNECTION_TYPES[type] || { display: type, pins: [], description: 'Custom connection type' };
}