import React from 'react';
import DocsCodeBlock from './DocsCodeBlock';
import DocsApiParams from './DocsApiParams';

/**
 * DocsApiResponse - API Response Display Component
 *
 * Features:
 * - Status code with color coding
 * - Response description
 * - Response schema/properties
 * - JSON response examples with syntax highlighting
 * - Multiple example support
 *
 * @param {Object} props
 * @param {number} props.status - HTTP status code
 * @param {string} props.statusText - Status text (e.g., "OK", "Created")
 * @param {string} props.description - Response description
 * @param {Object} props.example - Example response object/JSON
 * @param {Array} props.schema - Response schema properties [{name, type, description}]
 * @param {string} props.className - Additional CSS classes
 */
const DocsApiResponse = ({
  status,
  statusText,
  description,
  example,
  schema = [],
  className = ''
}) => {
  const getStatusColor = (code) => {
    if (code >= 200 && code < 300) {
      return 'bg-brand-green/10 text-brand-green border-brand-green/30';
    } else if (code >= 300 && code < 400) {
      return 'bg-blue-500/10 text-blue-500 border-blue-500/30';
    } else if (code >= 400 && code < 500) {
      return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/30';
    } else if (code >= 500) {
      return 'bg-red-500/10 text-red-500 border-red-500/30';
    }
    return 'bg-gray-500/10 text-gray-500 border-gray-500/30';
  };

  return (
    <div className={`docs-api-response ${className}`}>
      {/* Status and Description */}
      <div className="mb-4">
        {description && (
          <p className="text-sm text-muted-foreground mb-3">{description}</p>
        )}
      </div>

      {/* Response Schema */}
      {schema && schema.length > 0 && (
        <div className="mb-4">
          <h6 className="text-xs font-semibold text-foreground mb-2">
            Response Schema:
          </h6>
          <DocsApiParams params={schema} />
        </div>
      )}

      {/* Response Example */}
      {example && (
        <div>
          <h6 className="text-xs font-semibold text-foreground mb-2">
            Example Response:
          </h6>
          <DocsCodeBlock language="json" copy>
            {typeof example === 'string' ? example : JSON.stringify(example, null, 2)}
          </DocsCodeBlock>
        </div>
      )}

      {/* No content message */}
      {!description && !schema?.length && !example && (
        <p className="text-sm text-muted-foreground italic">
          No response body
        </p>
      )}
    </div>
  );
};

export default DocsApiResponse;
