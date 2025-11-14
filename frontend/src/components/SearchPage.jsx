import React, { useState, useEffect, useRef } from 'react';
import { Search, X, Filter, ChevronRight, Package, Settings, Link as LinkIcon, List, Hash, FileText } from 'lucide-react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from './ui';
import { Button } from './ui';

/**
 * Global search page for searching across all device data
 * Searches: devices, parameters, assemblies, connections, enums
 */
const SearchPage = ({ API_BASE, onNavigate }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState(null);
  const [deviceTypeFilter, setDeviceTypeFilter] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchInputRef = useRef(null);
  const suggestionsTimeoutRef = useRef(null);

  // Fetch search suggestions as user types
  useEffect(() => {
    if (searchQuery.length >= 1) {
      // Debounce suggestions
      if (suggestionsTimeoutRef.current) {
        clearTimeout(suggestionsTimeoutRef.current);
      }

      suggestionsTimeoutRef.current = setTimeout(async () => {
        try {
          const response = await axios.get(`${API_BASE}/api/search/suggestions`, {
            params: { q: searchQuery, limit: 10 }
          });
          setSuggestions(response.data.suggestions);
          setShowSuggestions(true);
        } catch (error) {
          console.error('Failed to fetch suggestions:', error);
        }
      }, 300);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }

    return () => {
      if (suggestionsTimeoutRef.current) {
        clearTimeout(suggestionsTimeoutRef.current);
      }
    };
  }, [searchQuery, API_BASE]);

  const handleSearch = async (query = searchQuery) => {
    if (query.length < 2) return;

    setSearching(true);
    setShowSuggestions(false);

    try {
      const params = { q: query, limit: 50 };
      if (deviceTypeFilter) {
        params.device_type = deviceTypeFilter;
      }

      const response = await axios.get(`${API_BASE}/api/search`, { params });
      setResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
      setResults(null);
    } finally {
      setSearching(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion.text);
    setShowSuggestions(false);
    handleSearch(suggestion.text);
  };

  const clearSearch = () => {
    setSearchQuery('');
    setResults(null);
    setSuggestions([]);
    setShowSuggestions(false);
    searchInputRef.current?.focus();
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'eds_devices':
      case 'iodd_devices':
        return <Package className="w-5 h-5 text-blue-400" />;
      case 'parameters':
        return <Settings className="w-5 h-5 text-green-400" />;
      case 'assemblies':
        return <List className="w-5 h-5 text-purple-400" />;
      case 'connections':
        return <LinkIcon className="w-5 h-5 text-orange-400" />;
      case 'enums':
        return <Hash className="w-5 h-5 text-pink-400" />;
      default:
        return <FileText className="w-5 h-5 text-slate-400" />;
    }
  };

  const getCategoryTitle = (category) => {
    switch (category) {
      case 'eds_devices':
        return 'EDS Devices';
      case 'iodd_devices':
        return 'IODD Devices';
      case 'parameters':
        return 'Parameters';
      case 'assemblies':
        return 'Assemblies';
      case 'connections':
        return 'Connections';
      case 'enums':
        return 'Enum Values';
      default:
        return category;
    }
  };

  const handleResultClick = (item, category) => {
    // Navigate to appropriate page based on result type
    if (category === 'eds_devices') {
      onNavigate('eds', item.id);
    } else if (category === 'iodd_devices') {
      onNavigate('iodd', item.id);
    } else if (category === 'parameters' || category === 'assemblies' || category === 'connections' || category === 'enums') {
      // Navigate to the parent device
      if (item.device_type === 'EDS') {
        onNavigate('eds', item.device_id);
      } else if (item.device_type === 'IODD') {
        onNavigate('iodd', item.device_id);
      }
    }
  };

  const highlightMatch = (text, query) => {
    if (!text || !query) return text;

    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);

    return parts.map((part, i) =>
      regex.test(part) ? <mark key={i} className="bg-orange-500/30 text-orange-300">{part}</mark> : part
    );
  };

  const renderResultItem = (item, category) => {
    return (
      <div
        key={`${category}-${item.id}`}
        onClick={() => handleResultClick(item, category)}
        className="p-4 bg-slate-800/50 border border-slate-700 rounded-lg hover:bg-slate-800 hover:border-slate-600 transition-all cursor-pointer group"
      >
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            {/* Device Name/Parameter Name */}
            <div className="flex items-center gap-2 mb-1">
              <h4 className="text-white font-medium truncate">
                {highlightMatch(
                  item.product_name || item.param_name || item.assembly_name || item.connection_name || item.param_name,
                  searchQuery
                )}
              </h4>
              {item.type && (
                <span className={`px-2 py-0.5 text-xs rounded-full ${
                  item.type === 'EDS' ? 'bg-blue-500/20 text-blue-300' : 'bg-green-500/20 text-green-300'
                }`}>
                  {item.type}
                </span>
              )}
            </div>

            {/* Vendor/Device Info */}
            {(item.vendor_name || item.device_vendor) && (
              <p className="text-sm text-slate-400 mb-1">
                {highlightMatch(item.vendor_name || item.device_vendor, searchQuery)}
                {(item.product_code || item.device_product_code) &&
                  ` • ${item.product_code || item.device_product_code}`}
              </p>
            )}

            {/* Parameter Details */}
            {category === 'parameters' && (
              <div className="text-sm text-slate-500 space-y-1">
                <p>Parameter #{item.param_number} • {item.device_name}</p>
                {item.description && (
                  <p className="text-slate-400">{highlightMatch(item.description, searchQuery)}</p>
                )}
                {(item.units || item.min_value || item.max_value) && (
                  <p>
                    {item.units && <span>Unit: {item.units}</span>}
                    {item.min_value != null && <span> • Min: {item.min_value}</span>}
                    {item.max_value != null && <span> • Max: {item.max_value}</span>}
                  </p>
                )}
              </div>
            )}

            {/* Assembly Details */}
            {category === 'assemblies' && (
              <div className="text-sm text-slate-500">
                <p>Assembly #{item.assembly_number} • {item.device_name}</p>
                {item.description && (
                  <p className="text-slate-400 mt-1">{highlightMatch(item.description, searchQuery)}</p>
                )}
              </div>
            )}

            {/* Connection Details */}
            {category === 'connections' && (
              <div className="text-sm text-slate-500">
                <p>Connection #{item.connection_number} • {item.device_name}</p>
                <p className="text-slate-400">Type: {item.connection_type}</p>
              </div>
            )}

            {/* Enum Details */}
            {category === 'enums' && (
              <div className="text-sm text-slate-500">
                <p>Parameter #{item.param_number} • {item.device_name}</p>
                {item.enum_values && (
                  <p className="text-slate-400 mt-1">{highlightMatch(item.enum_values, searchQuery)}</p>
                )}
              </div>
            )}

            {/* Generic Description */}
            {item.description && !['parameters', 'assemblies'].includes(category) && (
              <p className="text-sm text-slate-400 mt-1 line-clamp-2">
                {highlightMatch(item.description, searchQuery)}
              </p>
            )}
          </div>

          <ChevronRight className="w-5 h-5 text-slate-500 group-hover:text-orange-400 transition-colors flex-shrink-0 ml-3" />
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
            <Search className="w-8 h-8 text-orange-500" />
            Global Search
          </h1>
          <p className="text-slate-400">
            Search across all devices, parameters, assemblies, connections, and more
          </p>
        </div>

        {/* Search Bar */}
        <Card className="bg-slate-900 border-slate-800 mb-6">
          <CardContent className="p-6">
            <div className="relative">
              <div className="flex gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-3 w-5 h-5 text-slate-400" />
                  <input
                    ref={searchInputRef}
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Search devices, parameters, assemblies..."
                    className="w-full pl-10 pr-10 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-orange-500"
                  />
                  {searchQuery && (
                    <button
                      onClick={clearSearch}
                      className="absolute right-3 top-3 text-slate-400 hover:text-white"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  )}

                  {/* Suggestions Dropdown */}
                  {showSuggestions && suggestions.length > 0 && (
                    <div className="absolute z-10 w-full mt-2 bg-slate-800 border border-slate-700 rounded-lg shadow-lg max-h-64 overflow-y-auto">
                      {suggestions.map((suggestion, index) => (
                        <div
                          key={index}
                          onClick={() => handleSuggestionClick(suggestion)}
                          className="px-4 py-2 hover:bg-slate-700 cursor-pointer flex items-center justify-between"
                        >
                          <span className="text-white">{suggestion.text}</span>
                          <span className="text-xs text-slate-400 capitalize">{suggestion.type}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <Button
                  onClick={() => handleSearch()}
                  disabled={searching || searchQuery.length < 2}
                  className="bg-orange-600 hover:bg-orange-700 px-6"
                >
                  {searching ? 'Searching...' : 'Search'}
                </Button>
              </div>

              {/* Device Type Filter */}
              <div className="flex items-center gap-3 mt-4">
                <Filter className="w-4 h-4 text-slate-400" />
                <span className="text-sm text-slate-400">Filter by type:</span>
                <div className="flex gap-2">
                  <button
                    onClick={() => setDeviceTypeFilter(null)}
                    className={`px-3 py-1 text-sm rounded ${
                      deviceTypeFilter === null
                        ? 'bg-orange-600 text-white'
                        : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                    }`}
                  >
                    All
                  </button>
                  <button
                    onClick={() => setDeviceTypeFilter('EDS')}
                    className={`px-3 py-1 text-sm rounded ${
                      deviceTypeFilter === 'EDS'
                        ? 'bg-blue-600 text-white'
                        : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                    }`}
                  >
                    EDS
                  </button>
                  <button
                    onClick={() => setDeviceTypeFilter('IODD')}
                    className={`px-3 py-1 text-sm rounded ${
                      deviceTypeFilter === 'IODD'
                        ? 'bg-green-600 text-white'
                        : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                    }`}
                  >
                    IODD
                  </button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        {results && (
          <div className="space-y-6">
            {/* Results Summary */}
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">
                {results.total_results} result{results.total_results !== 1 ? 's' : ''} for "{results.query}"
              </h2>
              {results.has_more && (
                <span className="text-sm text-orange-400">
                  Showing first 50 results per category
                </span>
              )}
            </div>

            {/* No Results */}
            {results.total_results === 0 && (
              <Card className="bg-slate-900 border-slate-800">
                <CardContent className="p-12 text-center">
                  <Search className="w-16 h-16 mx-auto mb-4 text-slate-600" />
                  <h3 className="text-xl font-semibold mb-2">No results found</h3>
                  <p className="text-slate-400">
                    Try different keywords or check your spelling
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Results by Category */}
            {Object.entries(results).map(([category, items]) => {
              if (category === 'query' || category === 'total_results' || category === 'has_more') return null;
              if (!Array.isArray(items) || items.length === 0) return null;

              return (
                <Card key={category} className="bg-slate-900 border-slate-800">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-3 text-white">
                      {getCategoryIcon(category)}
                      {getCategoryTitle(category)}
                      <span className="text-sm font-normal text-slate-400">
                        ({items.length} result{items.length !== 1 ? 's' : ''})
                      </span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {items.map((item) => renderResultItem(item, category))}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {/* Empty State (no search performed) */}
        {!results && !searching && (
          <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-12 text-center">
              <Search className="w-16 h-16 mx-auto mb-4 text-slate-600" />
              <h3 className="text-xl font-semibold mb-2">Search across all data</h3>
              <p className="text-slate-400 mb-4">
                Enter a search term above to find devices, parameters, assemblies, and more
              </p>
              <div className="text-sm text-slate-500 space-y-1">
                <p>• Search by device names, vendors, product codes</p>
                <p>• Find parameters by name, description, or units</p>
                <p>• Discover assemblies and connections</p>
                <p>• Search through enum values</p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
