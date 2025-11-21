import React, { useState, useMemo, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Server, Database, Globe, Monitor, MessageSquare, HardDrive,
  Workflow, BarChart3, Shield, Cloud, Users, Cpu, Radio,
  ArrowRight, ArrowDown, ArrowLeftRight, Zap, Activity,
  Box, Layers, FileCode, Clock, Bell, Lock, Network, X
} from 'lucide-react';

// Architecture layers and components
const ARCHITECTURE = {
  clients: {
    name: 'Clients',
    color: '#8b5cf6',
    components: [
      { id: 'web', name: 'Web Browser', icon: Globe, desc: 'React SPA with real-time updates' },
      { id: 'api-client', name: 'API Clients', icon: FileCode, desc: 'REST API consumers' },
      { id: 'mqtt-client', name: 'MQTT Clients', icon: Radio, desc: 'IoT device publishers' },
    ]
  },
  gateway: {
    name: 'Gateway',
    color: '#06b6d4',
    components: [
      { id: 'nginx', name: 'Nginx', icon: Shield, desc: 'Reverse proxy & SSL termination' },
      { id: 'cors', name: 'CORS', icon: Lock, desc: 'Cross-origin protection' },
      { id: 'rate-limit', name: 'Rate Limit', icon: Activity, desc: 'SlowAPI rate limiting' },
    ]
  },
  application: {
    name: 'Application',
    color: '#10b981',
    components: [
      { id: 'fastapi', name: 'FastAPI', icon: Zap, desc: 'Async REST API with OpenAPI' },
      { id: 'celery', name: 'Celery', icon: Clock, desc: 'Background task processing' },
      { id: 'mqtt-bridge', name: 'MQTT Bridge', icon: MessageSquare, desc: 'MQTT-to-API bridge' },
      { id: 'shadow', name: 'Shadow', icon: Box, desc: 'Digital twin service' },
    ]
  },
  processing: {
    name: 'Processing',
    color: '#f59e0b',
    components: [
      { id: 'iodd', name: 'IODD Parser', icon: FileCode, desc: 'IO-Link XML parsing' },
      { id: 'eds', name: 'EDS Parser', icon: FileCode, desc: 'EtherNet/IP parsing' },
      { id: 'pqa', name: 'PQA Engine', icon: BarChart3, desc: 'Quality assessment' },
      { id: 'flows', name: 'Flow Gen', icon: Workflow, desc: 'Node-RED generation' },
    ]
  },
  data: {
    name: 'Data',
    color: '#ef4444',
    components: [
      { id: 'sql', name: 'PostgreSQL', icon: Database, desc: 'Primary database' },
      { id: 'redis', name: 'Redis', icon: HardDrive, desc: 'Cache & queue' },
      { id: 'influx', name: 'InfluxDB', icon: Activity, desc: 'Time-series data' },
      { id: 'files', name: 'Files', icon: HardDrive, desc: 'File storage' },
    ]
  },
  observability: {
    name: 'Observability',
    color: '#ec4899',
    components: [
      { id: 'prometheus', name: 'Prometheus', icon: BarChart3, desc: 'Metrics collection' },
      { id: 'grafana', name: 'Grafana', icon: Monitor, desc: 'Dashboards' },
      { id: 'jaeger', name: 'Jaeger', icon: Network, desc: 'Tracing' },
      { id: 'sentry', name: 'Sentry', icon: Bell, desc: 'Error tracking' },
    ]
  },
};

// Data flows between components
const DATA_FLOWS = [
  { from: 'web', to: 'nginx', color: '#8b5cf6' },
  { from: 'api-client', to: 'nginx', color: '#8b5cf6' },
  { from: 'mqtt-client', to: 'mqtt-bridge', color: '#f59e0b' },
  { from: 'nginx', to: 'fastapi', color: '#06b6d4' },
  { from: 'fastapi', to: 'celery', color: '#10b981' },
  { from: 'fastapi', to: 'iodd', color: '#10b981' },
  { from: 'fastapi', to: 'eds', color: '#10b981' },
  { from: 'iodd', to: 'pqa', color: '#f59e0b' },
  { from: 'eds', to: 'pqa', color: '#f59e0b' },
  { from: 'fastapi', to: 'sql', color: '#ef4444' },
  { from: 'fastapi', to: 'redis', color: '#ef4444' },
  { from: 'mqtt-bridge', to: 'influx', color: '#ef4444' },
  { from: 'celery', to: 'redis', color: '#ef4444' },
  { from: 'prometheus', to: 'fastapi', color: '#ec4899' },
  { from: 'grafana', to: 'prometheus', color: '#ec4899' },
];

// Component card
const ComponentCard = ({ comp, color, x, y, width, height, isSelected, onClick, delay }) => {
  const Icon = comp.icon;

  return (
    <motion.g
      style={{ cursor: 'pointer' }}
      onClick={() => onClick(comp)}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay, type: 'spring', stiffness: 200 }}
    >
      {/* Selection glow */}
      {isSelected && (
        <motion.rect
          x={x - 3} y={y - 3}
          width={width + 6} height={height + 6}
          rx={10}
          fill="none"
          stroke={color}
          strokeWidth={2}
          animate={{ opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        />
      )}

      {/* Shadow */}
      <rect
        x={x + 2} y={y + 2}
        width={width} height={height}
        rx={8}
        fill="rgba(0,0,0,0.3)"
      />

      {/* Background */}
      <rect
        x={x} y={y}
        width={width} height={height}
        rx={8}
        fill={`${color}15`}
        stroke={isSelected ? color : `${color}40`}
        strokeWidth={isSelected ? 2 : 1}
      />

      {/* Shine overlay */}
      <rect
        x={x} y={y}
        width={width} height={height}
        rx={8}
        fill="url(#cardShine)"
        opacity={0.4}
      />

      {/* Icon */}
      <foreignObject x={x + 6} y={y + (height - 16) / 2} width={16} height={16}>
        <Icon style={{ color, width: 16, height: 16 }} />
      </foreignObject>

      {/* Name */}
      <text
        x={x + 26}
        y={y + height / 2 + 4}
        fill="white"
        fontSize={9}
        fontWeight={500}
      >
        {comp.name}
      </text>
    </motion.g>
  );
};

// Layer row
const LayerRow = ({ layer, layerId, y, width, componentPositions, selectedComponent, onComponentClick, index }) => {
  const rowHeight = 50;

  return (
    <motion.g
      initial={{ opacity: 0, x: -30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      {/* Layer background */}
      <rect
        x={0} y={y}
        width={width}
        height={rowHeight}
        rx={6}
        fill={`${layer.color}08`}
        stroke={`${layer.color}20`}
        strokeWidth={1}
      />

      {/* Layer label */}
      <rect
        x={8} y={y + 8}
        width={70} height={34}
        rx={6}
        fill={`${layer.color}20`}
      />
      <text
        x={43} y={y + 30}
        textAnchor="middle"
        fill={layer.color}
        fontSize={9}
        fontWeight={600}
      >
        {layer.name}
      </text>

      {/* Components */}
      {layer.components.map((comp, compIndex) => {
        const pos = componentPositions[comp.id];
        if (!pos) return null;

        return (
          <ComponentCard
            key={comp.id}
            comp={comp}
            color={layer.color}
            x={pos.x}
            y={pos.y}
            width={pos.width}
            height={pos.height}
            isSelected={selectedComponent?.id === comp.id}
            onClick={onComponentClick}
            delay={index * 0.1 + compIndex * 0.03}
          />
        );
      })}
    </motion.g>
  );
};

// Connection line
const ConnectionLine = ({ x1, y1, x2, y2, color, animated, delay }) => {
  // Bezier curve for smoother connections
  const midY = (y1 + y2) / 2;
  const pathD = `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;

  return (
    <g>
      {/* Glow */}
      <path
        d={pathD}
        fill="none"
        stroke={color}
        strokeWidth={3}
        opacity={0.15}
        filter="url(#blur)"
      />

      {/* Main line */}
      <motion.path
        d={pathD}
        fill="none"
        stroke={`${color}50`}
        strokeWidth={1}
        strokeDasharray="3,3"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ delay, duration: 0.8 }}
      />

      {/* Animated dot */}
      {animated && (
        <circle r={2} fill={color}>
          <animateMotion dur="2.5s" repeatCount="indefinite" path={pathD} />
        </circle>
      )}
    </g>
  );
};

// Details panel
const DetailsPanel = ({ component, onClose }) => {
  if (!component) return null;

  return (
    <motion.div
      className="absolute top-3 right-3 w-56 rounded-xl border shadow-2xl backdrop-blur-xl overflow-hidden z-50"
      style={{
        backgroundColor: 'rgba(15, 15, 20, 0.95)',
        borderColor: 'rgba(16, 185, 129, 0.3)',
        boxShadow: '0 0 30px rgba(16, 185, 129, 0.15), 0 15px 40px rgba(0,0,0,0.5)',
      }}
      initial={{ opacity: 0, x: 20, scale: 0.95 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 20, scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 300, damping: 25 }}
    >
      <div className="p-3 bg-gradient-to-r from-brand-green/20 to-transparent relative">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 w-5 h-5 rounded-full flex items-center justify-center hover:bg-white/10 transition-colors"
        >
          <X className="w-3 h-3 text-white/60" />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-brand-green/30 flex items-center justify-center">
            <component.icon className="w-4 h-4 text-brand-green" />
          </div>
          <div>
            <h4 className="font-bold text-white text-sm">{component.name}</h4>
            <p className="text-white/40 text-[10px]">{component.id}</p>
          </div>
        </div>
      </div>
      <div className="p-3">
        <p className="text-white/60 text-xs leading-relaxed">{component.desc}</p>
        <div className="mt-2 pt-2 border-t border-white/10 flex items-center gap-1.5">
          <div className="w-1.5 h-1.5 rounded-full bg-brand-green animate-pulse" />
          <span className="text-white/40 text-[10px]">Active</span>
        </div>
      </div>
    </motion.div>
  );
};

const ArchitectureDiagram = () => {
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 900, height: 450 });
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [showFlows, setShowFlows] = useState(true);

  const layers = Object.entries(ARCHITECTURE);

  // Measure container
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setDimensions({
          width: Math.max(rect.width, 600),
          height: Math.max(380, Math.min(480, rect.width * 0.42))
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const { width, height } = dimensions;
  const padding = { top: 35, right: 15, bottom: 40, left: 15 };
  const contentWidth = width - padding.left - padding.right;
  const contentHeight = height - padding.top - padding.bottom;
  const rowHeight = contentHeight / layers.length;
  const rowGap = 4;

  // Calculate component positions
  const componentPositions = useMemo(() => {
    const positions = {};
    const compWidth = Math.min(85, (contentWidth - 90) / 5);
    const compHeight = rowHeight - rowGap * 2 - 10;
    const compGap = 8;

    layers.forEach(([layerId, layer], layerIndex) => {
      const y = padding.top + layerIndex * rowHeight;
      const startX = 90; // After layer label
      const availableWidth = contentWidth - startX;

      layer.components.forEach((comp, compIndex) => {
        const x = padding.left + startX + compIndex * (compWidth + compGap);
        positions[comp.id] = {
          x,
          y: y + rowGap + 5,
          width: compWidth,
          height: compHeight,
          centerX: x + compWidth / 2,
          centerY: y + rowGap + 5 + compHeight / 2,
        };
      });
    });

    return positions;
  }, [layers, contentWidth, rowHeight, padding]);

  return (
    <div ref={containerRef} className="relative w-full">
      <div
        className="relative bg-gradient-to-br from-[#0a0a0f] via-[#0d0d14] to-[#0a0a0f] rounded-2xl border border-white/10 overflow-hidden"
        style={{ height }}
      >
        {/* Background */}
        <div className="absolute inset-0 overflow-hidden rounded-2xl">
          <div
            className="absolute inset-0"
            style={{
              background: 'radial-gradient(ellipse 70% 50% at 50% 40%, rgba(16, 185, 129, 0.05) 0%, transparent 70%)',
            }}
          />

          <svg className="absolute inset-0 w-full h-full opacity-10">
            <defs>
              <pattern id="arch-grid" width="30" height="30" patternUnits="userSpaceOnUse">
                <path d="M 30 0 L 0 0 0 30" fill="none" stroke="currentColor" strokeWidth="0.3" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#arch-grid)" />
          </svg>

          {/* Particles */}
          {[...Array(10)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 rounded-full"
              style={{
                left: `${15 + Math.random() * 70}%`,
                top: `${15 + Math.random() * 70}%`,
                backgroundColor: ['#10b981', '#8b5cf6', '#f59e0b', '#ef4444', '#ec4899'][i % 5],
              }}
              animate={{ y: [0, -12, 0], opacity: [0.2, 0.4, 0.2] }}
              transition={{
                duration: 3 + Math.random() * 2,
                repeat: Infinity,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>

        {/* Main SVG */}
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="relative z-10"
          style={{ width: '100%', height: '100%' }}
        >
          <defs>
            <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" />
            </filter>
            <linearGradient id="cardShine" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="white" stopOpacity="0.1" />
              <stop offset="50%" stopColor="white" stopOpacity="0" />
              <stop offset="100%" stopColor="white" stopOpacity="0.05" />
            </linearGradient>
          </defs>

          {/* Connection lines (behind layers) */}
          {showFlows && (
            <g>
              {DATA_FLOWS.map((flow, index) => {
                const fromPos = componentPositions[flow.from];
                const toPos = componentPositions[flow.to];
                if (!fromPos || !toPos) return null;

                return (
                  <ConnectionLine
                    key={`${flow.from}-${flow.to}`}
                    x1={fromPos.centerX}
                    y1={fromPos.centerY + fromPos.height / 2}
                    x2={toPos.centerX}
                    y2={toPos.centerY - toPos.height / 2}
                    color={flow.color}
                    animated={index % 4 === 0}
                    delay={index * 0.05}
                  />
                );
              })}
            </g>
          )}

          {/* Layer rows */}
          <g transform={`translate(${padding.left}, 0)`}>
            {layers.map(([layerId, layer], index) => (
              <LayerRow
                key={layerId}
                layer={layer}
                layerId={layerId}
                y={padding.top + index * rowHeight}
                width={contentWidth}
                componentPositions={componentPositions}
                selectedComponent={selectedComponent}
                onComponentClick={setSelectedComponent}
                index={index}
              />
            ))}
          </g>

          {/* Title */}
          <text
            x={width / 2}
            y={20}
            textAnchor="middle"
            fill="white"
            fontSize={13}
            fontWeight={700}
            opacity={0.8}
          >
            GreenStack Architecture
          </text>
        </svg>

        {/* Details panel */}
        <AnimatePresence>
          {selectedComponent && (
            <DetailsPanel
              component={selectedComponent}
              onClose={() => setSelectedComponent(null)}
            />
          )}
        </AnimatePresence>

        {/* Controls */}
        <motion.div
          className="absolute bottom-3 left-3"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <button
            onClick={() => setShowFlows(!showFlows)}
            className={`px-3 py-1.5 rounded-lg text-[10px] font-medium transition-all ${
              showFlows
                ? 'bg-brand-green/20 text-brand-green border border-brand-green/30'
                : 'bg-white/5 text-white/50 border border-white/10'
            }`}
          >
            {showFlows ? 'Hide' : 'Show'} Flows
          </button>
        </motion.div>

        {/* Stats */}
        <motion.div
          className="absolute bottom-3 right-3 flex items-center gap-3"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
        >
          <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-black/40 backdrop-blur-sm border border-white/10">
            <div className="w-1.5 h-1.5 rounded-full bg-brand-green animate-pulse" />
            <span className="text-white/50 text-[10px]">{layers.length} Layers</span>
          </div>
          <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-black/40 backdrop-blur-sm border border-white/10">
            <div className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-pulse" />
            <span className="text-white/50 text-[10px]">
              {Object.values(ARCHITECTURE).reduce((acc, l) => acc + l.components.length, 0)} Components
            </span>
          </div>
        </motion.div>

        {/* Hint */}
        <motion.div
          className="absolute top-8 left-1/2 -translate-x-1/2 text-white/30 text-[10px]"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
        >
          Click components for details
        </motion.div>
      </div>
    </div>
  );
};

export default ArchitectureDiagram;
