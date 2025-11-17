import React from 'react';

/**
 * DocsApiMethod - HTTP Method Badge Component
 *
 * Features:
 * - Color-coded badges for different HTTP methods
 * - Consistent sizing and styling
 * - Uppercase method names
 * - Semantic colors (GET: blue, POST: green, PUT: yellow, DELETE: red, PATCH: purple)
 *
 * @param {Object} props
 * @param {string} props.method - HTTP method (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD)
 * @param {string} props.className - Additional CSS classes
 */
const DocsApiMethod = ({ method = 'GET', className = '' }) => {
  const methodConfig = {
    GET: {
      bgColor: 'bg-blue-500/10',
      textColor: 'text-blue-500',
      borderColor: 'border-blue-500/30'
    },
    POST: {
      bgColor: 'bg-brand-green/10',
      textColor: 'text-brand-green',
      borderColor: 'border-brand-green/30'
    },
    PUT: {
      bgColor: 'bg-yellow-500/10',
      textColor: 'text-yellow-500',
      borderColor: 'border-yellow-500/30'
    },
    PATCH: {
      bgColor: 'bg-purple-500/10',
      textColor: 'text-purple-500',
      borderColor: 'border-purple-500/30'
    },
    DELETE: {
      bgColor: 'bg-red-500/10',
      textColor: 'text-red-500',
      borderColor: 'border-red-500/30'
    },
    OPTIONS: {
      bgColor: 'bg-gray-500/10',
      textColor: 'text-gray-500',
      borderColor: 'border-gray-500/30'
    },
    HEAD: {
      bgColor: 'bg-gray-500/10',
      textColor: 'text-gray-500',
      borderColor: 'border-gray-500/30'
    }
  };

  const upperMethod = method.toUpperCase();
  const config = methodConfig[upperMethod] || methodConfig.GET;

  return (
    <span
      className={`docs-api-method inline-flex items-center px-2.5 py-1 text-xs font-bold rounded border ${config.bgColor} ${config.textColor} ${config.borderColor} ${className}`}
    >
      {upperMethod}
    </span>
  );
};

export default DocsApiMethod;
