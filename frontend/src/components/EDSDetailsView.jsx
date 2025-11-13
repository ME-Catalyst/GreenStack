import React, { useState } from 'react';
import {
  ArrowLeft, Download, FileText, Server, ArrowUpRight, ArrowDownRight,
  Users, Activity, Clock, Package, Code, Database, FileCode
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui';
import { Button } from '@/components/ui';
import { Badge } from '@/components/ui';

const EDSDetailsView = ({ selectedEds, onBack, onExportJSON, onExportZIP, API_BASE }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Package },
    { id: 'parameters', label: `Parameters (${selectedEds.parameters?.length || 0})`, icon: Database },
    { id: 'connections', label: `Connections (${selectedEds.connections?.length || 0})`, icon: Activity },
    { id: 'capacity', label: 'Capacity & Performance', icon: Server },
    { id: 'raw', label: 'Raw EDS Content', icon: FileCode },
  ];

  return (
    <div className="space-y-6">
      {/* Header with actions */}
      <div className="flex items-center justify-between">
        <Button
          variant="ghost"
          onClick={onBack}
          className="text-slate-400 hover:text-white"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to EDS Files
        </Button>
        <div className="flex gap-2">
          <Button
            onClick={onExportJSON}
            variant="outline"
            className="border-slate-700 text-slate-300 hover:bg-slate-800"
          >
            <Download className="w-4 h-4 mr-2" />
            Export JSON
          </Button>
          <Button
            onClick={onExportZIP}
            className="bg-purple-600 hover:bg-purple-700 text-white"
          >
            <Download className="w-4 h-4 mr-2" />
            Export ZIP
          </Button>
        </div>
      </div>

      {/* Product Header Card */}
      <Card className="bg-slate-900 border-slate-800">
        <CardHeader>
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center overflow-hidden">
              <img
                src={`${API_BASE}/api/eds/${selectedEds.id}/icon`}
                alt={selectedEds.product_name || 'Device'}
                className="w-12 h-12 object-contain"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <FileText className="w-8 h-8 text-purple-400" style={{display: 'none'}} />
            </div>
            <div className="flex-1">
              <CardTitle className="text-white text-2xl">{selectedEds.product_name || 'Unknown Product'}</CardTitle>
              <CardDescription className="text-slate-400 mt-1 flex items-center gap-2">
                <span>{selectedEds.vendor_name || 'Unknown Vendor'}</span>
                <span>•</span>
                <span>{selectedEds.catalog_number || 'N/A'}</span>
                <span>•</span>
                <span>Rev {selectedEds.major_revision}.{selectedEds.minor_revision}</span>
              </CardDescription>
            </div>
            {/* Quick stats */}
            <div className="hidden md:flex gap-4">
              {selectedEds.capacity && selectedEds.capacity.max_msg_connections && (
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-400">{selectedEds.capacity.max_msg_connections}</div>
                  <div className="text-xs text-slate-500">Msg Conn</div>
                </div>
              )}
              {selectedEds.capacity && selectedEds.capacity.max_io_producers && (
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-400">{selectedEds.capacity.max_io_producers}</div>
                  <div className="text-xs text-slate-500">IO Prod</div>
                </div>
              )}
              {selectedEds.capacity && selectedEds.capacity.max_io_consumers && (
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">{selectedEds.capacity.max_io_consumers}</div>
                  <div className="text-xs text-slate-500">IO Cons</div>
                </div>
              )}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Tab Navigation */}
      <div className="border-b border-slate-800">
        <div className="flex space-x-1 overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap
                  ${activeTab === tab.id
                    ? 'border-purple-500 text-white'
                    : 'border-transparent text-slate-400 hover:text-slate-300 hover:border-slate-700'
                  }
                `}
              >
                <Icon className="w-4 h-4 mr-2" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Content */}
      <div className="min-h-[600px]">
        {activeTab === 'overview' && <OverviewTab selectedEds={selectedEds} />}
        {activeTab === 'parameters' && <ParametersTab selectedEds={selectedEds} />}
        {activeTab === 'connections' && <ConnectionsTab selectedEds={selectedEds} />}
        {activeTab === 'capacity' && <CapacityTab selectedEds={selectedEds} />}
        {activeTab === 'raw' && <RawContentTab selectedEds={selectedEds} />}
      </div>
    </div>
  );
};

// Overview Tab Component
const OverviewTab = ({ selectedEds }) => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="pb-3">
            <CardTitle className="text-white text-sm flex items-center">
              <Clock className="w-4 h-4 mr-2 text-purple-400" />
              File History
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div>
              <p className="text-xs text-slate-500">Created</p>
              <p className="text-sm text-white">{selectedEds.create_date || 'N/A'} {selectedEds.create_time || ''}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Modified</p>
              <p className="text-sm text-white">{selectedEds.mod_date || 'N/A'} {selectedEds.mod_time || ''}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">File Revision</p>
              <p className="text-sm text-white">{selectedEds.file_revision || 'N/A'}</p>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="pb-3">
            <CardTitle className="text-white text-sm flex items-center">
              <FileText className="w-4 h-4 mr-2 text-blue-400" />
              Device Classification
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div>
              <p className="text-xs text-slate-500">Class 1</p>
              <p className="text-sm text-white">{selectedEds.class1 || 'N/A'}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Class 2</p>
              <p className="text-sm text-white">{selectedEds.class2 || 'N/A'}</p>
            </div>
            {selectedEds.class3 && (
              <div>
                <p className="text-xs text-slate-500">Class 3</p>
                <p className="text-sm text-white">{selectedEds.class3}</p>
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="pb-3">
            <CardTitle className="text-white text-sm flex items-center">
              <Database className="w-4 h-4 mr-2 text-green-400" />
              Quick Stats
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div>
              <p className="text-xs text-slate-500">Parameters</p>
              <p className="text-sm text-white">{selectedEds.parameters?.length || 0}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Connections</p>
              <p className="text-sm text-white">{selectedEds.connections?.length || 0}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500">Ports</p>
              <p className="text-sm text-white">{selectedEds.ports?.length || 0}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Description */}
      {selectedEds.description && (
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-white text-sm">Description</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-slate-300">{selectedEds.description}</p>
          </CardContent>
        </Card>
      )}

      {/* Home URL */}
      {selectedEds.home_url && (
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-white text-sm">Manufacturer Website</CardTitle>
          </CardHeader>
          <CardContent>
            <a
              href={selectedEds.home_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-purple-400 hover:text-purple-300 underline"
            >
              {selectedEds.home_url}
            </a>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

// Parameters Tab Component
const ParametersTab = ({ selectedEds }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredParams = selectedEds.parameters?.filter(param =>
    param.param_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    param.description?.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="flex items-center gap-4">
        <input
          type="text"
          placeholder={`Search ${selectedEds.parameters?.length || 0} parameters...`}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
        <Badge variant="secondary" className="bg-slate-800 text-slate-300">
          {filteredParams.length} / {selectedEds.parameters?.length || 0}
        </Badge>
      </div>

      {/* Parameters Table */}
      <Card className="bg-slate-900 border-slate-800">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-slate-800">
              <tr className="text-left text-xs text-slate-500 uppercase">
                <th className="p-4">#</th>
                <th className="p-4">Parameter Name</th>
                <th className="p-4">Type</th>
                <th className="p-4">Size</th>
                <th className="p-4">Default</th>
                <th className="p-4">Range</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredParams.length > 0 ? (
                filteredParams.map((param, index) => (
                  <tr key={index} className="hover:bg-slate-800/50 transition-colors">
                    <td className="p-4 text-slate-400">{param.param_number || index + 1}</td>
                    <td className="p-4 text-white font-medium">{param.param_name || 'Unnamed'}</td>
                    <td className="p-4 text-slate-300">{param.data_type || 'N/A'}</td>
                    <td className="p-4 text-slate-300">{param.data_size || 'N/A'}</td>
                    <td className="p-4 text-slate-300">{param.default_value || 'N/A'}</td>
                    <td className="p-4 text-slate-300">
                      {param.min_value !== null && param.max_value !== null
                        ? `${param.min_value} - ${param.max_value}`
                        : 'N/A'}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="p-8 text-center text-slate-500">
                    {searchTerm ? 'No parameters match your search' : 'No parameters available'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

// Connections Tab Component
const ConnectionsTab = ({ selectedEds }) => {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {selectedEds.connections && selectedEds.connections.length > 0 ? (
          selectedEds.connections.map((conn, index) => (
            <Card key={index} className="bg-slate-900 border-slate-800">
              <CardHeader>
                <CardTitle className="text-white text-sm flex items-center">
                  <Activity className="w-4 h-4 mr-2 text-green-400" />
                  {conn.connection_name || `Connection ${index + 1}`}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                {conn.trigger_transport && (
                  <div>
                    <span className="text-slate-500">Trigger/Transport: </span>
                    <span className="text-slate-300">{conn.trigger_transport}</span>
                  </div>
                )}
                {conn.connection_params && (
                  <div>
                    <span className="text-slate-500">Params: </span>
                    <span className="text-slate-300">{conn.connection_params}</span>
                  </div>
                )}
                {conn.help_string && (
                  <div className="pt-2 border-t border-slate-800">
                    <p className="text-slate-400 text-xs">{conn.help_string}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))
        ) : (
          <Card className="bg-slate-900 border-slate-800 col-span-2">
            <CardContent className="p-8 text-center text-slate-500">
              No connections available
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

// Capacity Tab Component
const CapacityTab = ({ selectedEds }) => {
  const capacity = selectedEds.capacity;

  return (
    <div className="space-y-6">
      {/* Capacity Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-purple-900/20 to-purple-800/10 border-purple-800/30">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-300 mb-1">Max Message Connections</p>
                <p className="text-3xl font-bold text-white">{capacity?.max_msg_connections ?? 'N/A'}</p>
              </div>
              <Server className="w-8 h-8 text-purple-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-900/20 to-green-800/10 border-green-800/30">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-300 mb-1">Max I/O Producers</p>
                <p className="text-3xl font-bold text-white">{capacity?.max_io_producers ?? 'N/A'}</p>
              </div>
              <ArrowUpRight className="w-8 h-8 text-green-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-blue-900/20 to-blue-800/10 border-blue-800/30">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-300 mb-1">Max I/O Consumers</p>
                <p className="text-3xl font-bold text-white">{capacity?.max_io_consumers ?? 'N/A'}</p>
              </div>
              <ArrowDownRight className="w-8 h-8 text-blue-400" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-cyan-900/20 to-cyan-800/10 border-cyan-800/30">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-cyan-300 mb-1">Max Config Tool Conn</p>
                <p className="text-3xl font-bold text-white">{capacity?.max_cx_per_config_tool ?? 'N/A'}</p>
              </div>
              <Users className="w-8 h-8 text-cyan-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* TSpecs */}
      {capacity?.tspecs && capacity.tspecs.length > 0 && (
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Activity className="w-5 h-5 mr-2 text-purple-400" />
              Bandwidth Specifications (TSpecs)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {capacity.tspecs.map((tspec, index) => (
                <div key={index} className="p-4 bg-slate-800 rounded-lg border border-slate-700">
                  <div className="flex items-center justify-between mb-2">
                    <Badge className="bg-purple-900/50 text-purple-300 border-purple-800">
                      {tspec.tspec_name}
                    </Badge>
                    <span className="text-sm text-slate-400">{tspec.direction}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 mt-3">
                    <div>
                      <p className="text-xs text-slate-500">Data Size</p>
                      <p className="text-white font-semibold">{tspec.data_size} bytes</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Rate</p>
                      <p className="text-white font-semibold">{tspec.rate} ms</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* No capacity data message */}
      {!capacity && (
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-8 text-center text-slate-500">
            No capacity data available for this device
          </CardContent>
        </Card>
      )}
    </div>
  );
};

// Raw Content Tab Component
const RawContentTab = ({ selectedEds }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (selectedEds.eds_content) {
      navigator.clipboard.writeText(selectedEds.eds_content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Raw EDS File Content</h3>
        <Button
          onClick={handleCopy}
          variant="outline"
          className="border-slate-700 text-slate-300 hover:bg-slate-800"
        >
          <Code className="w-4 h-4 mr-2" />
          {copied ? 'Copied!' : 'Copy to Clipboard'}
        </Button>
      </div>

      <Card className="bg-slate-950 border-slate-800">
        <CardContent className="p-0">
          <div className="relative">
            <pre className="p-6 overflow-auto max-h-[70vh] text-xs leading-relaxed">
              <code className="text-slate-300 font-mono">
                {selectedEds.eds_content || '// No raw content available'}
              </code>
            </pre>
          </div>
        </CardContent>
      </Card>

      <p className="text-sm text-slate-500">
        This is the raw EDS file content as it was uploaded. Line count: {selectedEds.eds_content?.split('\n').length || 0}
      </p>
    </div>
  );
};

export default EDSDetailsView;
