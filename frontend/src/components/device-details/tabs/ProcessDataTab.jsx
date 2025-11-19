import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, CardDescription, Button, Badge, TabsContent, Skeleton
} from '@/components/ui';
import {
  Activity, Download, Info, Database
} from 'lucide-react';


export const ProcessDataTab = ({ device, deviceData, exportHandlers, formatDisplayValue, applyScaling, getUiInfo }) => {
  return (
              <TabsContent value="processdata" className="space-y-4 mt-6">
            <Card className="bg-card/80 backdrop-blur-sm border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-brand-green/20 to-brand-green/20 flex items-center justify-center">
                        <ArrowRightLeft className="w-5 h-5 text-brand-green" />
                      </div>
                      Process Data Structure
                    </CardTitle>
                    <CardDescription className="text-muted-foreground mt-2">
                      Input and output process data configuration for real-time communication
                    </CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleExportProcessData('csv')}
                      disabled={processData.length === 0}
                      className="border-brand-green/50 text-foreground-secondary hover:bg-brand-green/10"
                      title="Export to CSV"
                    >
                      <Download className="w-4 h-4 mr-1" />
                      CSV
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleExportProcessData('json')}
                      disabled={processData.length === 0}
                      className="border-brand-green/50 text-foreground-secondary hover:bg-brand-green/10"
                      title="Export to JSON"
                    >
                      <Download className="w-4 h-4 mr-1" />
                      JSON
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loadingProcessData ? (
                  <div className="space-y-3">
                    {[...Array(4)].map((_, i) => (
                      <Skeleton key={i} className="h-24 bg-secondary" />
                    ))}
                  </div>
                ) : processData.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    No process data defined for this device
                  </div>
                ) : (
                  <div className="space-y-4">
                    {/* Process Data Conditions */}
                    {processDataConditions && processDataConditions.length > 0 && (
                      <div className="mb-6">
                        <div className="bg-gradient-to-br from-blue-500/10 to-cyan-500/5 border border-blue-500/30 rounded-lg p-4">
                          <h3 className="text-lg font-semibold text-blue-400 mb-3 flex items-center gap-2">
                            <Workflow className="w-5 h-5" />
                            Conditional Process Data Structures
                          </h3>
                          <p className="text-xs text-muted-foreground mb-4">
                            Process data structures that change based on device operating mode or configuration
                          </p>
                          <div className="space-y-3">
                            {processDataConditions.map((condition, idx) => (
                              <div
                                key={idx}
                                className="p-3 rounded-lg bg-background/50 border border-border"
                              >
                                <div className="flex items-start gap-3">
                                  <div className="mt-1">
                                    <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/50 text-xs">
                                      Condition {idx + 1}
                                    </Badge>
                                  </div>
                                  <div className="flex-1">
                                    {condition.variable_id && (
                                      <div className="mb-2">
                                        <span className="text-xs text-muted-foreground">Variable: </span>
                                        <code className="text-xs bg-muted px-2 py-0.5 rounded text-brand-green">
                                          {condition.variable_id}
                                        </code>
                                      </div>
                                    )}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-xs">
                                      {condition.value_filter && (
                                        <div>
                                          <span className="text-muted-foreground">Filter: </span>
                                          <code className="text-foreground font-mono">{condition.value_filter}</code>
                                        </div>
                                      )}
                                      {condition.max_value !== null && (
                                        <div>
                                          <span className="text-muted-foreground">Max Value: </span>
                                          <code className="text-foreground font-mono">{condition.max_value}</code>
                                        </div>
                                      )}
                                      {condition.min_value !== null && (
                                        <div>
                                          <span className="text-muted-foreground">Min Value: </span>
                                          <code className="text-foreground font-mono">{condition.min_value}</code>
                                        </div>
                                      )}
                                    </div>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Process Data Inputs */}
                    {processData.filter(pd => pd.direction === 'input').length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-brand-green mb-3 flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-brand-green animate-pulse" />
                          Process Data Inputs ({processData.filter(pd => pd.direction === 'input').length})
                        </h3>
                        <div className="space-y-3">
                          {processData.filter(pd => pd.direction === 'input').map((pd) => (
                            <div
                              key={pd.id}
                              className="p-4 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border hover:border-brand-green/50 transition-all"
                            >
                              <div className="flex items-start justify-between mb-3">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-2">
                                    <h4 className="text-foreground font-semibold">{pd.name}</h4>
                                    <Badge className="bg-brand-green/20 text-foreground-secondary border-brand-green/50 text-xs">
                                      {pd.bit_length} bits
                                    </Badge>
                                    <Badge className="bg-muted text-foreground text-xs">
                                      {pd.data_type}
                                    </Badge>
                                  </div>
                                  <p className="text-xs text-muted-foreground font-mono">ID: {pd.pd_id}</p>
                                </div>
                              </div>
                              {pd.record_items && pd.record_items.length > 0 && (
                                <>
                                  {/* Bit Field Visualizer */}
                                  <div className="mt-3 pt-3 border-t border-border">
                                    <p className="text-xs text-muted-foreground mb-2 font-semibold flex items-center gap-2">
                                      <span>Bit Field Layout</span>
                                      <Badge className="bg-muted text-foreground text-xs">
                                        {Math.ceil(pd.bit_length / 8)} bytes
                                      </Badge>
                                    </p>
                                    <div className="space-y-2">
                                      {(() => {
                                        const totalBytes = Math.ceil(pd.bit_length / 8);
                                        const bytes = [];

                                        for (let byteIdx = 0; byteIdx < totalBytes; byteIdx++) {
                                          const bitStart = byteIdx * 8;
                                          const bitEnd = Math.min(bitStart + 8, pd.bit_length);
                                          const bits = [];

                                          for (let bitPos = bitStart; bitPos < bitEnd; bitPos++) {
                                            // Find which field this bit belongs to
                                            const field = pd.record_items.find(item =>
                                              bitPos >= item.bit_offset &&
                                              bitPos < item.bit_offset + item.bit_length
                                            );

                                            bits.push({
                                              position: bitPos,
                                              field: field,
                                              isStart: field && bitPos === field.bit_offset,
                                              isEnd: field && bitPos === field.bit_offset + field.bit_length - 1
                                            });
                                          }

                                          bytes.push({ byteIdx, bits });
                                        }

                                        return bytes.map(({ byteIdx, bits }) => (
                                          <div key={byteIdx} className="bg-secondary/30 rounded p-2">
                                            <div className="flex items-center gap-2 mb-1">
                                              <span className="text-xs text-muted-foreground font-mono w-16">Byte {byteIdx}:</span>
                                              <div className="flex gap-px flex-1">
                                                {bits.map((bit, idx) => {
                                                  const color = bit.field
                                                    ? `hsl(${(bit.field.subindex * 137.5) % 360}, 70%, 50%)`
                                                    : 'hsl(var(--muted-foreground))';

                                                  return (
                                                    <div
                                                      key={idx}
                                                      className="relative group"
                                                      style={{ flex: 1 }}
                                                    >
                                                      <div
                                                        className="h-8 border border-border flex items-center justify-center text-xs font-mono transition-all hover:z-10 hover:scale-110"
                                                        style={{
                                                          backgroundColor: bit.field ? `${color}20` : 'hsl(var(--background))',
                                                          borderColor: bit.field ? `${color}80` : 'hsl(var(--border))',
                                                          borderLeftWidth: bit.isStart ? '2px' : '1px',
                                                          borderRightWidth: bit.isEnd ? '2px' : '1px'
                                                        }}
                                                        title={bit.field ? `${bit.field.name} (bit ${bit.position})` : `Unused (bit ${bit.position})`}
                                                      >
                                                        <span className="text-muted-foreground" style={{ fontSize: '9px' }}>
                                                          {7 - (bit.position % 8)}
                                                        </span>
                                                      </div>
                                                      {bit.field && (
                                                        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 hidden group-hover:block z-20">
                                                          <div className="bg-card border border-border rounded px-2 py-1 text-xs whitespace-nowrap shadow-lg">
                                                            <div className="font-semibold text-foreground">{bit.field.name}</div>
                                                            <div className="text-muted-foreground">Bit {bit.position} ({bit.field.data_type})</div>
                                                          </div>
                                                        </div>
                                                      )}
                                                    </div>
                                                  );
                                                })}
                                              </div>
                                            </div>
                                          </div>
                                        ));
                                      })()}
                                    </div>
                                    <div className="mt-2 flex flex-wrap gap-2">
                                      {pd.record_items.map((item) => {
                                        const color = `hsl(${(item.subindex * 137.5) % 360}, 70%, 50%)`;
                                        return (
                                          <div key={item.subindex} className="flex items-center gap-1 text-xs">
                                            <div
                                              className="w-3 h-3 rounded border"
                                              style={{
                                                backgroundColor: `${color}30`,
                                                borderColor: `${color}80`
                                              }}
                                            />
                                            <span className="text-foreground">{item.name}</span>
                                          </div>
                                        );
                                      })}
                                    </div>
                                  </div>

                                  {/* Record Structure Details */}
                                  <div className="mt-3 pt-3 border-t border-border">
                                    <p className="text-xs text-muted-foreground mb-2 font-semibold">Field Details:</p>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                      {pd.record_items.map((item) => {
                                        const uiInfo = getUiInfo(item.name);
                                        return (
                                          <div
                                            key={item.subindex}
                                            className="p-2 rounded bg-secondary/50 border border-border"
                                          >
                                            <div className="flex items-center justify-between mb-1">
                                              <span className="text-foreground text-sm font-medium">{item.name}</span>
                                              <span className="text-xs text-muted-foreground font-mono">idx:{item.subindex}</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                              <span className="font-mono">{item.data_type}</span>
                                              <span>•</span>
                                              <span>{item.bit_length} bits</span>
                                              <span>•</span>
                                              <span>offset: {item.bit_offset}</span>
                                            </div>
                                            {uiInfo && (uiInfo.gradient !== null || uiInfo.offset !== null || uiInfo.unit_code || uiInfo.display_format) && (
                                              <div className="mt-2 pt-2 border-t border-brand-green/20">
                                                <p className="text-xs text-brand-green mb-1 font-semibold">UI Rendering:</p>
                                                <div className="space-y-0.5 text-xs">
                                                  {uiInfo.gradient !== null && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Gradient:</span> {uiInfo.gradient}
                                                    </div>
                                                  )}
                                                  {uiInfo.offset !== null && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Offset:</span> {uiInfo.offset}
                                                    </div>
                                                  )}
                                                  {uiInfo.unit_code && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Unit:</span> {uiInfo.unit_code}
                                                    </div>
                                                  )}
                                                  {uiInfo.display_format && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Format:</span> {uiInfo.display_format}
                                                    </div>
                                                  )}
                                                  <div className="text-brand-green font-mono mt-1">
                                                    Example: raw value 100 → {formatDisplayValue(100, uiInfo)}
                                                  </div>
                                                </div>
                                              </div>
                                            )}
                                            {item.single_values && item.single_values.length > 0 && (
                                              <div className="mt-2 pt-2 border-t border-border">
                                                <p className="text-xs text-muted-foreground mb-1">Values:</p>
                                                <div className="flex flex-wrap gap-1">
                                                  {item.single_values.map((sv, svIdx) => (
                                                    <div
                                                      key={svIdx}
                                                      className="text-xs px-2 py-1 rounded bg-muted/50 text-foreground"
                                                      title={sv.description || sv.name}
                                                    >
                                                      <span className="font-mono text-brand-green">{sv.value}</span>
                                                      <span className="text-muted-foreground mx-1">=</span>
                                                      <span>{sv.name}</span>
                                                    </div>
                                                  ))}
                                                </div>
                                              </div>
                                            )}
                                          </div>
                                        );
                                      })}
                                    </div>
                                  </div>
                                </>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Process Data Outputs */}
                    {processData.filter(pd => pd.direction === 'output').length > 0 && (
                      <div>
                        <h3 className="text-lg font-semibold text-secondary mb-3 flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
                          Process Data Outputs ({processData.filter(pd => pd.direction === 'output').length})
                        </h3>
                        <div className="space-y-3">
                          {processData.filter(pd => pd.direction === 'output').map((pd) => (
                            <div
                              key={pd.id}
                              className="p-4 rounded-lg bg-gradient-to-br from-secondary/10 to-accent/5 border border-border hover:border-secondary/50 transition-all"
                            >
                              <div className="flex items-start justify-between mb-3">
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-2">
                                    <h4 className="text-foreground font-semibold">{pd.name}</h4>
                                    <Badge className="bg-secondary/20 text-foreground-secondary border-secondary/50 text-xs">
                                      {pd.bit_length} bits
                                    </Badge>
                                    <Badge className="bg-muted text-foreground text-xs">
                                      {pd.data_type}
                                    </Badge>
                                  </div>
                                  <p className="text-xs text-muted-foreground font-mono">ID: {pd.pd_id}</p>
                                </div>
                              </div>
                              {pd.record_items && pd.record_items.length > 0 && (
                                <>
                                  {/* Bit Field Visualizer */}
                                  <div className="mt-3 pt-3 border-t border-border">
                                    <p className="text-xs text-muted-foreground mb-2 font-semibold flex items-center gap-2">
                                      <span>Bit Field Layout</span>
                                      <Badge className="bg-muted text-foreground text-xs">
                                        {Math.ceil(pd.bit_length / 8)} bytes
                                      </Badge>
                                    </p>
                                    <div className="space-y-2">
                                      {(() => {
                                        const totalBytes = Math.ceil(pd.bit_length / 8);
                                        const bytes = [];

                                        for (let byteIdx = 0; byteIdx < totalBytes; byteIdx++) {
                                          const bitStart = byteIdx * 8;
                                          const bitEnd = Math.min(bitStart + 8, pd.bit_length);
                                          const bits = [];

                                          for (let bitPos = bitStart; bitPos < bitEnd; bitPos++) {
                                            // Find which field this bit belongs to
                                            const field = pd.record_items.find(item =>
                                              bitPos >= item.bit_offset &&
                                              bitPos < item.bit_offset + item.bit_length
                                            );

                                            bits.push({
                                              position: bitPos,
                                              field: field,
                                              isStart: field && bitPos === field.bit_offset,
                                              isEnd: field && bitPos === field.bit_offset + field.bit_length - 1
                                            });
                                          }

                                          bytes.push({ byteIdx, bits });
                                        }

                                        return bytes.map(({ byteIdx, bits }) => (
                                          <div key={byteIdx} className="bg-secondary/30 rounded p-2">
                                            <div className="flex items-center gap-2 mb-1">
                                              <span className="text-xs text-muted-foreground font-mono w-16">Byte {byteIdx}:</span>
                                              <div className="flex gap-px flex-1">
                                                {bits.map((bit, idx) => {
                                                  const color = bit.field
                                                    ? `hsl(${(bit.field.subindex * 137.5) % 360}, 70%, 50%)`
                                                    : 'hsl(var(--muted-foreground))';

                                                  return (
                                                    <div
                                                      key={idx}
                                                      className="relative group"
                                                      style={{ flex: 1 }}
                                                    >
                                                      <div
                                                        className="h-8 border border-border flex items-center justify-center text-xs font-mono transition-all hover:z-10 hover:scale-110"
                                                        style={{
                                                          backgroundColor: bit.field ? `${color}20` : 'hsl(var(--background))',
                                                          borderColor: bit.field ? `${color}80` : 'hsl(var(--border))',
                                                          borderLeftWidth: bit.isStart ? '2px' : '1px',
                                                          borderRightWidth: bit.isEnd ? '2px' : '1px'
                                                        }}
                                                        title={bit.field ? `${bit.field.name} (bit ${bit.position})` : `Unused (bit ${bit.position})`}
                                                      >
                                                        <span className="text-muted-foreground" style={{ fontSize: '9px' }}>
                                                          {7 - (bit.position % 8)}
                                                        </span>
                                                      </div>
                                                      {bit.field && (
                                                        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 hidden group-hover:block z-20">
                                                          <div className="bg-card border border-border rounded px-2 py-1 text-xs whitespace-nowrap shadow-lg">
                                                            <div className="font-semibold text-foreground">{bit.field.name}</div>
                                                            <div className="text-muted-foreground">Bit {bit.position} ({bit.field.data_type})</div>
                                                          </div>
                                                        </div>
                                                      )}
                                                    </div>
                                                  );
                                                })}
                                              </div>
                                            </div>
                                          </div>
                                        ));
                                      })()}
                                    </div>
                                    <div className="mt-2 flex flex-wrap gap-2">
                                      {pd.record_items.map((item) => {
                                        const color = `hsl(${(item.subindex * 137.5) % 360}, 70%, 50%)`;
                                        return (
                                          <div key={item.subindex} className="flex items-center gap-1 text-xs">
                                            <div
                                              className="w-3 h-3 rounded border"
                                              style={{
                                                backgroundColor: `${color}30`,
                                                borderColor: `${color}80`
                                              }}
                                            />
                                            <span className="text-foreground">{item.name}</span>
                                          </div>
                                        );
                                      })}
                                    </div>
                                  </div>

                                  {/* Record Structure Details */}
                                  <div className="mt-3 pt-3 border-t border-border">
                                    <p className="text-xs text-muted-foreground mb-2 font-semibold">Field Details:</p>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                      {pd.record_items.map((item) => {
                                        const uiInfo = getUiInfo(item.name);
                                        return (
                                          <div
                                            key={item.subindex}
                                            className="p-2 rounded bg-secondary/50 border border-border"
                                          >
                                            <div className="flex items-center justify-between mb-1">
                                              <span className="text-foreground text-sm font-medium">{item.name}</span>
                                              <span className="text-xs text-muted-foreground font-mono">idx:{item.subindex}</span>
                                            </div>
                                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                              <span className="font-mono">{item.data_type}</span>
                                              <span>•</span>
                                              <span>{item.bit_length} bits</span>
                                              <span>•</span>
                                              <span>offset: {item.bit_offset}</span>
                                            </div>
                                            {uiInfo && (uiInfo.gradient !== null || uiInfo.offset !== null || uiInfo.unit_code || uiInfo.display_format) && (
                                              <div className="mt-2 pt-2 border-t border-brand-green/20">
                                                <p className="text-xs text-brand-green mb-1 font-semibold">UI Rendering:</p>
                                                <div className="space-y-0.5 text-xs">
                                                  {uiInfo.gradient !== null && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Gradient:</span> {uiInfo.gradient}
                                                    </div>
                                                  )}
                                                  {uiInfo.offset !== null && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Offset:</span> {uiInfo.offset}
                                                    </div>
                                                  )}
                                                  {uiInfo.unit_code && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Unit:</span> {uiInfo.unit_code}
                                                    </div>
                                                  )}
                                                  {uiInfo.display_format && (
                                                    <div className="text-muted-foreground">
                                                      <span className="font-mono">Format:</span> {uiInfo.display_format}
                                                    </div>
                                                  )}
                                                  <div className="text-brand-green font-mono mt-1">
                                                    Example: raw value 100 → {formatDisplayValue(100, uiInfo)}
                                                  </div>
                                                </div>
                                              </div>
                                            )}
                                            {item.single_values && item.single_values.length > 0 && (
                                              <div className="mt-2 pt-2 border-t border-border">
                                                <p className="text-xs text-muted-foreground mb-1">Values:</p>
                                                <div className="flex flex-wrap gap-1">
                                                  {item.single_values.map((sv, svIdx) => (
                                                    <div
                                                      key={svIdx}
                                                      className="text-xs px-2 py-1 rounded bg-muted/50 text-foreground"
                                                      title={sv.description || sv.name}
                                                    >
                                                      <span className="font-mono text-brand-green">{sv.value}</span>
                                                      <span className="text-muted-foreground mx-1">=</span>
                                                      <span>{sv.name}</span>
                                                    </div>
                                                  ))}
                                                </div>
                                              </div>
                                            )}
                                          </div>
                                        );
                                      })}
                                    </div>
                                  </div>
                                </>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

  );
};
