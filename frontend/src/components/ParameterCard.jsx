import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Info, TrendingUp, Link2, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui';
import { Badge } from './ui';
import { getDataTypeInfo, getDataTypeBadgeColor, formatValueByType } from '../utils/edsDataTypeDecoder';
import { parseEnumValues, isBooleanParameter, extractUnits, getParameterDescription, parseRangeConstraints } from '../utils/edsEnumParser';
import { getCategoryBadgeColor } from '../utils/edsParameterCategorizer';

/**
 * Visual Range Indicator Component
 * Shows a visual slider indicating where the default value falls within the min-max range
 */
const RangeIndicator = ({ min, max, defaultValue, units = '' }) => {
  if (min === null || max === null || defaultValue === null) return null;
  if (isNaN(min) || isNaN(max) || isNaN(defaultValue)) return null;
  if (min === max) return null;

  const range = max - min;
  const position = ((defaultValue - min) / range) * 100;
  const clampedPosition = Math.max(0, Math.min(100, position));

  // Determine label based on position
  let positionLabel = 'Normal';
  if (clampedPosition < 25) positionLabel = 'Low';
  else if (clampedPosition > 75) positionLabel = 'High';

  return (
    <div className="mt-3">
      <div className="flex justify-between text-xs text-slate-500 mb-1">
        <span>{formatValueByType(min, { category: 'Integer' }, units)}</span>
        <span className="text-slate-400">{positionLabel}</span>
        <span>{formatValueByType(max, { category: 'Integer' }, units)}</span>
      </div>
      <div className="relative h-2 bg-slate-800 rounded-full overflow-hidden">
        {/* Filled portion */}
        <div
          className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-600 to-blue-500 transition-all"
          style={{ width: `${clampedPosition}%` }}
        />
        {/* Marker */}
        <div
          className="absolute top-0 h-full w-1 bg-white shadow-lg transition-all"
          style={{ left: `${clampedPosition}%` }}
        />
      </div>
      <div className="text-center mt-1">
        <span className="text-xs text-slate-400">
          Default: {formatValueByType(defaultValue, { category: 'Integer' }, units)}
        </span>
      </div>
    </div>
  );
};

/**
 * Enum Values Display Component
 * Shows enumerated values with radio button style indicators
 */
const EnumValuesDisplay = ({ enumInfo, currentValue }) => {
  if (!enumInfo || !enumInfo.values) return null;

  const displayValue = currentValue !== null ? currentValue : enumInfo.defaultValue;

  return (
    <div className="mt-3 space-y-2">
      <div className="text-sm text-slate-400 mb-2">Options:</div>
      <div className="space-y-1">
        {enumInfo.values.map((enumValue) => {
          const isSelected = enumValue.value === displayValue;
          const isCurrent = enumValue.value === displayValue;

          return (
            <div
              key={enumValue.value}
              className={`flex items-start gap-2 p-2 rounded ${
                isSelected ? 'bg-blue-900/30 border border-blue-700/50' : 'bg-slate-800/50'
              }`}
            >
              <div className="mt-0.5">
                {isCurrent ? (
                  <div className="w-4 h-4 rounded-full border-2 border-blue-400 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-blue-400" />
                  </div>
                ) : (
                  <div className="w-4 h-4 rounded-full border-2 border-slate-600" />
                )}
              </div>
              <div className="flex-1">
                <div className="text-sm text-white">
                  <span className="font-mono text-blue-300">{enumValue.value}</span>
                  <span className="mx-2 text-slate-600">→</span>
                  <span>{enumValue.label}</span>
                  {enumValue.isDefault && (
                    <Badge className="ml-2 text-xs bg-green-900/50 text-green-300 border-green-700">
                      default
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/**
 * Main Parameter Card Component
 * Displays a single parameter with expandable detailed view
 */
const ParameterCard = ({ param, category, usedByConnections = [], isExpanded: initialExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(initialExpanded);

  // Get data type information
  const dataTypeInfo = getDataTypeInfo(param.data_type);

  // Parse enum values if present
  const enumInfo = parseEnumValues(param);
  const isBoolean = isBooleanParameter(param);

  // Extract units and description
  const units = extractUnits(param);
  const description = getParameterDescription(param);

  // Parse range constraints
  const rangeInfo = parseRangeConstraints(param);

  // Format values
  const formattedDefault = formatValueByType(param.default_value, dataTypeInfo, units);
  const formattedMin = formatValueByType(param.min_value, dataTypeInfo, units);
  const formattedMax = formatValueByType(param.max_value, dataTypeInfo, units);

  // Build summary line
  const getSummary = () => {
    if (enumInfo) {
      const defaultEnum = enumInfo.values.find(v => v.value === enumInfo.defaultValue);
      if (defaultEnum) {
        return `${defaultEnum.label}`;
      }
    }

    if (param.default_value && param.default_value !== 'N/A') {
      return `Default: ${formattedDefault}`;
    }

    if (rangeInfo.hasRange) {
      return `Range: ${formattedMin} - ${formattedMax}`;
    }

    return description.substring(0, 60) + (description.length > 60 ? '...' : '');
  };

  return (
    <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
      <CardHeader
        className="cursor-pointer hover:bg-slate-800/50 transition-colors"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <CardTitle className="text-white text-base truncate">
                {param.param_name || 'Unnamed Parameter'}
              </CardTitle>
              <Badge className={`text-xs ${getDataTypeBadgeColor(dataTypeInfo.category)}`}>
                {dataTypeInfo.name}
              </Badge>
              {param.param_number && (
                <Badge variant="outline" className="text-xs text-slate-400 border-slate-700">
                  #{param.param_number}
                </Badge>
              )}
            </div>
            <div className="text-sm text-slate-400">{getSummary()}</div>
          </div>
          <div className="flex items-center gap-2">
            {usedByConnections.length > 0 && (
              <Link2 className="w-4 h-4 text-purple-400" title={`Used by ${usedByConnections.length} connection(s)`} />
            )}
            {rangeInfo && !rangeInfo.isDefaultValid && (
              <AlertCircle className="w-4 h-4 text-yellow-400" title="Default value outside valid range" />
            )}
            {isExpanded ? (
              <ChevronDown className="w-5 h-5 text-slate-400 flex-shrink-0" />
            ) : (
              <ChevronRight className="w-5 h-5 text-slate-400 flex-shrink-0" />
            )}
          </div>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="space-y-4 border-t border-slate-800 pt-4">
          {/* Type Information */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-xs text-slate-500 mb-1">Data Type</div>
              <div className="text-sm text-white">{dataTypeInfo.displayName}</div>
              {dataTypeInfo.size && (
                <div className="text-xs text-slate-400">Size: {dataTypeInfo.size}</div>
              )}
            </div>
            {units && (
              <div>
                <div className="text-xs text-slate-500 mb-1">Units</div>
                <div className="text-sm text-white">{units}</div>
              </div>
            )}
          </div>

          {/* Value Information */}
          {!enumInfo && (
            <div className="grid grid-cols-3 gap-4">
              <div>
                <div className="text-xs text-slate-500 mb-1">Default</div>
                <div className="text-sm text-white font-mono">{formattedDefault}</div>
              </div>
              <div>
                <div className="text-xs text-slate-500 mb-1">Minimum</div>
                <div className="text-sm text-white font-mono">{formattedMin}</div>
              </div>
              <div>
                <div className="text-xs text-slate-500 mb-1">Maximum</div>
                <div className="text-sm text-white font-mono">{formattedMax}</div>
              </div>
            </div>
          )}

          {/* Visual Range Indicator */}
          {!enumInfo && rangeInfo && rangeInfo.hasRange && (
            <RangeIndicator
              min={rangeInfo.min}
              max={rangeInfo.max}
              defaultValue={rangeInfo.default}
              units={units}
            />
          )}

          {/* Enum Values Display */}
          {enumInfo && (
            <EnumValuesDisplay enumInfo={enumInfo} currentValue={rangeInfo?.default} />
          )}

          {/* Description */}
          {description && (
            <div className="bg-blue-900/20 border border-blue-700/30 rounded-lg p-3">
              <div className="flex items-start gap-2">
                <Info className="w-4 h-4 text-blue-400 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-slate-300">{description}</div>
              </div>
            </div>
          )}

          {/* Usage Information */}
          {usedByConnections.length > 0 && (
            <div className="bg-purple-900/20 border border-purple-700/30 rounded-lg p-3">
              <div className="flex items-start gap-2">
                <Link2 className="w-4 h-4 text-purple-400 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="text-xs text-slate-400 mb-1">Used by Connections:</div>
                  <div className="text-sm text-slate-300">
                    {usedByConnections.join(', ')}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Technical Details */}
          <details className="group">
            <summary className="cursor-pointer text-xs text-slate-500 hover:text-slate-400 flex items-center gap-2">
              <ChevronRight className="w-3 h-3 group-open:rotate-90 transition-transform" />
              Technical Details
            </summary>
            <div className="mt-2 ml-5 space-y-2 text-xs font-mono">
              {param.link_path_size && param.link_path_size !== '0' && (
                <div className="text-slate-400">
                  <span className="text-slate-500">Link Path Size:</span> {param.link_path_size}
                </div>
              )}
              {param.link_path && param.link_path.trim() && (
                <div className="text-slate-400">
                  <span className="text-slate-500">Link Path:</span> {param.link_path}
                </div>
              )}
              {param.descriptor && param.descriptor.trim() && (
                <div className="text-slate-400">
                  <span className="text-slate-500">Descriptor:</span> {param.descriptor}
                </div>
              )}
              {param.data_size && (
                <div className="text-slate-400">
                  <span className="text-slate-500">Data Size:</span> {param.data_size} bytes
                </div>
              )}
            </div>
          </details>
        </CardContent>
      )}
    </Card>
  );
};

export default ParameterCard;
