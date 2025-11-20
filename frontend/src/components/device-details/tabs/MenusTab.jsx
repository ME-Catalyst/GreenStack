import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, Button, TabsContent, ScrollArea
} from '@/components/ui';
import {
  Menu, Download
} from 'lucide-react';
import IODDMenuRenderer from '../IODDMenuRenderer';


export const MenusTab = ({ device, uiMenus, MenuItemDisplay, InteractiveParameterControl, API_BASE }) => {
  return (
              <TabsContent value="menus" className="space-y-4 mt-6">
            {/* IODD Menu Renderer - Role-based interactive menu interface */}
            {device && device.id && (
              <IODDMenuRenderer deviceId={device.id} API_BASE={API_BASE} />
            )}
            {/* System Command Buttons */}
            {menuButtons && menuButtons.length > 0 && (
              <Card className="bg-card/80 backdrop-blur-sm border-border hover:border-orange-500/30 transition-all">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500/20 to-red-500/20 flex items-center justify-center">
                        <Command className="w-5 h-5 text-orange-400" />
                      </div>
                      System Commands
                    </CardTitle>
                    <Badge className="bg-orange-500/20 text-orange-400 border-orange-500/50">
                      {menuButtons.length} {menuButtons.length === 1 ? 'Command' : 'Commands'}
                    </Badge>
                  </div>
                  <CardDescription className="text-muted-foreground mt-2">
                    System-level commands for device management and maintenance
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {menuButtons.map((button, idx) => (
                      <div
                        key={idx}
                        className="p-4 rounded-lg bg-gradient-to-br from-orange-500/10 to-red-500/5 border border-border hover:border-orange-500/50 transition-all group"
                      >
                        <div className="flex items-start gap-3">
                          <div className="mt-1">
                            <div className="w-10 h-10 rounded-lg bg-orange-500/20 border border-orange-500/30 flex items-center justify-center group-hover:bg-orange-500/30 transition-colors">
                              {button.button_function === 'FactoryReset' && <RotateCcw className="w-5 h-5 text-orange-400" />}
                              {button.button_function === 'Identify' && <Radio className="w-5 h-5 text-orange-400" />}
                              {button.button_function === 'TeachIn' && <Book className="w-5 h-5 text-orange-400" />}
                              {button.button_function === 'LocalParameterization' && <Wrench className="w-5 h-5 text-orange-400" />}
                              {button.button_function === 'RestoreFactorySettings' && <RotateCcw className="w-5 h-5 text-orange-400" />}
                              {!['FactoryReset', 'Identify', 'TeachIn', 'LocalParameterization', 'RestoreFactorySettings'].includes(button.button_function) && (
                                <Command className="w-5 h-5 text-orange-400" />
                              )}
                            </div>
                          </div>
                          <div className="flex-1">
                            <h4 className="text-foreground font-semibold text-sm mb-1">
                              {button.button_function || 'System Command'}
                            </h4>
                            {button.button_value !== null && (
                              <div className="text-xs text-muted-foreground mb-2">
                                <span className="font-mono">Value: {button.button_value}</span>
                              </div>
                            )}
                            <div className="flex items-center gap-2">
                              <Badge className="bg-muted text-foreground text-xs">
                                Menu: {button.menu_id || 'N/A'}
                              </Badge>
                              {button.access_rights && (
                                <Badge className={`text-xs ${
                                  button.access_rights === 'ro' ? 'bg-blue-500/20 text-blue-400 border-blue-500/50' :
                                  button.access_rights === 'rw' ? 'bg-green-500/20 text-green-400 border-green-500/50' :
                                  'bg-muted text-foreground'
                                }`}>
                                  {button.access_rights.toUpperCase()}
                                </Badge>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {configSchema && configSchema.menus && configSchema.menus.length > 0 ? (
              <div className="space-y-4">
                {/* Configuration Toolbar */}
                <Card className="bg-gradient-to-r from-secondary/10 to-secondary/10 border-secondary/30">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 flex-1">
                        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-secondary/20 to-secondary/20 flex items-center justify-center">
                          <Settings className="w-5 h-5 text-secondary" />
                        </div>
                        <div className="flex-1">
                          <Input
                            value={configurationName}
                            onChange={(e) => setConfigurationName(e.target.value)}
                            className="bg-secondary/50 border-secondary/30 text-foreground font-semibold max-w-md"
                            placeholder="Configuration name..."
                          />
                          <p className="text-xs text-muted-foreground mt-1">
                            {hasUnsavedChanges ? (
                              <span className="text-warning">Unsaved changes</span>
                            ) : (
                              'All changes auto-saved'
                            )}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={resetConfiguration}
                          className="bg-secondary border-border hover:bg-muted"
                        >
                          <RotateCcw className="w-4 h-4 mr-2" />
                          Reset
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={exportConfiguration}
                          className="bg-secondary/10 border-secondary/50 hover:bg-secondary/20 text-secondary"
                        >
                          <Download className="w-4 h-4 mr-2" />
                          Export
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Main Configuration Interface */}
                <div className="grid grid-cols-12 gap-4">
                  {/* Left: Configuration Interface */}
                  <div className="col-span-12 lg:col-span-8">
                    <Card className="bg-card/80 backdrop-blur-sm border-border">
                      <CardHeader className="pb-3">
                        <CardTitle className="text-foreground text-lg">Device Configuration</CardTitle>
                        <CardDescription className="text-muted-foreground">
                          Adjust device parameters - changes are not applied to the physical device
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        {/* Menu Tabs */}
                        <Tabs value={activeConfigMenu} onValueChange={setActiveConfigMenu} className="w-full">
                          <TabsList className="bg-secondary/50 border border-border p-1 flex flex-wrap h-auto">
                            {configSchema.menus.map((menu) => (
                              <TabsTrigger
                                key={menu.id}
                                value={menu.id}
                                className="data-[state=active]:bg-secondary/20 data-[state=active]:text-secondary text-muted-foreground text-sm"
                              >
                                {menu.name}
                                <Badge className="ml-2 bg-muted text-foreground text-xs">
                                  {menu.items.length}
                                </Badge>
                              </TabsTrigger>
                            ))}
                          </TabsList>

                          {/* Menu Content - Show ALL items */}
                          {configSchema.menus.map((menu) => (
                            <TabsContent key={menu.id} value={menu.id} className="mt-4 space-y-3">
                              {menu.items.length === 0 ? (
                                <div className="text-center py-12 text-muted-foreground">
                                  No items in this menu
                                </div>
                              ) : (
                                menu.items.map((item, idx) => (
                                  <MenuItemDisplay key={idx} item={item} index={idx} />
                                ))
                              )}
                            </TabsContent>
                          ))}
                        </Tabs>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Right: Parameter Details Panel */}
                  <div className="col-span-12 lg:col-span-4">
                    <Card className="bg-card/80 backdrop-blur-sm border-border sticky top-4">
                      <CardHeader>
                        <CardTitle className="text-foreground text-lg flex items-center gap-2">
                          <Info className="w-5 h-5 text-secondary" />
                          Parameter Details
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        {selectedParameter && selectedParameter.parameter ? (
                          <div className="space-y-4">
                            <div>
                              <h3 className="text-lg font-semibold text-foreground mb-1">
                                {selectedParameter.parameter.name}
                              </h3>
                              <Badge className="font-mono text-xs bg-brand-green/20 text-foreground-secondary border-brand-green/50">
                                {selectedParameter.variable_id}
                              </Badge>
                            </div>

                            {selectedParameter.parameter.description && (
                              <div>
                                <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">Description</p>
                                <p className="text-sm text-foreground">{selectedParameter.parameter.description}</p>
                              </div>
                            )}

                            <div className="grid grid-cols-2 gap-3 text-sm">
                              <div className="p-2 rounded bg-secondary/50 border border-border">
                                <p className="text-xs text-muted-foreground mb-1">Data Type</p>
                                <p className="text-foreground font-mono text-xs">{selectedParameter.parameter.data_type}</p>
                              </div>
                              <div className="p-2 rounded bg-secondary/50 border border-border">
                                <p className="text-xs text-muted-foreground mb-1">Access</p>
                                <Badge className={`text-xs ${selectedParameter.access_right_restriction === 'ro' ? 'bg-brand-green/20 text-brand-green' : selectedParameter.access_right_restriction === 'wo' ? 'bg-warning/20 text-warning' : 'bg-success/20 text-success'}`}>
                                  {selectedParameter.access_right_restriction}
                                </Badge>
                              </div>
                              {selectedParameter.parameter.default_value && (
                                <div className="p-2 rounded bg-secondary/50 border border-border">
                                  <p className="text-xs text-muted-foreground mb-1">Default</p>
                                  <p className="text-foreground font-mono text-xs">{selectedParameter.parameter.default_value}</p>
                                </div>
                              )}
                              {selectedParameter.parameter.bit_length && (
                                <div className="p-2 rounded bg-secondary/50 border border-border">
                                  <p className="text-xs text-muted-foreground mb-1">Bit Length</p>
                                  <p className="text-foreground font-mono text-xs">{selectedParameter.parameter.bit_length}</p>
                                </div>
                              )}
                            </div>

                            {(selectedParameter.parameter.min_value !== null || selectedParameter.parameter.max_value !== null) && (
                              <div className="p-3 rounded-lg bg-brand-green/10 border border-brand-green/30">
                                <p className="text-xs text-brand-green font-semibold mb-2">Value Range</p>
                                <div className="flex items-center justify-between text-sm">
                                  <span className="text-foreground">Min: <span className="font-mono">{selectedParameter.parameter.min_value}</span></span>
                                  <span className="text-foreground">Max: <span className="font-mono">{selectedParameter.parameter.max_value}</span></span>
                                </div>
                              </div>
                            )}

                            {selectedParameter.parameter.enumeration_values && Object.keys(selectedParameter.parameter.enumeration_values).length > 0 && (
                              <div className="p-3 rounded-lg bg-success/10 border border-success/30">
                                <p className="text-xs text-success font-semibold mb-2">Valid Values</p>
                                <div className="space-y-1 max-h-40 overflow-y-auto">
                                  {Object.entries(selectedParameter.parameter.enumeration_values).map(([value, name]) => (
                                    <div key={value} className="text-xs text-foreground flex items-center gap-2">
                                      <span className="font-mono bg-secondary px-2 py-1 rounded">{value}</span>
                                      <span>{name}</span>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}

                            <div className="pt-3 border-t border-border">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => copyToClipboard(selectedParameter.variable_id)}
                                className="w-full bg-secondary border-border hover:bg-muted"
                              >
                                <Copy className="w-4 h-4 mr-2" />
                                Copy Variable ID
                              </Button>
                            </div>
                          </div>
                        ) : (
                          <div className="text-center py-12 text-muted-foreground">
                            <Info className="w-12 h-12 mx-auto mb-3 opacity-50" />
                            <p className="text-sm">Click on any parameter to view details</p>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-muted-foreground">
                {configSchema === null ? (
                  <div>
                    <Skeleton className="h-8 w-64 mx-auto mb-2 bg-secondary" />
                    <Skeleton className="h-4 w-48 mx-auto bg-secondary" />
                  </div>
                ) : (
                  'No menu structure information available for this device'
                )}
              </div>
            )}
          </TabsContent>

  );
};
