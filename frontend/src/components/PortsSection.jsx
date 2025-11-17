import React, { useState, useEffect } from 'react';
import { Wifi, AlertCircle, Loader2, Network, Link, Box, Settings, Info, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui';
import { Badge } from './ui';
import { Button } from './ui';
import axios from 'axios';

/**
 * Ports Section Component
 * Intelligently displays port definitions for an EDS file:
 * - Explicit [Port] definitions from EDS
 * - Inferred ports from assemblies (IO-Link, channels)
 * - Port-related parameters and configuration
 */
const PortsSection = ({ edsId }) => {
  const [portsData, setPortsData] = useState({
    explicit_ports: [],
    explicit_port_count: 0,
    inferred_ports: [],
    inferred_port_count: 0,
    port_parameters: [],
    port_parameter_count: 0,
    has_port_data: false
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!edsId) return;

    const fetchPorts = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/eds/${edsId}/ports`);
        setPortsData(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch ports:', err);
        setError('Failed to load ports');
      } finally {
        setLoading(false);
      }
    };

    fetchPorts();
  }, [edsId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-6 h-6 animate-spin text-brand-green" />
        <span className="ml-2 text-muted-foreground">Loading ports...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center p-8 text-error">
        <AlertCircle className="w-5 h-5 mr-2" />
        {error}
      </div>
    );
  }

  // Enhanced empty state - show helpful message when no explicit ports but has other data
  if (portsData.explicit_port_count === 0 && !portsData.has_port_data) {
    return (
      <div className="text-center p-8 text-muted-foreground">
        <Network className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p className="text-lg font-medium text-foreground mb-2">No Port Definitions Found</p>
        <p className="text-sm">
          This EDS file does not contain explicit [Port] section definitions.
        </p>
        <p className="text-sm mt-2">
          Ports define communication interfaces like TCP, Ethernet, and other network protocols.
        </p>
      </div>
    );
  }

  // Group explicit ports by type
  const portsByType = portsData.explicit_ports.reduce((acc, port) => {
    const type = port.port_type || 'Unknown';
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push(port);
    return acc;
  }, {});

  const getPortTypeColor = (portType) => {
    const type = (portType || '').toLowerCase();
    if (type.includes('tcp') || type.includes('ethernet')) return 'brand-green';
    if (type.includes('udp')) return 'accent';
    if (type.includes('serial')) return 'success';
    if (type.includes('can')) return 'warning';
    return 'muted';
  };

  const getPortTypeIcon = (portType) => {
    const type = (portType || '').toLowerCase();
    if (type.includes('tcp') || type.includes('ethernet') || type.includes('udp')) {
      return <Wifi className="w-5 h-5" />;
    }
    if (type.includes('link')) {
      return <Link className="w-5 h-5" />;
    }
    return <Network className="w-5 h-5" />;
  };

  return (
    <div className="space-y-6">
      {/* Explicit Ports Section */}
      {portsData.explicit_port_count > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
            <Network className="w-5 h-5 text-brand-green" />
            Explicit Port Definitions ({portsData.explicit_port_count})
          </h2>

          {Object.entries(portsByType).map(([portType, ports]) => {
            const color = getPortTypeColor(portType);
            const icon = getPortTypeIcon(portType);

            return (
              <div key={portType} className="mb-6">
                <div className="flex items-center gap-2 mb-4">
                  <div className={`text-${color}-400`}>
                    {icon}
                  </div>
                  <h3 className="text-lg font-semibold text-foreground">
                    {portType} Ports
                  </h3>
                  <Badge className={`bg-${color}-900/50 text-${color}-300 border-${color}-700`}>
                    {ports.length}
                  </Badge>
                </div>

                <div className="grid gap-4">
                  {ports.map((port) => (
                    <Card
                      key={port.id}
                      className={`bg-card border-border hover:border-${color}/50 transition-colors`}
                    >
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <CardTitle className="text-foreground text-base flex items-center gap-2">
                              <span className={`font-mono text-${color}-300`}>
                                Port {port.port_number}
                              </span>
                              <span className="text-muted-foreground">→</span>
                              <span>{port.port_name}</span>
                            </CardTitle>
                          </div>
                          <Badge
                            variant="outline"
                            className="text-xs text-muted-foreground border-border"
                          >
                            #{port.port_number}
                          </Badge>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <div className="text-xs text-muted-foreground mb-1">Port Type</div>
                            <div className={`font-mono text-${color}-300`}>
                              {port.port_type || 'N/A'}
                            </div>
                          </div>
                          {port.link_number !== null && port.link_number !== undefined && (
                            <div>
                              <div className="text-xs text-muted-foreground mb-1">Link Number</div>
                              <div className="font-mono text-foreground">
                                {port.link_number}
                              </div>
                            </div>
                          )}
                        </div>

                        {port.port_path && (
                          <div className="bg-secondary/50 rounded p-2">
                            <div className="text-xs text-muted-foreground mb-1">Port Path</div>
                            <div className="font-mono text-xs text-brand-green">
                              {port.port_path}
                            </div>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Inferred Ports from Assemblies */}
      {portsData.inferred_port_count > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
              <Box className="w-5 h-5 text-accent" />
              Inferred Port Assemblies ({portsData.inferred_port_count})
            </h2>
            {portsData.explicit_port_count === 0 && (
              <Badge className="bg-accent/50 text-accent border-accent/70">
                Detected from Assemblies
              </Badge>
            )}
          </div>

          {portsData.explicit_port_count === 0 && (
            <div className="bg-primary/10 border border-primary/50 rounded-lg p-4 mb-4">
              <div className="flex items-start gap-3">
                <Info className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
                <div className="text-sm text-foreground">
                  This EDS file does not contain explicit <span className="font-mono text-primary">[Port]</span> definitions,
                  but port-related data was detected in <strong className="text-primary">assemblies</strong>.
                  This is common for devices with IO-Link masters, channel-based I/O, or modular systems.
                </div>
              </div>
            </div>
          )}

          <div className="grid gap-4">
            {portsData.inferred_ports.map((port, idx) => (
              <Card
                key={idx}
                className="bg-card border-border hover:border-accent/50 transition-colors"
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-foreground text-base flex items-center gap-2">
                        <Box className="w-4 h-4 text-accent" />
                        <span>{port.name}</span>
                      </CardTitle>
                      <CardDescription className="mt-1 text-xs">
                        Assembly #{port.assembly_number}
                      </CardDescription>
                    </div>
                    <Badge
                      variant="outline"
                      className="text-xs bg-accent/30 text-accent border-accent/70"
                    >
                      From Assembly
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-xs text-muted-foreground mb-1">Assembly Number</div>
                      <div className="font-mono text-accent">
                        {port.assembly_number}
                      </div>
                    </div>
                    {port.size > 0 && (
                      <div>
                        <div className="text-xs text-muted-foreground mb-1">Data Size</div>
                        <div className="font-mono text-accent">
                          {port.size} bytes
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Port-Related Parameters */}
      {portsData.port_parameter_count > 0 && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
              <Settings className="w-5 h-5 text-success" />
              Port Configuration Parameters
            </h2>
            <Badge className="bg-success/50 text-success border-success/70">
              {portsData.port_parameter_count} total
            </Badge>
          </div>

          <div className="grid gap-3">
            {portsData.port_parameters.map((param, idx) => (
              <div
                key={idx}
                className="bg-secondary/30 rounded-lg p-3 border border-border hover:border-success/50 transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-foreground truncate">
                      {param.name}
                    </div>
                    {param.description && (
                      <div className="text-xs text-muted-foreground mt-1">
                        {param.description}
                      </div>
                    )}
                  </div>
                  <Badge
                    variant="outline"
                    className="text-xs text-muted-foreground border-border flex-shrink-0"
                  >
                    #{param.param_number}
                  </Badge>
                </div>
              </div>
            ))}
          </div>

          {portsData.port_parameter_count > 20 && (
            <div className="text-center mt-4">
              <p className="text-sm text-muted-foreground">
                Showing 20 of {portsData.port_parameter_count} port-related parameters.
                See the <strong>Parameters</strong> tab for complete details.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Info Footer */}
      <div className="bg-primary/20 border border-primary/30 rounded-lg p-4">
        <div className="text-sm text-foreground">
          <strong className="text-primary">Port Information:</strong>{' '}
          {portsData.explicit_port_count > 0 ? (
            <>
              This device has explicit <span className="font-mono text-brand-green">[Port]</span> definitions
              for communication interfaces like TCP, Ethernet, and network protocols.
            </>
          ) : (
            <>
              While this EDS file lacks explicit port definitions, port-related data is available in{' '}
              <strong className="text-accent">Assemblies</strong> and{' '}
              <strong className="text-success">Parameters</strong> tabs.
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default PortsSection;
