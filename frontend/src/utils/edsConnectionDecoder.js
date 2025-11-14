/**
 * EDS Connection Decoder Utility
 *
 * Decodes EtherNet/IP connection hex values into human-readable descriptions
 * based on ODVA CIP specification.
 */

/**
 * Decode Trigger/Transport field (Connection1 line 1)
 * Format: 0xXXXXXXXX
 * Bits 0-15: Supported transport classes
 * Bits 16-23: Trigger types
 * Bits 24-27: Application types
 * Bit 31: Direction (Client=0, Server=1)
 */
export function decodeTriggerTransport(hexValue) {
  if (!hexValue) return null;

  const value = parseInt(hexValue, 16);

  return {
    rawValue: hexValue,
    transportClasses: {
      label: 'Transport Classes',
      bits: '0-15',
      value: value & 0xFFFF,
      hex: `0x${(value & 0xFFFF).toString(16).toUpperCase().padStart(4, '0')}`,
      description: getTransportClassesDescription(value & 0xFFFF)
    },
    triggers: {
      label: 'Trigger Types',
      bits: '16-23',
      cyclic: Boolean(value & (1 << 16)),
      changeOfState: Boolean(value & (1 << 17)),
      application: Boolean(value & (1 << 18)),
      description: getTriggerTypesDescription(value)
    },
    applicationTypes: {
      label: 'Application Types',
      bits: '24-27',
      listenOnly: Boolean(value & (1 << 24)),
      inputOnly: Boolean(value & (1 << 25)),
      exclusiveOwner: Boolean(value & (1 << 26)),
      redundantOwner: Boolean(value & (1 << 27)),
      description: getApplicationTypesDescription(value)
    },
    direction: {
      label: 'Direction',
      bit: '31',
      isServer: Boolean(value & (1 << 31)),
      description: (value & (1 << 31)) ? 'Server' : 'Client'
    }
  };
}

/**
 * Decode Connection Parameters field (Connection1 line 2)
 * Format: 0xXXXXXXXX
 * Bits 0-3: Size support flags
 * Bits 8-14: Real-time transfer format
 * Bits 16-23: Connection types
 * Bits 24-31: Priority levels
 */
export function decodeConnectionParams(hexValue) {
  if (!hexValue) return null;

  const value = parseInt(hexValue, 16);

  return {
    rawValue: hexValue,
    sizeSupport: {
      label: 'Size Support',
      bits: '0-3',
      oToTFixed: Boolean(value & (1 << 0)),
      oToTVariable: Boolean(value & (1 << 1)),
      tToOFixed: Boolean(value & (1 << 2)),
      tToOVariable: Boolean(value & (1 << 3)),
      description: getSizeSupportDescription(value)
    },
    realTimeFormat: {
      label: 'Real-Time Format',
      bits: '8-14',
      oToT: (value >> 8) & 0x7,
      tToO: (value >> 12) & 0x7,
      description: getRealTimeFormatDescription(value)
    },
    connectionTypes: {
      label: 'Connection Types',
      bits: '16-23',
      oToT: {
        null: Boolean(value & (1 << 16)),
        multicast: Boolean(value & (1 << 17)),
        pointToPoint: Boolean(value & (1 << 18))
      },
      tToO: {
        null: Boolean(value & (1 << 20)),
        multicast: Boolean(value & (1 << 21)),
        pointToPoint: Boolean(value & (1 << 22))
      },
      description: getConnectionTypesDescription(value)
    },
    priority: {
      label: 'Priority Levels',
      bits: '24-31',
      oToT: {
        low: Boolean(value & (1 << 24)),
        high: Boolean(value & (1 << 25)),
        scheduled: Boolean(value & (1 << 26))
      },
      tToO: {
        low: Boolean(value & (1 << 28)),
        high: Boolean(value & (1 << 29)),
        scheduled: Boolean(value & (1 << 30))
      },
      description: getPriorityDescription(value)
    }
  };
}

// Helper functions for descriptions

function getTransportClassesDescription(value) {
  const classes = [];
  if (value & 0x0001) classes.push('Class 0 (I/O)');
  if (value & 0x0002) classes.push('Class 1 (Explicit Messaging)');
  if (value & 0x0004) classes.push('Class 2');
  if (value & 0x0008) classes.push('Class 3');
  return classes.length > 0 ? classes.join(', ') : 'None';
}

function getTriggerTypesDescription(value) {
  const triggers = [];
  if (value & (1 << 16)) triggers.push('Cyclic');
  if (value & (1 << 17)) triggers.push('Change of State');
  if (value & (1 << 18)) triggers.push('Application');
  return triggers.length > 0 ? triggers.join(', ') : 'None';
}

function getApplicationTypesDescription(value) {
  const types = [];
  if (value & (1 << 24)) types.push('Listen-Only');
  if (value & (1 << 25)) types.push('Input-Only');
  if (value & (1 << 26)) types.push('Exclusive Owner');
  if (value & (1 << 27)) types.push('Redundant Owner');
  return types.length > 0 ? types.join(', ') : 'None';
}

function getSizeSupportDescription(value) {
  const support = [];
  if (value & (1 << 0)) support.push('O→T Fixed');
  if (value & (1 << 1)) support.push('O→T Variable');
  if (value & (1 << 2)) support.push('T→O Fixed');
  if (value & (1 << 3)) support.push('T→O Variable');
  return support.length > 0 ? support.join(', ') : 'None';
}

function getRealTimeFormatDescription(value) {
  const oToTFormat = (value >> 8) & 0x7;
  const tToOFormat = (value >> 12) & 0x7;

  const formatNames = ['Modeless', '32-bit Header', 'Heartbeat', 'Reserved3', 'Reserved4', 'Reserved5', 'Reserved6', 'Reserved7'];

  return `O→T: ${formatNames[oToTFormat]}, T→O: ${formatNames[tToOFormat]}`;
}

function getConnectionTypesDescription(value) {
  const oToT = [];
  const tToO = [];

  if (value & (1 << 16)) oToT.push('NULL');
  if (value & (1 << 17)) oToT.push('Multicast');
  if (value & (1 << 18)) oToT.push('Point-to-Point');

  if (value & (1 << 20)) tToO.push('NULL');
  if (value & (1 << 21)) tToO.push('Multicast');
  if (value & (1 << 22)) tToO.push('Point-to-Point');

  return `O→T: ${oToT.join('/')}, T→O: ${tToO.join('/')}`;
}

function getPriorityDescription(value) {
  const oToT = [];
  const tToO = [];

  if (value & (1 << 24)) oToT.push('Low');
  if (value & (1 << 25)) oToT.push('High');
  if (value & (1 << 26)) oToT.push('Scheduled');

  if (value & (1 << 28)) tToO.push('Low');
  if (value & (1 << 29)) tToO.push('High');
  if (value & (1 << 30)) tToO.push('Scheduled');

  return `O→T: ${oToT.join('/')}, T→O: ${tToO.join('/')}`;
}

/**
 * Get a summary description for a connection
 */
export function getConnectionSummary(triggerTransport, connectionParams) {
  const trigger = decodeTriggerTransport(triggerTransport);
  const params = decodeConnectionParams(connectionParams);

  if (!trigger || !params) return 'Unknown connection type';

  const summary = [];

  // Application type
  if (trigger.applicationTypes.exclusiveOwner) {
    summary.push('Exclusive Owner');
  } else if (trigger.applicationTypes.inputOnly) {
    summary.push('Input Only');
  } else if (trigger.applicationTypes.listenOnly) {
    summary.push('Listen Only');
  } else if (trigger.applicationTypes.redundantOwner) {
    summary.push('Redundant Owner');
  }

  // Trigger type
  if (trigger.triggers.cyclic) {
    summary.push('Cyclic');
  } else if (trigger.triggers.changeOfState) {
    summary.push('Change of State');
  } else if (trigger.triggers.application) {
    summary.push('Application Triggered');
  }

  // Connection type
  if (params.connectionTypes.oToT.multicast || params.connectionTypes.tToO.multicast) {
    summary.push('Multicast');
  } else if (params.connectionTypes.oToT.pointToPoint || params.connectionTypes.tToO.pointToPoint) {
    summary.push('Point-to-Point');
  }

  return summary.join(' • ');
}
