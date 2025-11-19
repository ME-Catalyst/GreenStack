import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, CardDescription, Badge, TabsContent
} from '@/components/ui';
import {
  Wifi, Network, Gauge
} from 'lucide-react';


export const CommunicationTab = ({ device, communicationProfile, translateBitrate, formatCycleTime }) => {
  return (
              <TabsContent value="communication" className="space-y-4 mt-6">
            {communicationProfile ? (
              <Card className="bg-card/80 backdrop-blur-sm border-border">
                <CardHeader>
                  <CardTitle className="text-foreground text-xl flex items-center gap-2">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-teal-500/20 to-emerald-500/20 flex items-center justify-center">
                      <Wifi className="w-5 h-5 text-teal-400" />
                    </div>
                    IO-Link Communication Profile
                  </CardTitle>
                  <CardDescription className="text-muted-foreground">
                    Network configuration and physical connection details
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Protocol Information */}
                    <div>
                      <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Protocol</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {communicationProfile.iolink_revision && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-teal-500/10 to-emerald-500/5 border border-border">
                            <p className="text-xs text-muted-foreground mb-1">IO-Link Revision</p>
                            <p className="text-lg font-bold text-teal-400">{communicationProfile.iolink_revision}</p>
                          </div>
                        )}
                        {communicationProfile.compatible_with && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border">
                            <p className="text-xs text-muted-foreground mb-1">Compatible With</p>
                            <p className="text-lg font-bold text-brand-green">{communicationProfile.compatible_with}</p>
                          </div>
                        )}
                        {communicationProfile.bitrate && (() => {
                          const bitrateDisplay = translateBitrate(communicationProfile.bitrate);
                          return (
                            <div className="p-4 rounded-lg bg-gradient-to-br from-secondary/10 to-accent/5 border border-border">
                              <p className="text-xs text-muted-foreground mb-1">Bitrate</p>
                              <p className="text-lg font-bold text-secondary" title={`${communicationProfile.bitrate} - ${bitrateDisplay}`}>
                                {bitrateDisplay}
                              </p>
                            </div>
                          );
                        })()}
                      </div>
                    </div>

                    {/* Timing Information */}
                    <div>
                      <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Timing & Performance</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {communicationProfile.min_cycle_time && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-orange-500/10 to-amber-500/5 border border-border">
                            <p className="text-xs text-muted-foreground mb-1">Min Cycle Time</p>
                            <p className="text-lg font-bold text-warning" title={`${communicationProfile.min_cycle_time} microseconds`}>
                              {formatCycleTime(communicationProfile.min_cycle_time)}
                            </p>
                          </div>
                        )}
                        {communicationProfile.msequence_capability && (
                          <div className="p-4 rounded-lg bg-gradient-to-br from-green-500/10 to-emerald-500/5 border border-border">
                            <p className="text-xs text-muted-foreground mb-1">M-Sequence Capability</p>
                            <p className="text-lg font-bold text-success" title={`${communicationProfile.msequence_capability} bytes`}>
                              {decodeMSequence(communicationProfile.msequence_capability)}
                            </p>
                          </div>
                        )}
                        <div className={`p-4 rounded-lg border ${communicationProfile.sio_supported ? 'bg-success/10 border-success/30' : 'bg-secondary/50 border-border'}`}>
                          <p className="text-xs text-muted-foreground mb-1">SIO Support</p>
                          <p className={`text-lg font-bold ${communicationProfile.sio_supported ? 'text-success' : 'text-muted-foreground'}`}>
                            {communicationProfile.sio_supported ? 'Supported' : 'Not Supported'}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Physical Connection */}
                    {communicationProfile.connection_type && (() => {
                      const connInfo = getConnectionTypeInfo(communicationProfile.connection_type);
                      return (
                        <div>
                          <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Physical Connection</h3>
                          <div className="p-4 rounded-lg bg-gradient-to-br from-surface to-surface border border-border">
                            <p className="text-xs text-muted-foreground mb-2">Connection Type</p>
                            <p className="text-lg font-bold text-foreground">{communicationProfile.connection_type}</p>
                            {connInfo.description !== communicationProfile.connection_type && (
                              <p className="text-xs text-muted-foreground mt-2">{connInfo.description}</p>
                            )}
                            {connInfo.pins > 0 && (
                              <p className="text-xs text-success mt-1">{connInfo.pins} pins</p>
                            )}
                          </div>
                        </div>
                      );
                    })()}

                    {/* Wire Configuration */}
                    {communicationProfile.wire_config && Object.keys(communicationProfile.wire_config).length > 0 && (
                      <div>
                        <h3 className="text-sm font-semibold text-foreground uppercase tracking-wider mb-3">Wire Configuration</h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                          {Object.entries(communicationProfile.wire_config).map(([wire, func]) => {
                            const wireInfo = getWireColorInfo(wire);
                            return (
                              <div key={wire} className="p-3 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border hover:border-brand-green/50 transition-all">
                                <div className="flex items-center gap-2 mb-1">
                                  <div
                                    className="w-4 h-4 rounded-full border-2 border-border shadow-inner"
                                    style={{ backgroundColor: wireInfo.hex }}
                                    title={wireInfo.name}
                                  />
                                  <p className="text-xs text-muted-foreground font-mono">{wire}</p>
                                </div>
                                <p className="text-xs text-foreground mb-1">{wireInfo.name}</p>
                                <p className="text-xs font-semibold text-brand-green">{func}</p>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ) : (
              <div className="text-center py-12 text-muted-foreground">
                No communication profile information available for this device
              </div>
            )}
          </TabsContent>

  );
};
