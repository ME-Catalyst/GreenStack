import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Code, Play } from 'lucide-react';
import DocsApiMethod from './DocsApiMethod';
import DocsApiParams from './DocsApiParams';
import DocsApiResponse from './DocsApiResponse';
import DocsCodeBlock from './DocsCodeBlock';

/**
 * DocsApiEndpoint - API Endpoint Documentation Component
 *
 * Features:
 * - Method badge (GET, POST, PUT, DELETE, PATCH)
 * - Endpoint path with path parameters highlighted
 * - Description and usage notes
 * - Request parameters (path, query, body)
 * - Response examples with status codes
 * - Interactive "Try It" functionality
 * - Collapsible sections for better readability
 *
 * @param {Object} props
 * @param {string} props.method - HTTP method (GET, POST, PUT, DELETE, PATCH)
 * @param {string} props.path - API endpoint path (e.g., "/api/devices/{id}")
 * @param {string} props.title - Endpoint title/summary
 * @param {string} props.description - Detailed description
 * @param {Array} props.pathParams - Path parameters [{name, type, required, description}]
 * @param {Array} props.queryParams - Query parameters [{name, type, required, description}]
 * @param {Object} props.requestBody - Request body schema {type, required, properties, example}
 * @param {Array} props.responses - Response examples [{status, description, example}]
 * @param {Function} props.onTryIt - Callback for "Try It" button
 * @param {string} props.className - Additional CSS classes
 */
const DocsApiEndpoint = ({
  method = 'GET',
  path,
  title,
  description,
  pathParams = [],
  queryParams = [],
  requestBody = null,
  responses = [],
  onTryIt,
  className = ''
}) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [activeResponseTab, setActiveResponseTab] = useState(0);

  // Highlight path parameters in the path
  const renderPath = () => {
    const parts = path.split(/(\{[^}]+\})/g);
    return parts.map((part, index) => {
      if (part.startsWith('{') && part.endsWith('}')) {
        return (
          <span key={index} className="text-brand-green font-semibold">
            {part}
          </span>
        );
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className={`docs-api-endpoint border border-border rounded-lg mb-6 overflow-hidden ${className}`}>
      {/* Header */}
      <div
        className="flex items-center justify-between p-4 bg-surface hover:bg-surface-hover cursor-pointer transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3 flex-1">
          <DocsApiMethod method={method} />
          <code className="text-sm font-mono text-foreground">
            {renderPath()}
          </code>
        </div>
        <button className="p-1 hover:bg-surface rounded">
          {isExpanded ? (
            <ChevronDown className="w-5 h-5 text-muted-foreground" />
          ) : (
            <ChevronRight className="w-5 h-5 text-muted-foreground" />
          )}
        </button>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="border-t border-border">
          {/* Title and Description */}
          <div className="p-4 border-b border-border">
            {title && (
              <h4 className="text-lg font-semibold text-foreground mb-2">
                {title}
              </h4>
            )}
            {description && (
              <p className="text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>

          {/* Path Parameters */}
          {pathParams.length > 0 && (
            <div className="p-4 border-b border-border">
              <h5 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                <Code className="w-4 h-4" />
                Path Parameters
              </h5>
              <DocsApiParams params={pathParams} />
            </div>
          )}

          {/* Query Parameters */}
          {queryParams.length > 0 && (
            <div className="p-4 border-b border-border">
              <h5 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                <Code className="w-4 h-4" />
                Query Parameters
              </h5>
              <DocsApiParams params={queryParams} />
            </div>
          )}

          {/* Request Body */}
          {requestBody && (
            <div className="p-4 border-b border-border">
              <h5 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                <Code className="w-4 h-4" />
                Request Body
                {requestBody.required && (
                  <span className="text-xs px-2 py-0.5 bg-red-500/10 text-red-500 rounded">
                    Required
                  </span>
                )}
              </h5>
              {requestBody.description && (
                <p className="text-sm text-muted-foreground mb-3">
                  {requestBody.description}
                </p>
              )}
              {requestBody.properties && (
                <DocsApiParams params={requestBody.properties} />
              )}
              {requestBody.example && (
                <div className="mt-3">
                  <p className="text-xs font-semibold text-muted-foreground mb-2">
                    Example:
                  </p>
                  <DocsCodeBlock language="json" copy>
                    {JSON.stringify(requestBody.example, null, 2)}
                  </DocsCodeBlock>
                </div>
              )}
            </div>
          )}

          {/* Responses */}
          {responses.length > 0 && (
            <div className="p-4">
              <h5 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                <Code className="w-4 h-4" />
                Responses
              </h5>

              {/* Response Tabs */}
              <div className="flex gap-2 mb-3 flex-wrap">
                {responses.map((response, index) => (
                  <button
                    key={index}
                    onClick={() => setActiveResponseTab(index)}
                    className={`px-3 py-1.5 text-xs font-semibold rounded transition-colors ${
                      activeResponseTab === index
                        ? 'bg-brand-green text-white'
                        : 'bg-surface hover:bg-surface-hover text-muted-foreground'
                    }`}
                  >
                    {response.status} {response.statusText || getStatusText(response.status)}
                  </button>
                ))}
              </div>

              {/* Active Response */}
              {responses[activeResponseTab] && (
                <DocsApiResponse
                  status={responses[activeResponseTab].status}
                  statusText={responses[activeResponseTab].statusText}
                  description={responses[activeResponseTab].description}
                  example={responses[activeResponseTab].example}
                  schema={responses[activeResponseTab].schema}
                />
              )}
            </div>
          )}

          {/* Try It Button */}
          {onTryIt && (
            <div className="p-4 border-t border-border bg-surface/50">
              <button
                onClick={onTryIt}
                className="flex items-center gap-2 px-4 py-2 bg-brand-green hover:bg-brand-green/90 text-white rounded-lg font-medium transition-colors"
              >
                <Play className="w-4 h-4" />
                Try It Out
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * Get standard HTTP status text
 */
function getStatusText(status) {
  const statusTexts = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    409: 'Conflict',
    422: 'Unprocessable Entity',
    500: 'Internal Server Error',
    502: 'Bad Gateway',
    503: 'Service Unavailable'
  };
  return statusTexts[status] || '';
}

export default DocsApiEndpoint;
