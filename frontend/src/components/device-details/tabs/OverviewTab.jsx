import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, CardDescription, Badge, Tabs, TabsContent
} from '@/components/ui';
import {
  Zap, Database, ImageIcon, FileCode, FileText, GitBranch, Cable, Clock, CheckCircle, Code2, List, Layers, Settings, Lock, Wrench, Monitor, ExternalLink
} from 'lucide-react';


export const OverviewTab = ({ device, deviceData, API_BASE, formatVersion, translateText }) => {
  return (
              <TabsContent value="overview" className="space-y-6 mt-6">
            {/* Device Capabilities */}
            <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-foreground text-xl flex items-center gap-2">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-brand-green/20 to-brand-green/20 flex items-center justify-center">
                      <Zap className="w-5 h-5 text-brand-green" />
                    </div>
                    Device Capabilities
                  </CardTitle>
                  <Badge className="bg-brand-green/20 text-brand-green border-brand-green/50">
                    Features
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="flex items-center space-x-3 p-4 rounded-lg bg-gradient-to-br from-green-500/10 to-emerald-500/5 border border-border hover:border-success/50 transition-all">
                    <div className="w-10 h-10 rounded-lg bg-success/20 flex items-center justify-center flex-shrink-0">
                      <Database className="w-5 h-5 text-success" />
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Parameters</p>
                      <p className="text-lg font-bold text-foreground">{parameters.length}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 p-4 rounded-lg bg-gradient-to-br from-orange-500/10 to-amber-500/5 border border-border hover:border-warning/50 transition-all">
                    <div className="w-10 h-10 rounded-lg bg-warning/20 flex items-center justify-center flex-shrink-0">
                      <ImageIcon className="w-5 h-5 text-warning" />
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">Asset Files</p>
                      <p className="text-lg font-bold text-foreground">{imageAssets.length}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-3 p-4 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border hover:border-brand-green/50 transition-all">
                    <div className="w-10 h-10 rounded-lg bg-brand-green/20 flex items-center justify-center flex-shrink-0">
                      <FileCode className="w-5 h-5 text-brand-green" />
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">IODD Version</p>
                      <p className="text-lg font-bold text-foreground">v{formatVersion(device.iodd_version)}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Document Information */}
            {documentInfo && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-brand-green/20 to-brand-green/20 flex items-center justify-center">
                        <FileText className="w-5 h-5 text-brand-green" />
                      </div>
                      Document Information
                    </CardTitle>
                    <Badge className="bg-brand-green/20 text-brand-green border-brand-green/50">
                      Metadata
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Vendor Information Section */}
                    {(documentInfo.vendor_name || documentInfo.vendor_url || documentInfo.vendor_text) && (
                      <div className="pb-4 border-b border-border">
                        <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Vendor Information</h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {documentInfo.vendor_name && (
                            <div className="p-4 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border">
                              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Vendor</p>
                              <p className="text-sm text-foreground font-medium">{documentInfo.vendor_name}</p>
                            </div>
                          )}
                          {documentInfo.vendor_url && (
                            <div className="p-4 rounded-lg bg-gradient-to-br from-green-500/10 to-emerald-500/5 border border-border">
                              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Website</p>
                              <a
                                href={documentInfo.vendor_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-sm text-success hover:text-foreground-secondary underline transition-colors inline-flex items-center gap-1"
                              >
                                {documentInfo.vendor_url.replace(/^https?:\/\/(www\.)?/, '').split('/')[0]}
                                <ExternalLink className="w-3 h-3" />
                              </a>
                            </div>
                          )}
                          {documentInfo.vendor_text && (
                            <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Description</p>
                              <p className="text-sm text-foreground">{documentInfo.vendor_text}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Product Information */}
                    {(documentInfo.product_text || documentInfo.device_family) && (
                      <div className="pb-4 border-b border-border">
                        <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Product Information</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {documentInfo.product_text && (
                            <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Product Description</p>
                              <p className="text-sm text-foreground">{documentInfo.product_text}</p>
                            </div>
                          )}
                          {documentInfo.device_family && (
                            <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Device Family</p>
                              <p className="text-sm text-foreground">{documentInfo.device_family}</p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Document Metadata */}
                    <div>
                      <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Document Metadata</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {documentInfo.copyright && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                            <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Copyright</p>
                            <p className="text-sm text-foreground">{documentInfo.copyright}</p>
                          </div>
                        )}
                        {documentInfo.release_date && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                            <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Release Date</p>
                            <p className="text-sm text-foreground">{documentInfo.release_date}</p>
                          </div>
                        )}
                        {documentInfo.version && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                            <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Document Version</p>
                            <p className="text-sm text-foreground">{documentInfo.version}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Device Variants */}
            {deviceVariants && deviceVariants.length > 0 && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center">
                        <GitBranch className="w-5 h-5 text-purple-400" />
                      </div>
                      Device Variants
                    </CardTitle>
                    <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/50">
                      {deviceVariants.length} {deviceVariants.length === 1 ? 'Variant' : 'Variants'}
                    </Badge>
                  </div>
                  <CardDescription className="text-muted-foreground mt-2">
                    Multiple product configurations available for this device family
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {deviceVariants.map((variant, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-lg bg-gradient-to-br from-purple-500/10 to-pink-500/5 border border-border hover:border-purple-500/50 transition-all"
                      >
                        <div className="flex items-start gap-3">
                          {variant.product_variant_image && (
                            <div className="w-16 h-16 rounded-lg bg-background/50 border border-border flex items-center justify-center overflow-hidden flex-shrink-0">
                              <img
                                src={`${API_BASE}/api/iodd/${device.id}/asset/${variant.product_variant_image}`}
                                alt={variant.product_variant_id || 'Variant'}
                                className="w-full h-full object-contain"
                                onError={(e) => {
                                  e.target.style.display = 'none';
                                  e.target.parentElement.innerHTML = '<div class="text-muted-foreground text-xs">No Image</div>';
                                }}
                              />
                            </div>
                          )}
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <Badge className="bg-purple-500/20 text-purple-400 border-purple-500/50 text-xs">
                                {variant.product_variant_id}
                              </Badge>
                              {variant.device_symbol && (
                                <Badge className="bg-muted text-foreground text-xs">
                                  {variant.device_symbol}
                                </Badge>
                              )}
                            </div>
                            {variant.product_variant_name && (
                              <h4 className="text-foreground font-semibold text-sm mb-1">
                                {translateText(variant.product_variant_name)}
                              </h4>
                            )}
                            {variant.product_variant_text && (
                              <p className="text-muted-foreground text-xs leading-relaxed">
                                {translateText(variant.product_variant_text)}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Wiring Configurations */}
            {wiringConfigurations && wiringConfigurations.length > 0 && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-teal-500/20 to-emerald-500/20 flex items-center justify-center">
                        <Cable className="w-5 h-5 text-teal-400" />
                      </div>
                      Wiring Configurations
                    </CardTitle>
                    <Badge className="bg-teal-500/20 text-teal-400 border-teal-500/50">
                      Installation Guide
                    </Badge>
                  </div>
                  <CardDescription className="text-muted-foreground mt-2">
                    Connector pin-outs and wire assignments for proper device installation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Group by connector type */}
                    {Object.entries(
                      wiringConfigurations.reduce((acc, wire) => {
                        const connectorType = wire.connector_type || 'Unknown';
                        if (!acc[connectorType]) {
                          acc[connectorType] = [];
                        }
                        acc[connectorType].push(wire);
                        return acc;
                      }, {})
                    ).map(([connectorType, wires]) => (
                      <div key={connectorType} className="p-4 rounded-lg bg-gradient-to-br from-teal-500/10 to-emerald-500/5 border border-border">
                        <div className="flex items-start gap-4">
                          {/* Diagram Image (if available) */}
                          {wires[0].diagram_image && (
                            <div className="w-48 h-48 rounded-lg bg-background/50 border border-border flex items-center justify-center overflow-hidden flex-shrink-0">
                              <img
                                src={`${API_BASE}/api/iodd/${device.id}/asset/${wires[0].diagram_image}`}
                                alt={`${connectorType} diagram`}
                                className="w-full h-full object-contain"
                                onError={(e) => {
                                  e.target.style.display = 'none';
                                  e.target.parentElement.innerHTML = '<div class="text-muted-foreground text-xs p-4 text-center">Diagram not available</div>';
                                }}
                              />
                            </div>
                          )}

                          {/* Wire Details */}
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-3">
                              <Badge className="bg-teal-500/30 text-teal-300 border-teal-500/50">
                                {connectorType}
                              </Badge>
                            </div>

                            {wires[0].description && (
                              <p className="text-sm text-muted-foreground mb-4">
                                {translateText(wires[0].description)}
                              </p>
                            )}

                            {/* Pin Assignment Table */}
                            <div className="overflow-x-auto">
                              <table className="w-full text-sm">
                                <thead>
                                  <tr className="border-b border-border">
                                    <th className="text-left py-2 px-3 text-xs font-semibold text-teal-400 uppercase tracking-wider">Pin</th>
                                    <th className="text-left py-2 px-3 text-xs font-semibold text-teal-400 uppercase tracking-wider">Assignment</th>
                                    <th className="text-left py-2 px-3 text-xs font-semibold text-teal-400 uppercase tracking-wider">Color</th>
                                    <th className="text-left py-2 px-3 text-xs font-semibold text-teal-400 uppercase tracking-wider">Function</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {wires.map((wire, idx) => (
                                    <tr key={idx} className="border-b border-border/50 hover:bg-teal-500/5 transition-colors">
                                      <td className="py-2 px-3">
                                        <div className="flex items-center gap-2">
                                          <div className="w-6 h-6 rounded-full bg-teal-500/20 border border-teal-500/50 flex items-center justify-center">
                                            <span className="text-xs font-semibold text-teal-300">
                                              {wire.wire_number || '-'}
                                            </span>
                                          </div>
                                        </div>
                                      </td>
                                      <td className="py-2 px-3 text-foreground font-mono text-xs">
                                        {wire.pin_assignment || '-'}
                                      </td>
                                      <td className="py-2 px-3">
                                        {wire.wire_color ? (
                                          <div className="flex items-center gap-2">
                                            <div
                                              className="w-4 h-4 rounded-full border border-border"
                                              style={{
                                                backgroundColor: wire.wire_color.toLowerCase().includes('brown') ? '#8B4513' :
                                                              wire.wire_color.toLowerCase().includes('white') ? '#FFFFFF' :
                                                              wire.wire_color.toLowerCase().includes('blue') ? '#0000FF' :
                                                              wire.wire_color.toLowerCase().includes('black') ? '#000000' :
                                                              wire.wire_color.toLowerCase().includes('red') ? '#FF0000' :
                                                              wire.wire_color.toLowerCase().includes('green') ? '#00FF00' :
                                                              wire.wire_color.toLowerCase().includes('yellow') ? '#FFFF00' :
                                                              wire.wire_color.toLowerCase().includes('gray') || wire.wire_color.toLowerCase().includes('grey') ? '#808080' :
                                                              '#666666'
                                              }}
                                            />
                                            <span className="text-xs text-muted-foreground">{wire.wire_color}</span>
                                          </div>
                                        ) : (
                                          <span className="text-xs text-muted-foreground">-</span>
                                        )}
                                      </td>
                                      <td className="py-2 px-3 text-muted-foreground text-xs">
                                        {wire.wire_function || '-'}
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Test Configuration Procedures */}
            {testConfigurations && testConfigurations.config && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-violet-500/20 to-indigo-500/20 flex items-center justify-center">
                        <CheckCircle className="w-5 h-5 text-violet-400" />
                      </div>
                      Test & Commissioning Procedures
                    </CardTitle>
                    <Badge className="bg-violet-500/20 text-violet-400 border-violet-500/50">
                      Quality Assurance
                    </Badge>
                  </div>
                  <CardDescription className="text-muted-foreground mt-2">
                    Automated test procedures and validation steps for device commissioning
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Test Configuration Info */}
                    <div className="p-4 rounded-lg bg-gradient-to-br from-violet-500/10 to-indigo-500/5 border border-border">
                      <div className="space-y-3">
                        <div className="flex items-start gap-3">
                          <div className="mt-1">
                            <div className="w-10 h-10 rounded-lg bg-violet-500/20 border border-violet-500/30 flex items-center justify-center">
                              <Clock className="w-5 h-5 text-violet-400" />
                            </div>
                          </div>
                          <div className="flex-1">
                            <h4 className="text-foreground font-semibold text-base mb-2">
                              {testConfigurations.config.test_name || 'Device Test Configuration'}
                            </h4>
                            {testConfigurations.config.test_description && (
                              <p className="text-sm text-muted-foreground mb-3">
                                {translateText(testConfigurations.config.test_description)}
                              </p>
                            )}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                              {testConfigurations.config.test_duration && (
                                <div className="p-3 rounded-lg bg-background/50 border border-border">
                                  <p className="text-xs text-muted-foreground mb-1">Test Duration</p>
                                  <p className="text-sm font-mono text-violet-400">
                                    {testConfigurations.config.test_duration}
                                  </p>
                                </div>
                              )}
                              {testConfigurations.config.test_conditions && (
                                <div className="p-3 rounded-lg bg-background/50 border border-border md:col-span-2">
                                  <p className="text-xs text-muted-foreground mb-1">Test Conditions</p>
                                  <p className="text-sm text-foreground">
                                    {translateText(testConfigurations.config.test_conditions)}
                                  </p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Event Triggers */}
                    {testConfigurations.events && testConfigurations.events.length > 0 && (
                      <div>
                        <h4 className="text-sm font-semibold text-violet-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                          <Zap className="w-4 h-4" />
                          Test Event Triggers ({testConfigurations.events.length})
                        </h4>
                        <div className="space-y-3">
                          {testConfigurations.events.map((event, idx) => (
                            <div
                              key={idx}
                              className="p-3 rounded-lg bg-gradient-to-br from-violet-500/5 to-indigo-500/5 border border-border hover:border-violet-500/30 transition-all"
                            >
                              <div className="flex items-start gap-3">
                                <div className="mt-1">
                                  <div className="w-8 h-8 rounded-lg bg-violet-500/20 border border-violet-500/30 flex items-center justify-center">
                                    <span className="text-xs font-semibold text-violet-300">
                                      {idx + 1}
                                    </span>
                                  </div>
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center gap-2 mb-2">
                                    <h5 className="text-foreground font-semibold text-sm">
                                      {event.event_name || `Event ${idx + 1}`}
                                    </h5>
                                    {event.trigger_condition && (
                                      <Badge className="bg-violet-500/20 text-violet-400 border-violet-500/50 text-xs">
                                        {event.trigger_condition}
                                      </Badge>
                                    )}
                                  </div>
                                  {event.event_description && (
                                    <p className="text-xs text-muted-foreground leading-relaxed">
                                      {translateText(event.event_description)}
                                    </p>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Custom Datatypes */}
            {customDatatypes && customDatatypes.length > 0 && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-amber-500/20 to-yellow-500/20 flex items-center justify-center">
                        <Code2 className="w-5 h-5 text-amber-400" />
                      </div>
                      Custom Datatypes
                    </CardTitle>
                    <Badge className="bg-amber-500/20 text-amber-400 border-amber-500/50">
                      {customDatatypes.length} {customDatatypes.length === 1 ? 'Type' : 'Types'}
                    </Badge>
                  </div>
                  <CardDescription className="text-muted-foreground mt-2">
                    Device-specific complex data structures and enumerations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {customDatatypes.map((datatype, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-lg bg-gradient-to-br from-amber-500/10 to-yellow-500/5 border border-border hover:border-amber-500/30 transition-all"
                      >
                        <div className="space-y-3">
                          {/* Datatype Header */}
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <h4 className="text-foreground font-semibold text-base">
                                  {datatype.datatype_name || datatype.datatype_id}
                                </h4>
                                <Badge className="bg-amber-500/20 text-amber-400 border-amber-500/50 text-xs">
                                  {datatype.value_type}
                                </Badge>
                                {datatype.bit_length && (
                                  <Badge className="bg-muted text-foreground text-xs">
                                    {datatype.bit_length} bits
                                  </Badge>
                                )}
                              </div>
                              {datatype.datatype_id && datatype.datatype_id !== datatype.datatype_name && (
                                <p className="text-xs text-muted-foreground font-mono mb-2">
                                  ID: {datatype.datatype_id}
                                </p>
                              )}
                            </div>
                          </div>

                          {/* Single Value Enumeration */}
                          {datatype.value_type === 'SingleValue' && datatype.single_values && datatype.single_values.length > 0 && (
                            <div>
                              <h5 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                                <List className="w-3 h-3" />
                                Enumeration Values ({datatype.single_values.length})
                              </h5>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                {datatype.single_values.map((sv, svIdx) => (
                                  <div
                                    key={svIdx}
                                    className="p-2 rounded bg-background/50 border border-border hover:bg-amber-500/5 transition-colors"
                                  >
                                    <div className="flex items-center gap-2">
                                      <div className="w-8 h-8 rounded bg-amber-500/20 border border-amber-500/30 flex items-center justify-center flex-shrink-0">
                                        <span className="text-xs font-mono font-semibold text-amber-300">
                                          {sv.value}
                                        </span>
                                      </div>
                                      <div className="flex-1 min-w-0">
                                        <p className="text-sm text-foreground truncate">
                                          {translateText(sv.value_text) || `Value ${sv.value}`}
                                        </p>
                                      </div>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {/* Record Item Structure */}
                          {datatype.value_type === 'RecordItem' && datatype.record_items && datatype.record_items.length > 0 && (
                            <div>
                              <h5 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                                <Layers className="w-3 h-3" />
                                Record Structure ({datatype.record_items.length} fields)
                              </h5>
                              <div className="overflow-x-auto">
                                <table className="w-full text-sm">
                                  <thead>
                                    <tr className="border-b border-border">
                                      <th className="text-left py-2 px-3 text-xs font-semibold text-amber-400 uppercase tracking-wider">Subindex</th>
                                      <th className="text-left py-2 px-3 text-xs font-semibold text-amber-400 uppercase tracking-wider">Field Name</th>
                                      <th className="text-left py-2 px-3 text-xs font-semibold text-amber-400 uppercase tracking-wider">Type</th>
                                      <th className="text-left py-2 px-3 text-xs font-semibold text-amber-400 uppercase tracking-wider">Bit Length</th>
                                      <th className="text-left py-2 px-3 text-xs font-semibold text-amber-400 uppercase tracking-wider">Offset</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {datatype.record_items.map((item, itemIdx) => (
                                      <tr key={itemIdx} className="border-b border-border/50 hover:bg-amber-500/5 transition-colors">
                                        <td className="py-2 px-3">
                                          <div className="w-7 h-7 rounded bg-amber-500/20 border border-amber-500/30 flex items-center justify-center">
                                            <span className="text-xs font-semibold text-amber-300">
                                              {item.subindex}
                                            </span>
                                          </div>
                                        </td>
                                        <td className="py-2 px-3 text-foreground font-mono text-xs">
                                          {item.record_item_name}
                                        </td>
                                        <td className="py-2 px-3">
                                          <Badge className="bg-muted text-foreground text-xs">
                                            {item.simple_datatype}
                                          </Badge>
                                        </td>
                                        <td className="py-2 px-3 text-muted-foreground text-xs font-mono">
                                          {item.bit_length || '-'}
                                        </td>
                                        <td className="py-2 px-3 text-muted-foreground text-xs font-mono">
                                          {item.bit_offset !== null ? item.bit_offset : '-'}
                                        </td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Device Features & Capabilities */}
            {deviceFeatures && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-secondary/20 to-accent/20 flex items-center justify-center">
                        <Settings className="w-5 h-5 text-secondary" />
                      </div>
                      Device Features
                    </CardTitle>
                    <Badge className="bg-secondary/20 text-secondary border-secondary/50">
                      Capabilities
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {/* Feature flags */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      <div className={`p-3 rounded-lg border ${deviceFeatures.data_storage ? 'bg-success/10 border-success/30' : 'bg-secondary/50 border-border'}`}>
                        <div className="flex items-center gap-2">
                          <Database className={`w-4 h-4 ${deviceFeatures.data_storage ? 'text-success' : 'text-muted-foreground'}`} />
                          <span className={`text-sm ${deviceFeatures.data_storage ? 'text-success' : 'text-muted-foreground'}`}>
                            Data Storage
                          </span>
                        </div>
                      </div>
                      <div className={`p-3 rounded-lg border ${deviceFeatures.block_parameter ? 'bg-success/10 border-success/30' : 'bg-secondary/50 border-border'}`}>
                        <div className="flex items-center gap-2">
                          <Lock className={`w-4 h-4 ${deviceFeatures.block_parameter ? 'text-success' : 'text-muted-foreground'}`} />
                          <span className={`text-sm ${deviceFeatures.block_parameter ? 'text-success' : 'text-muted-foreground'}`}>
                            Block Parameter
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Profile Characteristic */}
                    {deviceFeatures.profile_characteristic && (() => {
                      const characteristics = decodeProfileCharacteristics(deviceFeatures.profile_characteristic);
                      return (
                        <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                          <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Profile Characteristics</p>
                          <p className="text-xs text-muted-foreground font-mono mb-2">Raw: {deviceFeatures.profile_characteristic}</p>
                          {characteristics.length > 0 ? (
                            <div className="flex flex-wrap gap-2 mt-2">
                              {characteristics.map((char) => (
                                <Badge
                                  key={char.code}
                                  className="bg-secondary/20 text-foreground-secondary border-secondary/50 text-xs"
                                  title={`${char.description} (Code: ${char.code})`}
                                >
                                  {char.name}
                                </Badge>
                              ))}
                            </div>
                          ) : (
                            <p className="text-xs text-muted-foreground italic">No profile characteristics decoded</p>
                          )}
                        </div>
                      );
                    })()}

                    {/* Access Locks */}
                    <div>
                      <p className="text-xs text-muted-foreground uppercase tracking-wider mb-3">Supported Access Locks</p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        <div className={`p-3 rounded-lg border text-center ${deviceFeatures.access_locks_data_storage ? 'bg-brand-green/10 border-brand-green/30' : 'bg-secondary/50 border-border'}`}>
                          <Database className={`w-4 h-4 mx-auto mb-1 ${deviceFeatures.access_locks_data_storage ? 'text-brand-green' : 'text-muted-foreground'}`} />
                          <span className={`text-xs ${deviceFeatures.access_locks_data_storage ? 'text-brand-green' : 'text-muted-foreground'}`}>
                            Data Storage
                          </span>
                        </div>
                        <div className={`p-3 rounded-lg border text-center ${deviceFeatures.access_locks_parameter ? 'bg-brand-green/10 border-brand-green/30' : 'bg-secondary/50 border-border'}`}>
                          <Settings className={`w-4 h-4 mx-auto mb-1 ${deviceFeatures.access_locks_parameter ? 'text-brand-green' : 'text-muted-foreground'}`} />
                          <span className={`text-xs ${deviceFeatures.access_locks_parameter ? 'text-brand-green' : 'text-muted-foreground'}`}>
                            Parameter
                          </span>
                        </div>
                        <div className={`p-3 rounded-lg border text-center ${deviceFeatures.access_locks_local_parameterization ? 'bg-brand-green/10 border-brand-green/30' : 'bg-secondary/50 border-border'}`}>
                          <Wrench className={`w-4 h-4 mx-auto mb-1 ${deviceFeatures.access_locks_local_parameterization ? 'text-brand-green' : 'text-muted-foreground'}`} />
                          <span className={`text-xs ${deviceFeatures.access_locks_local_parameterization ? 'text-brand-green' : 'text-muted-foreground'}`}>
                            Local Param
                          </span>
                        </div>
                        <div className={`p-3 rounded-lg border text-center ${deviceFeatures.access_locks_local_user_interface ? 'bg-brand-green/10 border-brand-green/30' : 'bg-secondary/50 border-border'}`}>
                          <Monitor className={`w-4 h-4 mx-auto mb-1 ${deviceFeatures.access_locks_local_user_interface ? 'text-brand-green' : 'text-muted-foreground'}`} />
                          <span className={`text-xs ${deviceFeatures.access_locks_local_user_interface ? 'text-brand-green' : 'text-muted-foreground'}`}>
                            Local UI
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Device Images Gallery */}
            {imageAssets.length > 0 && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-brand-green/30 transition-all">
                <CardHeader>
                  <CardTitle className="text-foreground text-xl flex items-center gap-2">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500/20 to-amber-500/20 flex items-center justify-center">
                      <ImageIcon className="w-5 h-5 text-warning" />
                    </div>
                    Device Images
                  </CardTitle>
                  <CardDescription className="text-muted-foreground">
                    Visual assets and product images
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {imageAssets.map((asset, index) => (
                      <div key={asset.id} className="group space-y-2">
                        <div
                          onClick={() => {
                            setLightboxIndex(index);
                            setLightboxOpen(true);
                          }}
                          className="aspect-square bg-gradient-to-br from-surface to-surface rounded-lg p-3 border border-border hover:border-brand-green/50 transition-all cursor-pointer relative overflow-hidden"
                        >
                          {/* Hover glow effect */}
                          <div className="absolute inset-0 bg-gradient-to-br from-brand-green/20 to-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity" />

                          <img
                            src={`${API_BASE}/api/iodd/${device.id}/assets/${asset.id}`}
                            alt={asset.file_name}
                            className="relative z-10 w-full h-full object-contain group-hover:scale-110 transition-transform duration-300"
                          />
                        </div>
                        <div className="text-center">
                          <p className="text-xs text-muted-foreground truncate">{asset.file_name}</p>
                          {asset.image_purpose && (
                            <Badge className="text-xs mt-1 bg-brand-green/20 text-brand-green border-brand-green/50">
                              {asset.image_purpose}
                            </Badge>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

  );
};
