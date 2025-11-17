import React from 'react';
import { Server, Database, Globe, Cpu, Layers, ArrowRight, ArrowDown } from 'lucide-react';

/**
 * DocsDiagram - Interactive Diagram Component
 *
 * Reusable component for creating interactive architecture diagrams
 * with nodes, connections, and animations
 */

// DiagramNode - Individual node in the diagram
const DiagramNode = ({ icon: Icon, title, description, color = 'brand-green', size = 'md', children }) => {
  const sizeClasses = {
    sm: 'p-3 min-w-[120px]',
    md: 'p-4 min-w-[160px]',
    lg: 'p-6 min-w-[200px]'
  };

  return (
    <div className={`
      ${sizeClasses[size]}
      border-2 border-${color} rounded-lg
      bg-background hover:bg-surface
      transition-all duration-300
      hover:scale-105 hover:shadow-lg hover:shadow-${color}/20
      cursor-pointer
      group
    `}>
      <div className="flex flex-col items-center gap-2 text-center">
        {Icon && (
          <div className={`
            p-2 rounded-lg bg-${color}/10
            group-hover:bg-${color}/20
            transition-colors duration-300
          `}>
            <Icon className={`w-6 h-6 text-${color}`} />
          </div>
        )}
        <h4 className="font-semibold text-foreground text-sm">{title}</h4>
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
        {children}
      </div>
    </div>
  );
};

// DiagramArrow - Connecting arrow between nodes
const DiagramArrow = ({ direction = 'right', label, animated = false }) => {
  const ArrowIcon = direction === 'down' ? ArrowDown : ArrowRight;

  return (
    <div className="flex items-center justify-center gap-2">
      <div className="flex flex-col items-center gap-1">
        <ArrowIcon className={`
          w-5 h-5 text-brand-green
          ${animated ? 'animate-pulse' : ''}
        `} />
        {label && (
          <span className="text-xs text-muted-foreground font-medium">
            {label}
          </span>
        )}
      </div>
    </div>
  );
};

// DiagramLayer - Horizontal layer for grouping nodes
const DiagramLayer = ({ title, children, variant = 'default' }) => {
  const variants = {
    default: 'border-border bg-surface/30',
    primary: 'border-brand-green/30 bg-brand-green/5',
    secondary: 'border-muted bg-surface/50'
  };

  return (
    <div className={`
      border-2 ${variants[variant]} rounded-xl p-6
      transition-all duration-300
    `}>
      {title && (
        <h3 className="text-sm font-semibold text-foreground mb-4 uppercase tracking-wider">
          {title}
        </h3>
      )}
      <div className="flex items-center justify-center gap-4 flex-wrap">
        {children}
      </div>
    </div>
  );
};

// DiagramContainer - Main container for the entire diagram
const DiagramContainer = ({ title, description, children, className = '' }) => {
  return (
    <div className={`my-8 ${className}`}>
      {(title || description) && (
        <div className="mb-6 text-center">
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
      <div className="flex flex-col gap-6">
        {children}
      </div>
    </div>
  );
};

// Example: Three-tier architecture diagram
export const ThreeTierArchitecture = () => {
  return (
    <DiagramContainer
      title="Greenstack Architecture"
      description="Modern three-tier architecture with microservices"
    >
      {/* Presentation Layer */}
      <DiagramLayer title="Presentation Layer" variant="primary">
        <DiagramNode
          icon={Globe}
          title="React Frontend"
          description="Port 3000"
          color="brand-green"
          size="lg"
        />
      </DiagramLayer>

      <DiagramArrow direction="down" label="HTTP/REST" animated />

      {/* Application Layer */}
      <DiagramLayer title="Application Layer" variant="default">
        <DiagramNode
          icon={Server}
          title="FastAPI Server"
          description="Port 8000"
          color="brand-green"
        />
        <DiagramNode
          icon={Cpu}
          title="EDS Parser"
          description="XML Processing"
          color="brand-green"
        />
        <DiagramNode
          icon={Layers}
          title="MQTT Bridge"
          description="Port 1883"
          color="brand-green"
        />
      </DiagramLayer>

      <DiagramArrow direction="down" label="SQL/ORM" animated />

      {/* Data Layer */}
      <DiagramLayer title="Data Layer" variant="secondary">
        <DiagramNode
          icon={Database}
          title="SQLite/PostgreSQL"
          description="Primary Database"
          color="brand-green"
          size="lg"
        />
      </DiagramLayer>
    </DiagramContainer>
  );
};

// Export components
export default {
  Container: DiagramContainer,
  Layer: DiagramLayer,
  Node: DiagramNode,
  Arrow: DiagramArrow,
};
