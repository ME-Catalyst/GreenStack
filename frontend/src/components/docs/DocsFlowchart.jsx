import React from 'react';
import { CheckCircle, AlertCircle, ArrowDown, ArrowRight, GitBranch } from 'lucide-react';

/**
 * DocsFlowchart - Interactive Flowchart Component
 *
 * Creates interactive flowcharts for visualizing processes, workflows, and decision trees
 */

// FlowchartStep - Individual step in the flowchart
const FlowchartStep = ({
  title,
  description,
  type = 'process', // 'process', 'decision', 'start', 'end', 'success', 'error'
  children
}) => {
  const typeStyles = {
    start: {
      shape: 'rounded-full',
      bg: 'bg-brand-green/10 hover:bg-brand-green/20',
      border: 'border-brand-green',
      text: 'text-brand-green'
    },
    process: {
      shape: 'rounded-lg',
      bg: 'bg-surface hover:bg-surface-hover',
      border: 'border-border',
      text: 'text-foreground'
    },
    decision: {
      shape: 'rotate-45',
      bg: 'bg-warning/10 hover:bg-warning/20',
      border: 'border-warning',
      text: 'text-warning'
    },
    success: {
      shape: 'rounded-lg',
      bg: 'bg-success/10 hover:bg-success/20',
      border: 'border-success',
      text: 'text-success'
    },
    error: {
      shape: 'rounded-lg',
      bg: 'bg-destructive/10 hover:bg-destructive/20',
      border: 'border-destructive',
      text: 'text-destructive'
    },
    end: {
      shape: 'rounded-full',
      bg: 'bg-muted hover:bg-muted/80',
      border: 'border-muted',
      text: 'text-muted-foreground'
    }
  };

  const style = typeStyles[type] || typeStyles.process;
  const isDecision = type === 'decision';

  return (
    <div className="flex flex-col items-center gap-2">
      <div className={`
        relative p-6 min-w-[200px] max-w-[300px]
        border-2 ${style.border} ${style.shape} ${style.bg}
        transition-all duration-300
        hover:scale-105 hover:shadow-lg
        cursor-pointer
        group
      `}>
        <div className={isDecision ? '-rotate-45' : ''}>
          <div className="text-center">
            <h4 className={`font-semibold ${style.text} mb-1`}>{title}</h4>
            {description && (
              <p className="text-sm text-muted-foreground">{description}</p>
            )}
          </div>
        </div>
      </div>
      {children}
    </div>
  );
};

// FlowchartConnector - Arrow connecting flowchart steps
const FlowchartConnector = ({ label, direction = 'down', variant = 'default' }) => {
  const ConnectorIcon = direction === 'right' ? ArrowRight : ArrowDown;

  const variants = {
    default: 'text-muted-foreground',
    success: 'text-success',
    error: 'text-destructive',
    branch: 'text-warning'
  };

  return (
    <div className="flex items-center justify-center gap-2 my-2">
      <div className="flex flex-col items-center">
        <ConnectorIcon className={`w-6 h-6 ${variants[variant]} animate-pulse`} />
        {label && (
          <span className={`text-xs font-medium ${variants[variant]} mt-1`}>
            {label}
          </span>
        )}
      </div>
    </div>
  );
};

// FlowchartBranch - Decision branch with multiple paths
const FlowchartBranch = ({ children }) => {
  return (
    <div className="flex items-start justify-center gap-8 my-4">
      {children}
    </div>
  );
};

// FlowchartPath - Single path in a branch
const FlowchartPath = ({ label, variant = 'default', children }) => {
  return (
    <div className="flex flex-col items-center">
      <FlowchartConnector label={label} variant={variant} />
      {children}
    </div>
  );
};

// FlowchartContainer - Main container for flowchart
const FlowchartContainer = ({ title, description, children, className = '' }) => {
  return (
    <div className={`my-8 p-6 border border-border rounded-xl bg-surface/30 ${className}`}>
      {(title || description) && (
        <div className="mb-8 text-center">
          {title && (
            <h3 className="text-xl font-bold text-foreground mb-2">
              {title}
            </h3>
          )}
          {description && (
            <p className="text-sm text-muted-foreground">
              {description}
            </p>
          )}
        </div>
      )}
      <div className="flex flex-col items-center">
        {children}
      </div>
    </div>
  );
};

// Example: EDS Import Process Flowchart
export const EdsImportFlow = () => {
  return (
    <FlowchartContainer
      title="EDS File Import Process"
      description="Step-by-step flow of how EDS files are processed"
    >
      <FlowchartStep type="start" title="Start" description="User uploads EDS file" />

      <FlowchartConnector />

      <FlowchartStep type="process" title="Validate File" description="Check file format and structure" />

      <FlowchartConnector />

      <FlowchartStep type="decision" title="Valid?" description="Is file valid?" />

      <FlowchartBranch>
        <FlowchartPath label="No" variant="error">
          <FlowchartStep type="error" title="Show Error" description="Display validation errors" />
          <FlowchartConnector />
          <FlowchartStep type="end" title="End" description="Process cancelled" />
        </FlowchartPath>

        <FlowchartPath label="Yes" variant="success">
          <FlowchartStep type="process" title="Parse XML" description="Extract device metadata" />
          <FlowchartConnector />
          <FlowchartStep type="process" title="Save to Database" description="Store device information" />
          <FlowchartConnector />
          <FlowchartStep type="success" title="Success" description="Device imported" />
          <FlowchartConnector />
          <FlowchartStep type="end" title="End" description="Process complete" />
        </FlowchartPath>
      </FlowchartBranch>
    </FlowchartContainer>
  );
};

// Export components
export default {
  Container: FlowchartContainer,
  Step: FlowchartStep,
  Connector: FlowchartConnector,
  Branch: FlowchartBranch,
  Path: FlowchartPath,
};
