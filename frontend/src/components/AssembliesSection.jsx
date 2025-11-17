import React, { useState, useEffect } from 'react';
import { Package, Variable, AlertCircle, Loader2, Activity, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui';
import { Badge } from './ui';
import axios from 'axios';

/**
 * Assemblies Section Component
 * Displays both fixed and variable assembly definitions for an EDS file
 */
const AssembliesSection = ({ edsId }) => {
  const [assemblies, setAssemblies] = useState({ fixed: [], variable: [], total_count: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!edsId) return;

    const fetchAssemblies = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/eds/${edsId}/assemblies`);
        setAssemblies(response.data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch assemblies:', err);
        setError('Failed to load assemblies');
      } finally {
        setLoading(false);
      }
    };

    fetchAssemblies();
  }, [edsId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="w-6 h-6 animate-spin text-primary" />
        <span className="ml-2 text-muted-foreground">Loading assemblies...</span>
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

  if (assemblies.total_count === 0) {
    return (
      <div className="text-center p-8 text-muted-foreground">
        <Package className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No assembly definitions found in this EDS file.</p>
        <p className="text-sm mt-2">
          Assemblies define I/O configurations and are used by connection definitions.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Fixed Assemblies */}
      {assemblies.fixed.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Package className="w-5 h-5 text-success" />
            <h3 className="text-lg font-semibold text-foreground">
              Fixed Assemblies
            </h3>
            <Badge className="bg-success/20 text-success border-success/50">
              {assemblies.fixed.length}
            </Badge>
          </div>

          <div className="grid gap-4">
            {assemblies.fixed.map((assembly) => (
              <Card
                key={assembly.id}
                className="bg-card border-border hover:border-success/50 transition-colors"
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-foreground text-base flex items-center gap-2">
                        <span className="font-mono text-success">
                          Assem{assembly.assembly_number}
                        </span>
                        <span className="text-muted-foreground">→</span>
                        <span>{assembly.assembly_name}</span>
                      </CardTitle>
                    </div>
                    <Badge
                      variant="outline"
                      className="text-xs text-muted-foreground border-border"
                    >
                      #{assembly.assembly_number}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <div className="text-xs text-muted-foreground mb-1">Type</div>
                      <div className="font-mono text-primary">
                        0x{assembly.assembly_type?.toString(16).padStart(2, '0') || '00'}
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground mb-1">Size</div>
                      <div className="font-mono text-foreground">
                        {assembly.size} bytes
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground mb-1">Field 1</div>
                      <div className="font-mono text-foreground">
                        {assembly.unknown_field1}
                      </div>
                    </div>
                  </div>

                  {assembly.path && (
                    <div className="bg-secondary/50 rounded p-2">
                      <div className="text-xs text-muted-foreground mb-1">Path</div>
                      <div className="font-mono text-xs text-brand-green">
                        {assembly.path}
                      </div>
                    </div>
                  )}

                  {assembly.help_string && (
                    <div className="text-sm text-muted-foreground italic">
                      {assembly.help_string}
                    </div>
                  )}

                  {/* Connection Usage */}
                  {assembly.used_by_connections && assembly.used_by_connections.length > 0 && (
                    <div className="bg-primary/10 border border-primary/30 rounded p-3">
                      <div className="flex items-center gap-2 mb-2">
                        <Activity className="w-4 h-4 text-primary" />
                        <div className="text-xs font-semibold text-primary">
                          Used by {assembly.used_by_connections.length} connection{assembly.used_by_connections.length > 1 ? 's' : ''}
                        </div>
                      </div>
                      <div className="space-y-1">
                        {assembly.used_by_connections.map((conn, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-xs">
                            <ArrowRight className="w-3 h-3 text-primary" />
                            <span className="text-foreground">{conn.connection_name || `Connection ${conn.connection_number}`}</span>
                            <Badge className="text-xs bg-primary/20 text-primary border-primary/50">
                              {conn.direction}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Variable Assemblies */}
      {assemblies.variable.length > 0 && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Variable className="w-5 h-5 text-secondary" />
            <h3 className="text-lg font-semibold text-foreground">
              Variable Assemblies
            </h3>
            <Badge className="bg-secondary/20 text-secondary border-secondary/50">
              {assemblies.variable.length}
            </Badge>
          </div>

          <div className="grid gap-4">
            {assemblies.variable.map((assembly) => (
              <Card
                key={assembly.id}
                className="bg-card border-border hover:border-secondary/50 transition-colors"
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-foreground text-base flex items-center gap-2">
                        <span className="font-mono text-secondary">
                          {assembly.assembly_name}
                        </span>
                      </CardTitle>
                      {assembly.description && (
                        <p className="text-sm text-muted-foreground mt-1">
                          {assembly.description}
                        </p>
                      )}
                    </div>
                    <Badge
                      variant="outline"
                      className="text-xs text-muted-foreground border-border"
                    >
                      #{assembly.assembly_number}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-xs text-muted-foreground mb-1">Max Size</div>
                      <div className="font-mono text-foreground">
                        {assembly.max_size} bytes
                      </div>
                    </div>
                    <div>
                      <div className="text-xs text-muted-foreground mb-1">Value</div>
                      <div className="font-mono text-foreground">
                        {assembly.unknown_value1}
                      </div>
                    </div>
                  </div>

                  <div className="bg-secondary/10 border border-secondary/30 rounded p-2">
                    <div className="text-xs text-secondary">
                      Variable-length assembly for dynamic I/O configurations
                    </div>
                  </div>

                  {/* Connection Usage */}
                  {assembly.used_by_connections && assembly.used_by_connections.length > 0 && (
                    <div className="bg-primary/10 border border-primary/30 rounded p-3">
                      <div className="flex items-center gap-2 mb-2">
                        <Activity className="w-4 h-4 text-primary" />
                        <div className="text-xs font-semibold text-primary">
                          Used by {assembly.used_by_connections.length} connection{assembly.used_by_connections.length > 1 ? 's' : ''}
                        </div>
                      </div>
                      <div className="space-y-1">
                        {assembly.used_by_connections.map((conn, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-xs">
                            <ArrowRight className="w-3 h-3 text-primary" />
                            <span className="text-foreground">{conn.connection_name || `Connection ${conn.connection_number}`}</span>
                            <Badge className="text-xs bg-primary/20 text-primary border-primary/50">
                              {conn.direction}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Info Footer */}
      <div className="bg-info/10 border border-info/30 rounded-lg p-4">
        <div className="text-sm text-foreground">
          <strong className="text-info">Assemblies</strong> define I/O data structures
          that are referenced by connection definitions. They specify the size and format
          of data exchanged between the device and controller.
        </div>
      </div>
    </div>
  );
};

export default AssembliesSection;
