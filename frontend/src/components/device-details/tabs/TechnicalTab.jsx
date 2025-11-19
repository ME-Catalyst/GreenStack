import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, CardDescription, Badge, TabsContent
} from '@/components/ui';
import {
  Settings, Info
} from 'lucide-react';


export const TechnicalTab = ({ device, processDataConditions, deviceVariants }) => {
  return (
              <TabsContent value="technical" className="space-y-6 mt-6">
            <Card className="bg-card/80 backdrop-blur-sm border-border">
              <CardHeader>
                <CardTitle className="text-foreground text-xl flex items-center gap-2">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center">
                    <Code2 className="w-5 h-5 text-success" />
                  </div>
                  Technical Information
                </CardTitle>
                <CardDescription className="text-muted-foreground">
                  Device specifications and metadata
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="p-4 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border">
                    <div className="flex items-center space-x-2 mb-2">
                      <Cpu className="w-4 h-4 text-brand-green" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wider">Vendor ID</p>
                    </div>
                    <p className="text-lg font-mono font-bold text-foreground">{device.vendor_id}</p>
                  </div>

                  <div className="p-4 rounded-lg bg-gradient-to-br from-secondary/10 to-accent/5 border border-border">
                    <div className="flex items-center space-x-2 mb-2">
                      <Package className="w-4 h-4 text-secondary" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wider">Device ID</p>
                    </div>
                    <p className="text-lg font-mono font-bold text-foreground">{device.device_id}</p>
                  </div>

                  <div className="p-4 rounded-lg bg-gradient-to-br from-green-500/10 to-emerald-500/5 border border-border">
                    <div className="flex items-center space-x-2 mb-2">
                      <FileCode className="w-4 h-4 text-success" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wider">IODD Version</p>
                    </div>
                    <p className="text-lg font-bold text-foreground">v{formatVersion(device.iodd_version)}</p>
                  </div>

                  <div className="p-4 rounded-lg bg-gradient-to-br from-orange-500/10 to-amber-500/5 border border-border">
                    <div className="flex items-center space-x-2 mb-2">
                      <Database className="w-4 h-4 text-warning" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wider">Total Parameters</p>
                    </div>
                    <p className="text-lg font-bold text-foreground">{parameters.length}</p>
                  </div>

                  <div className="p-4 rounded-lg bg-gradient-to-br from-brand-green/10 to-brand-green/5 border border-border">
                    <div className="flex items-center space-x-2 mb-2">
                      <Calendar className="w-4 h-4 text-brand-green" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wider">Import Date</p>
                    </div>
                    <p className="text-sm font-medium text-foreground">
                      {format(new Date(device.import_date), 'PPP')}
                    </p>
                  </div>

                  <div className="p-4 rounded-lg bg-gradient-to-br from-pink-500/10 to-rose-500/5 border border-border">
                    <div className="flex items-center space-x-2 mb-2">
                      <Activity className="w-4 h-4 text-pink-400" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wider">Asset Count</p>
                    </div>
                    <p className="text-lg font-bold text-foreground">{assets.length}</p>
                  </div>
                </div>

                {/* Standard Variables */}
                <div className="mt-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-success/20 flex items-center justify-center">
                      <Database className="w-4 h-4 text-success" />
                    </div>
                    Standard Variables
                  </h3>
                  <div className="overflow-x-auto rounded-lg border border-border">
                    <table className="w-full">
                      <thead>
                        <tr className="bg-gradient-to-r from-green-600 to-emerald-600">
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Variable</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Value</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Description</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr className="border-b border-border hover:bg-success/5">
                          <td className="py-3 px-4 text-sm font-medium text-foreground">Product Name</td>
                          <td className="py-3 px-4 text-sm text-foreground">{device.product_name}</td>
                          <td className="py-3 px-4 text-sm text-muted-foreground">Device product name</td>
                        </tr>
                        <tr className="border-b border-border hover:bg-success/5">
                          <td className="py-3 px-4 text-sm font-medium text-foreground">Manufacturer</td>
                          <td className="py-3 px-4 text-sm text-foreground">{device.manufacturer}</td>
                          <td className="py-3 px-4 text-sm text-muted-foreground">Manufacturer name</td>
                        </tr>
                        <tr className="border-b border-border hover:bg-success/5">
                          <td className="py-3 px-4 text-sm font-medium text-foreground">IODD Version</td>
                          <td className="py-3 px-4 text-sm font-mono text-foreground">{device.iodd_version}</td>
                          <td className="py-3 px-4 text-sm text-muted-foreground">IO-Link Device Description version</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

  );
};
