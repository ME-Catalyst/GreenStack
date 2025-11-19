import React from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, Button, Input, Badge, TabsContent
} from '@/components/ui';
import {
  Database, Download, Search, Filter
} from 'lucide-react';


export const ParametersTab = ({ device, parameters, exportHandlers, getDataTypeDisplay, getAccessRightInfo }) => {
  return (
              <TabsContent value="parameters" className="space-y-4 mt-6">
            <Card className="bg-card/80 backdrop-blur-sm border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-foreground text-xl flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-secondary/20 to-accent/20 flex items-center justify-center">
                        <Settings className="w-5 h-5 text-secondary" />
                      </div>
                      Device Parameters
                    </CardTitle>
                    <CardDescription className="text-muted-foreground mt-2">
                      {parameters.length} configuration parameters available
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge className="bg-secondary/20 text-secondary border-secondary/50 text-base px-4 py-1">
                      {filteredParameters.length} / {parameters.length}
                    </Badge>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleExportParameters('csv')}
                        disabled={filteredParameters.length === 0}
                        className="border-secondary/50 text-foreground-secondary hover:bg-secondary/10"
                        title="Export to CSV"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        CSV
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleExportParameters('json')}
                        disabled={filteredParameters.length === 0}
                        className="border-secondary/50 text-foreground-secondary hover:bg-secondary/10"
                        title="Export to JSON"
                      >
                        <Download className="w-4 h-4 mr-1" />
                        JSON
                      </Button>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {/* Search Box */}
                <div className="mb-6">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-5 h-5" />
                    <Input
                      type="text"
                      placeholder="Search parameters by name or index..."
                      value={paramSearchQuery}
                      onChange={(e) => setParamSearchQuery(e.target.value)}
                      className="pl-11 bg-secondary border-border text-foreground placeholder:text-muted-foreground focus:border-secondary/50 focus:ring-secondary/20 transition-all"
                    />
                  </div>

                  {/* Filter Toggle and Advanced Filters */}
                  <div className="mt-3">
                    <button
                      onClick={() => setParamShowFilters(!paramShowFilters)}
                      className="flex items-center gap-2 text-sm text-muted-foreground hover:text-secondary transition-colors"
                    >
                      <Filter className="w-4 h-4" />
                      {paramShowFilters ? 'Hide Filters' : 'Show Filters'}
                    </button>

                    {paramShowFilters && (
                      <div className="mt-3 p-4 rounded-lg bg-secondary/50 border border-border">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {/* Access Rights Filter */}
                          <div>
                            <label className="block text-xs text-muted-foreground mb-2">Access Rights</label>
                            <select
                              value={paramAccessFilter}
                              onChange={(e) => setParamAccessFilter(e.target.value)}
                              className="w-full px-3 py-2 rounded bg-card border border-border text-foreground text-sm focus:border-secondary/50 focus:ring-secondary/20 transition-all"
                            >
                              <option value="all">All Access Rights</option>
                              <option value="ro">🔒 Read Only (ro)</option>
                              <option value="rw">🔓 Read/Write (rw)</option>
                              <option value="wo">✏️ Write Only (wo)</option>
                            </select>
                          </div>

                          {/* Data Type Filter */}
                          <div>
                            <label className="block text-xs text-muted-foreground mb-2">Data Type</label>
                            <select
                              value={paramDataTypeFilter}
                              onChange={(e) => setParamDataTypeFilter(e.target.value)}
                              className="w-full px-3 py-2 rounded bg-card border border-border text-foreground text-sm focus:border-secondary/50 focus:ring-secondary/20 transition-all"
                            >
                              <option value="all">All Data Types</option>
                              <option value="boolean">Boolean</option>
                              <option value="integer">Integer</option>
                              <option value="uinteger">Unsigned Integer</option>
                              <option value="float">Float</option>
                              <option value="string">String</option>
                              <option value="octetstring">Octet String</option>
                              <option value="record">Record</option>
                              <option value="array">Array</option>
                            </select>
                          </div>
                        </div>

                        {/* Active Filters Summary */}
                        {(paramAccessFilter !== 'all' || paramDataTypeFilter !== 'all') && (
                          <div className="mt-3 pt-3 border-t border-border">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-xs text-muted-foreground">Active filters:</span>
                              {paramAccessFilter !== 'all' && (
                                <Badge className="bg-brand-green/20 text-foreground-secondary border-brand-green/50 text-xs">
                                  Access: {paramAccessFilter.toUpperCase()}
                                </Badge>
                              )}
                              {paramDataTypeFilter !== 'all' && (
                                <Badge className="bg-success/20 text-foreground-secondary border-success/50 text-xs">
                                  Type: {paramDataTypeFilter}
                                </Badge>
                              )}
                              <button
                                onClick={() => {
                                  setParamAccessFilter('all');
                                  setParamDataTypeFilter('all');
                                }}
                                className="text-xs text-muted-foreground hover:text-error transition-colors ml-auto"
                              >
                                Clear all filters
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {filteredParameters.length > 0 ? (
                  <div className="overflow-x-auto rounded-lg border border-border">
                    <table className="w-full">
                      <thead>
                        <tr className="bg-gradient-to-r from-secondary to-accent">
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Index</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Name</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Type</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Access</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Default</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Range/Options</th>
                          <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Value</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredParameters.map((param, index) => (
                          <tr
                            key={index}
                            className="border-b border-border hover:bg-gradient-to-r hover:from-secondary/10 hover:to-transparent transition-all"
                          >
                            <td className="py-3 px-4 text-sm font-mono text-brand-green font-semibold">{param.index}</td>
                            <td className="py-3 px-4 text-sm text-foreground font-medium">
                              <div className="flex items-center gap-2 flex-wrap">
                                <span>{param.name}</span>
                                {param.dynamic && (
                                  <Badge className="bg-brand-green/20 text-brand-green border-brand-green/50 text-xs" title="Parameter updates in real-time">
                                    🔄 Dynamic
                                  </Badge>
                                )}
                                {param.unit_code && (() => {
                                  const unitInfo = getUnitInfo(param.unit_code);
                                  return (
                                    <span className="text-xs text-secondary font-semibold" title={`Unit Code ${param.unit_code}: ${unitInfo.name}`}>
                                      [{unitInfo.symbol || param.unit_code}]
                                    </span>
                                  );
                                })()}
                                {param.bit_length && (
                                  <span className="text-xs text-muted-foreground">({param.bit_length} bits)</span>
                                )}
                              </div>
                            </td>
                            <td className="py-3 px-4 text-sm font-mono text-muted-foreground">{param.data_type}</td>
                            <td className="py-3 px-4 text-sm">
                              <Badge className={`text-xs ${
                                param.access_rights === 'rw' || param.access_rights === 'RW'
                                  ? 'bg-success/20 text-success border-success/50'
                                  : param.access_rights === 'ro' || param.access_rights === 'RO'
                                  ? 'bg-brand-green/20 text-brand-green border-brand-green/50'
                                  : 'bg-warning/20 text-warning border-warning/50'
                              }`}>
                                {param.access_rights}
                              </Badge>
                            </td>
                            <td className="py-3 px-4 text-sm">
                              {param.enumeration_values && param.default_value ? (
                                <div className="flex items-center space-x-2">
                                  <span className="font-mono text-brand-green">{param.default_value}</span>
                                  <span className="text-muted-foreground">=</span>
                                  <span className="text-foreground">
                                    {param.enumeration_values[param.default_value] || 'Unknown'}
                                  </span>
                                </div>
                              ) : (
                                <span className="font-mono text-muted-foreground">
                                  {param.default_value || '-'}
                                </span>
                              )}
                            </td>
                            <td className="py-3 px-4 text-sm">
                              {param.enumeration_values && Object.keys(param.enumeration_values).length > 0 ? (
                                <div className="space-y-1">
                                  <Badge className="bg-secondary/20 text-foreground-secondary border-secondary/50 text-xs">
                                    {Object.keys(param.enumeration_values).length} options
                                  </Badge>
                                  <div className="text-xs text-muted-foreground">
                                    {Object.entries(param.enumeration_values).slice(0, 2).map(([value, label]) => (
                                      <div key={value}>{value}: {label}</div>
                                    ))}
                                    {Object.keys(param.enumeration_values).length > 2 && (
                                      <div>...</div>
                                    )}
                                  </div>
                                </div>
                              ) : param.min_value && param.max_value ? (
                                <span className="font-mono text-muted-foreground">
                                  {param.min_value} - {param.max_value}
                                </span>
                              ) : (
                                <span className="text-muted-foreground">-</span>
                              )}
                            </td>
                            <td className="py-3 px-4 text-sm">
                              {(param.access_rights === 'rw' || param.access_rights === 'RW') ? (
                                param.enumeration_values && Object.keys(param.enumeration_values).length > 0 ? (
                                  <Select defaultValue={param.default_value || Object.keys(param.enumeration_values)[0]}>
                                    <SelectTrigger className="w-full bg-secondary border-border text-foreground hover:border-secondary/50 transition-all">
                                      <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent className="bg-secondary border-border">
                                      {Object.entries(param.enumeration_values).map(([value, label]) => (
                                        <SelectItem
                                          key={value}
                                          value={value}
                                          className="text-foreground hover:bg-secondary/20 cursor-pointer"
                                        >
                                          <div className="flex items-center space-x-2">
                                            <span className="font-mono text-brand-green text-xs">{value}:</span>
                                            <span>{label}</span>
                                          </div>
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                ) : param.data_type === 'BooleanT' ? (
                                  <Select defaultValue={param.default_value || '0'}>
                                    <SelectTrigger className="w-full bg-secondary border-border text-foreground hover:border-secondary/50 transition-all">
                                      <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent className="bg-secondary border-border">
                                      <SelectItem value="0" className="text-foreground hover:bg-secondary/20 cursor-pointer">
                                        False (0)
                                      </SelectItem>
                                      <SelectItem value="1" className="text-foreground hover:bg-secondary/20 cursor-pointer">
                                        True (1)
                                      </SelectItem>
                                    </SelectContent>
                                  </Select>
                                ) : param.data_type === 'StringT' ? (
                                  <Input
                                    type="text"
                                    defaultValue={param.default_value || ''}
                                    placeholder="Enter value..."
                                    className="w-full bg-secondary border-border text-foreground focus:border-secondary/50 focus:ring-secondary/20 transition-all"
                                  />
                                ) : (
                                  <Input
                                    type="number"
                                    defaultValue={param.default_value || ''}
                                    min={param.min_value || undefined}
                                    max={param.max_value || undefined}
                                    placeholder="Enter value..."
                                    className="w-full bg-secondary border-border text-foreground focus:border-secondary/50 focus:ring-secondary/20 transition-all font-mono"
                                  />
                                )
                              ) : (
                                <div className="flex items-center space-x-2">
                                  <Badge className="bg-muted/50 text-muted-foreground border-border text-xs">
                                    Read Only
                                  </Badge>
                                  {param.enumeration_values && param.default_value && (
                                    <span className="text-xs text-muted-foreground">
                                      ({param.enumeration_values[param.default_value]})
                                    </span>
                                  )}
                                </div>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <Database className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground">
                      {paramSearchQuery ? 'No parameters match your search' : 'No parameters found'}
                    </p>
                    {paramSearchQuery && (
                      <Button
                        variant="link"
                        onClick={() => setParamSearchQuery('')}
                        className="mt-2 text-secondary"
                      >
                        Clear search
                      </Button>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

  );
};
