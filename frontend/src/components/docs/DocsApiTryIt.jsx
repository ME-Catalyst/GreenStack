import React, { useState } from 'react';
import { Play, X, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { Dialog, DialogContent, Input, Textarea, Button } from '../ui';
import DocsCodeBlock from './DocsCodeBlock';
import DocsApiMethod from './DocsApiMethod';

/**
 * DocsApiTryIt - Interactive API Testing Component
 *
 * Features:
 * - Interactive parameter input forms
 * - Path parameter substitution
 * - Query parameter builder
 * - Request body editor (JSON)
 * - Live request/response display
 * - HTTP status code display
 * - Response timing
 * - Error handling
 * - Copy cURL command
 *
 * @param {Object} props
 * @param {boolean} props.isOpen - Whether the modal is open
 * @param {Function} props.onClose - Callback to close the modal
 * @param {string} props.method - HTTP method
 * @param {string} props.path - API endpoint path
 * @param {Array} props.pathParams - Path parameters
 * @param {Array} props.queryParams - Query parameters
 * @param {Object} props.requestBody - Request body schema
 * @param {string} props.baseUrl - Base API URL (default: window.location.origin)
 */
const DocsApiTryIt = ({
  isOpen,
  onClose,
  method = 'GET',
  path,
  pathParams = [],
  queryParams = [],
  requestBody = null,
  baseUrl = window.location.origin
}) => {
  const [pathValues, setPathValues] = useState({});
  const [queryValues, setQueryValues] = useState({});
  const [bodyValue, setBodyValue] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [responseTime, setResponseTime] = useState(null);

  const handleSend = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);
    setResponseTime(null);

    try {
      // Build URL with path parameters
      let url = path;
      pathParams.forEach(param => {
        const value = pathValues[param.name] || '';
        url = url.replace(`{${param.name}}`, encodeURIComponent(value));
      });

      // Add query parameters
      const queryString = Object.entries(queryValues)
        .filter(([key, value]) => value !== '' && value !== undefined)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
        .join('&');

      if (queryString) {
        url += `?${queryString}`;
      }

      // Build fetch options
      const options = {
        method: method.toUpperCase(),
        headers: {
          'Content-Type': 'application/json'
        }
      };

      // Add request body for POST/PUT/PATCH
      if (['POST', 'PUT', 'PATCH'].includes(method.toUpperCase()) && bodyValue) {
        try {
          options.body = bodyValue;
          // Validate JSON
          JSON.parse(bodyValue);
        } catch (e) {
          throw new Error(`Invalid JSON in request body: ${e.message}`);
        }
      }

      // Send request
      const startTime = performance.now();
      const res = await fetch(`${baseUrl}${url}`, options);
      const endTime = performance.now();
      setResponseTime((endTime - startTime).toFixed(0));

      // Parse response
      const contentType = res.headers.get('content-type');
      let data;
      if (contentType && contentType.includes('application/json')) {
        data = await res.json();
      } else {
        data = await res.text();
      }

      setResponse({
        status: res.status,
        statusText: res.statusText,
        headers: Object.fromEntries(res.headers.entries()),
        data
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getCurlCommand = () => {
    let url = path;
    pathParams.forEach(param => {
      const value = pathValues[param.name] || '';
      url = url.replace(`{${param.name}}`, value);
    });

    const queryString = Object.entries(queryValues)
      .filter(([key, value]) => value !== '' && value !== undefined)
      .map(([key, value]) => `${key}=${value}`)
      .join('&');

    if (queryString) {
      url += `?${queryString}`;
    }

    let curl = `curl -X ${method.toUpperCase()} "${baseUrl}${url}"`;

    if (['POST', 'PUT', 'PATCH'].includes(method.toUpperCase()) && bodyValue) {
      curl += ` \\\n  -H "Content-Type: application/json" \\\n  -d '${bodyValue}'`;
    }

    return curl;
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="space-y-4">
          {/* Header */}
          <div className="flex items-center justify-between pb-4 border-b border-border">
            <div className="flex items-center gap-3">
              <h3 className="text-xl font-semibold text-foreground">Try API Endpoint</h3>
              <DocsApiMethod method={method} />
            </div>
            <button
              onClick={onClose}
              className="p-1 hover:bg-surface rounded transition-colors"
            >
              <X className="w-5 h-5 text-muted-foreground" />
            </button>
          </div>

          {/* Endpoint */}
          <div>
            <label className="text-sm font-semibold text-foreground">Endpoint</label>
            <code className="block mt-1 text-sm font-mono text-muted-foreground">
              {baseUrl}{path}
            </code>
          </div>

          {/* Path Parameters */}
          {pathParams.length > 0 && (
            <div>
              <label className="text-sm font-semibold text-foreground mb-2 block">
                Path Parameters
              </label>
              <div className="space-y-2">
                {pathParams.map((param) => (
                  <div key={param.name}>
                    <label className="text-xs text-muted-foreground mb-1 block">
                      {param.name}
                      {param.required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    <Input
                      value={pathValues[param.name] || ''}
                      onChange={(e) => setPathValues({ ...pathValues, [param.name]: e.target.value })}
                      placeholder={param.description || param.name}
                      className="text-sm"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Query Parameters */}
          {queryParams.length > 0 && (
            <div>
              <label className="text-sm font-semibold text-foreground mb-2 block">
                Query Parameters
              </label>
              <div className="space-y-2">
                {queryParams.map((param) => (
                  <div key={param.name}>
                    <label className="text-xs text-muted-foreground mb-1 block">
                      {param.name}
                      {param.required && <span className="text-red-500 ml-1">*</span>}
                    </label>
                    <Input
                      value={queryValues[param.name] || ''}
                      onChange={(e) => setQueryValues({ ...queryValues, [param.name]: e.target.value })}
                      placeholder={param.description || param.name}
                      className="text-sm"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Request Body */}
          {requestBody && ['POST', 'PUT', 'PATCH'].includes(method.toUpperCase()) && (
            <div>
              <label className="text-sm font-semibold text-foreground mb-2 block">
                Request Body (JSON)
                {requestBody.required && <span className="text-red-500 ml-1">*</span>}
              </label>
              <Textarea
                value={bodyValue}
                onChange={(e) => setBodyValue(e.target.value)}
                placeholder={requestBody.example ? JSON.stringify(requestBody.example, null, 2) : '{}'}
                rows={8}
                className="font-mono text-xs"
              />
            </div>
          )}

          {/* cURL Command */}
          <div>
            <label className="text-sm font-semibold text-foreground mb-2 block">
              cURL Command
            </label>
            <DocsCodeBlock language="bash" copy>
              {getCurlCommand()}
            </DocsCodeBlock>
          </div>

          {/* Send Button */}
          <Button
            onClick={handleSend}
            disabled={loading}
            className="w-full bg-brand-green hover:bg-brand-green/90 text-white"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Sending...
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Send Request
              </>
            )}
          </Button>

          {/* Response */}
          {(response || error) && (
            <div className="border-t border-border pt-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-sm font-semibold text-foreground">Response</h4>
                {responseTime && (
                  <span className="text-xs text-muted-foreground">
                    {responseTime}ms
                  </span>
                )}
              </div>

              {error && (
                <div className="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-semibold text-red-500">Error</p>
                    <p className="text-sm text-foreground">{error}</p>
                  </div>
                </div>
              )}

              {response && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    {response.status >= 200 && response.status < 300 ? (
                      <CheckCircle className="w-5 h-5 text-brand-green" />
                    ) : (
                      <AlertCircle className="w-5 h-5 text-red-500" />
                    )}
                    <span className={`text-sm font-semibold ${
                      response.status >= 200 && response.status < 300
                        ? 'text-brand-green'
                        : 'text-red-500'
                    }`}>
                      {response.status} {response.statusText}
                    </span>
                  </div>

                  <div>
                    <p className="text-xs font-semibold text-foreground mb-2">Response Body:</p>
                    <DocsCodeBlock language="json" copy>
                      {typeof response.data === 'string'
                        ? response.data
                        : JSON.stringify(response.data, null, 2)}
                    </DocsCodeBlock>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default DocsApiTryIt;
