import React, { useState, useCallback, useMemo, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Server, Database, Globe, Cpu, Cloud, Shield, Activity,
  MessageSquare, BarChart3, GitBranch, Layers, Box, Zap,
  Code, FileCode, Terminal, Monitor, Workflow, Lock,
  Clock, Bell, HardDrive, Network, Radio, Gauge
} from 'lucide-react';

// Tech Stack Data Structure
const TECH_STACK = {
  core: {
    name: 'Core',
    icon: Server,
    color: '#10b981',
    items: [
      { name: 'FastAPI', version: '0.100+' },
      { name: 'SQLAlchemy', version: '2.0+' },
      { name: 'Pydantic', version: '2.0+' },
      { name: 'Alembic', version: '1.11+' },
      { name: 'Uvicorn', version: '0.23+' },
    ]
  },
  frontend: {
    name: 'Frontend',
    icon: Monitor,
    color: '#8b5cf6',
    items: [
      { name: 'React 18', version: '18.2+' },
      { name: 'Vite', version: '7.2+' },
      { name: 'TailwindCSS', version: '3.3+' },
      { name: 'Radix UI', version: 'Latest' },
      { name: 'Framer', version: '10.16+' },
      { name: 'Recharts', version: '3.4+' },
      { name: 'Lucide', version: '0.290+' },
      { name: 'Three.js', version: '0.158+' },
    ]
  },
  database: {
    name: 'Data',
    icon: Database,
    color: '#06b6d4',
    items: [
      { name: 'SQLite', version: '3.x' },
      { name: 'PostgreSQL', version: '16+' },
      { name: 'Redis', version: '7+' },
      { name: 'InfluxDB', version: '2.7+' },
    ]
  },
  messaging: {
    name: 'IoT',
    icon: Radio,
    color: '#f59e0b',
    items: [
      { name: 'MQTT v5', version: 'v5' },
      { name: 'Mosquitto', version: '2.0' },
      { name: 'Paho', version: '1.6+' },
      { name: 'WebSocket', version: 'RFC' },
    ]
  },
  background: {
    name: 'Jobs',
    icon: Clock,
    color: '#ec4899',
    items: [
      { name: 'Celery', version: '5.3+' },
      { name: 'Flower', version: '2.0+' },
      { name: 'Redis', version: '7+' },
    ]
  },
  observability: {
    name: 'Observe',
    icon: Activity,
    color: '#ef4444',
    items: [
      { name: 'Prometheus', version: '2.48+' },
      { name: 'Grafana', version: '10.2+' },
      { name: 'Jaeger', version: 'Latest' },
      { name: 'OTel', version: '1.20+' },
      { name: 'Sentry', version: '7.100+' },
      { name: 'Alertmgr', version: '0.26+' },
    ]
  },
  security: {
    name: 'Security',
    icon: Shield,
    color: '#14b8a6',
    items: [
      { name: 'JWT', version: '3.3+' },
      { name: 'Passlib', version: '1.7+' },
      { name: 'SlowAPI', version: '0.1.9+' },
      { name: 'CORS', version: 'Built-in' },
    ]
  },
  devops: {
    name: 'DevOps',
    icon: Cloud,
    color: '#6366f1',
    items: [
      { name: 'Docker', version: 'Latest' },
      { name: 'Compose', version: '3.8' },
      { name: 'GH Actions', version: 'Latest' },
      { name: 'Nginx', version: 'Alpine' },
    ]
  },
  protocols: {
    name: 'Protocols',
    icon: Network,
    color: '#84cc16',
    items: [
      { name: 'IODD', version: '1.0-1.1' },
      { name: 'EDS', version: 'ODVA' },
      { name: 'lxml', version: '4.9+' },
      { name: 'xmlschema', version: '2.3+' },
    ]
  },
  automation: {
    name: 'Auto',
    icon: Workflow,
    color: '#f97316',
    items: [
      { name: 'Node-RED', version: 'Latest' },
      { name: 'Jinja2', version: '3.1+' },
      { name: 'Flows', version: 'Custom' },
    ]
  },
};

// Small tech node (child of category)
const TechNode = ({ item, color, x, y, delay }) => {
  return (
    <motion.g
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ delay, type: 'spring', stiffness: 300, damping: 20 }}
    >
      {/* Node background */}
      <rect
        x={x - 28}
        y={y - 10}
        width={56}
        height={20}
        rx={10}
        fill={`${color}25`}
        stroke={`${color}60`}
        strokeWidth={1}
      />

      {/* Tech name */}
      <text
        x={x}
        y={y + 4}
        textAnchor="middle"
        fill="white"
        fontSize={8}
        fontWeight={500}
      >
        {item.name.length > 9 ? item.name.slice(0, 8) + '..' : item.name}
      </text>
    </motion.g>
  );
};

// Connection line from category to tech
const BranchLine = ({ x1, y1, x2, y2, color, delay }) => {
  return (
    <motion.line
      x1={x1}
      y1={y1}
      x2={x2}
      y2={y2}
      stroke={`${color}50`}
      strokeWidth={1}
      initial={{ pathLength: 0, opacity: 0 }}
      animate={{ pathLength: 1, opacity: 1 }}
      exit={{ pathLength: 0, opacity: 0 }}
      transition={{ delay, duration: 0.3 }}
    />
  );
};

// Category node with branching children
const CategoryNode = ({ category, data, isExpanded, onClick, cx, cy, techPositions }) => {
  const Icon = data.icon;

  return (
    <g>
      {/* Branch lines to tech nodes */}
      <AnimatePresence>
        {isExpanded && techPositions.map((pos, i) => (
          <BranchLine
            key={`line-${i}`}
            x1={cx}
            y1={cy}
            x2={pos.x}
            y2={pos.y}
            color={data.color}
            delay={i * 0.03}
          />
        ))}
      </AnimatePresence>

      {/* Tech nodes */}
      <AnimatePresence>
        {isExpanded && techPositions.map((pos, i) => (
          <TechNode
            key={data.items[i].name}
            item={data.items[i]}
            color={data.color}
            x={pos.x}
            y={pos.y}
            delay={i * 0.03 + 0.1}
          />
        ))}
      </AnimatePresence>

      {/* Main category node */}
      <motion.g
        style={{ cursor: 'pointer' }}
        onClick={() => onClick(category)}
        whileHover={{ scale: 1.1 }}
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 200 }}
      >
        {/* Pulse ring when expanded */}
        {isExpanded && (
          <motion.circle
            cx={cx}
            cy={cy}
            r={28}
            fill="none"
            stroke={data.color}
            strokeWidth={2}
            animate={{ scale: [1, 1.3, 1], opacity: [0.5, 0, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        )}

        {/* Node shadow */}
        <circle
          cx={cx + 2}
          cy={cy + 2}
          r={24}
          fill="rgba(0,0,0,0.3)"
        />

        {/* Node background */}
        <circle
          cx={cx}
          cy={cy}
          r={24}
          fill={isExpanded ? `${data.color}40` : `${data.color}20`}
          stroke={data.color}
          strokeWidth={2}
        />

        {/* Node shine */}
        <circle
          cx={cx}
          cy={cy}
          r={24}
          fill="url(#nodeShine)"
          opacity={0.4}
        />

        {/* Icon */}
        <foreignObject x={cx - 10} y={cy - 14} width={20} height={20}>
          <Icon style={{ color: data.color, width: 20, height: 20 }} />
        </foreignObject>

        {/* Label */}
        <text
          x={cx}
          y={cy + 18}
          textAnchor="middle"
          fill={data.color}
          fontSize={7}
          fontWeight={600}
        >
          {data.name}
        </text>

        {/* Count badge */}
        <circle
          cx={cx + 18}
          cy={cy - 18}
          r={9}
          fill={data.color}
        />
        <text
          x={cx + 18}
          y={cy - 15}
          textAnchor="middle"
          fill="#000"
          fontSize={8}
          fontWeight={700}
        >
          {data.items.length}
        </text>
      </motion.g>
    </g>
  );
};

// Connection line from center to category
const ConnectionLine = ({ x1, y1, x2, y2, color, isActive, delay }) => {
  return (
    <g>
      {/* Glow */}
      {isActive && (
        <line
          x1={x1} y1={y1} x2={x2} y2={y2}
          stroke={color}
          strokeWidth={6}
          opacity={0.2}
          filter="url(#blur)"
        />
      )}

      {/* Main line */}
      <motion.line
        x1={x1} y1={y1} x2={x2} y2={y2}
        stroke={isActive ? color : '#333'}
        strokeWidth={isActive ? 2 : 1}
        strokeDasharray={isActive ? '0' : '4,4'}
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ delay, duration: 0.4 }}
      />

      {/* Animated dot */}
      {isActive && (
        <motion.circle
          r={3}
          fill={color}
          animate={{
            cx: [x1, x2],
            cy: [y1, y2],
            opacity: [0, 1, 1, 0],
          }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}
    </g>
  );
};

const TechStackMindMap = () => {
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 1000, height: 500 });
  const categories = Object.keys(TECH_STACK);
  const [expandedCategory, setExpandedCategory] = useState(null);

  // Measure container
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setDimensions({
          width: Math.max(rect.width, 600),
          height: Math.max(420, Math.min(520, rect.width * 0.45))
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const { width, height } = dimensions;
  const centerX = width / 2;
  const centerY = height / 2;

  // Elliptical layout for categories
  const radiusX = Math.min(width * 0.38, 380);
  const radiusY = Math.min(height * 0.36, 170);

  const totalTechs = useMemo(() =>
    Object.values(TECH_STACK).reduce((acc, cat) => acc + cat.items.length, 0),
    []
  );

  // Get category position
  const getCategoryPosition = useCallback((index, total) => {
    const angle = (index * 2 * Math.PI) / total - Math.PI / 2;
    return {
      x: centerX + radiusX * Math.cos(angle),
      y: centerY + radiusY * Math.sin(angle),
      angle,
    };
  }, [centerX, centerY, radiusX, radiusY]);

  // Calculate tech node positions (branching outward from category)
  const getTechPositions = useCallback((categoryPos, itemCount, angle) => {
    const positions = [];
    const branchRadius = 65; // Distance from category to tech nodes
    const spreadAngle = Math.min(Math.PI * 0.6, itemCount * 0.18); // How wide the fan spreads
    const startAngle = angle - spreadAngle / 2;

    for (let i = 0; i < itemCount; i++) {
      const techAngle = startAngle + (spreadAngle * i) / Math.max(1, itemCount - 1);
      positions.push({
        x: categoryPos.x + branchRadius * Math.cos(techAngle),
        y: categoryPos.y + branchRadius * Math.sin(techAngle),
      });
    }

    return positions;
  }, []);

  const handleCategoryClick = useCallback((category) => {
    setExpandedCategory(prev => prev === category ? null : category);
  }, []);

  const collapseAll = useCallback(() => {
    setExpandedCategory(null);
  }, []);

  return (
    <div ref={containerRef} className="relative w-full">
      <div
        className="relative bg-gradient-to-br from-[#0a0a0f] via-[#0d0d14] to-[#0a0a0f] rounded-2xl border border-white/10 overflow-hidden"
        style={{ height }}
      >
        {/* Background effects */}
        <div className="absolute inset-0 overflow-hidden rounded-2xl">
          <div
            className="absolute inset-0"
            style={{
              background: `radial-gradient(ellipse 60% 50% at 50% 50%, rgba(16, 185, 129, 0.06) 0%, transparent 70%)`,
            }}
          />

          <svg className="absolute inset-0 w-full h-full opacity-15">
            <defs>
              <pattern id="mindmap-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="0.3" />
              </pattern>
              <radialGradient id="gridFade" cx="50%" cy="50%" r="60%">
                <stop offset="0%" stopColor="white" stopOpacity="1" />
                <stop offset="100%" stopColor="white" stopOpacity="0" />
              </radialGradient>
              <mask id="gridMask">
                <rect width="100%" height="100%" fill="url(#gridFade)" />
              </mask>
            </defs>
            <rect width="100%" height="100%" fill="url(#mindmap-grid)" mask="url(#gridMask)" />
          </svg>

          {/* Floating particles */}
          {[...Array(10)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 rounded-full bg-brand-green/30"
              style={{
                left: `${15 + Math.random() * 70}%`,
                top: `${15 + Math.random() * 70}%`,
              }}
              animate={{
                y: [0, -15, 0],
                opacity: [0.2, 0.5, 0.2],
              }}
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
            <linearGradient id="nodeShine" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="white" stopOpacity="0.2" />
              <stop offset="50%" stopColor="white" stopOpacity="0" />
              <stop offset="100%" stopColor="white" stopOpacity="0.1" />
            </linearGradient>
            <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#10b981" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
            </radialGradient>
          </defs>

          {/* Connection lines from center to categories */}
          {categories.map((cat, i) => {
            const pos = getCategoryPosition(i, categories.length);
            const data = TECH_STACK[cat];
            const isActive = expandedCategory === cat;

            return (
              <ConnectionLine
                key={`conn-${cat}`}
                x1={centerX}
                y1={centerY}
                x2={pos.x}
                y2={pos.y}
                color={data.color}
                isActive={isActive}
                delay={i * 0.05}
              />
            );
          })}

          {/* Category nodes with tech branches */}
          {categories.map((cat, i) => {
            const pos = getCategoryPosition(i, categories.length);
            const data = TECH_STACK[cat];
            const isExpanded = expandedCategory === cat;
            const techPositions = getTechPositions(pos, data.items.length, pos.angle);

            return (
              <CategoryNode
                key={cat}
                category={cat}
                data={data}
                isExpanded={isExpanded}
                onClick={handleCategoryClick}
                cx={pos.x}
                cy={pos.y}
                techPositions={techPositions}
              />
            );
          })}

          {/* Center node */}
          <motion.g
            style={{ cursor: 'pointer' }}
            onClick={collapseAll}
            whileHover={{ scale: 1.05 }}
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 200 }}
          >
            {/* Center glow */}
            <circle
              cx={centerX}
              cy={centerY}
              r={50}
              fill="url(#centerGlow)"
            />

            {/* Animated outer ring */}
            <motion.circle
              cx={centerX}
              cy={centerY}
              r={42}
              fill="none"
              stroke="rgba(16, 185, 129, 0.3)"
              strokeWidth={1}
              animate={{ scale: [1, 1.1, 1], opacity: [0.3, 0.1, 0.3] }}
              transition={{ duration: 3, repeat: Infinity }}
            />

            {/* Main circle */}
            <circle
              cx={centerX}
              cy={centerY}
              r={38}
              fill="url(#centerGradient)"
            />
            <defs>
              <linearGradient id="centerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#10b981" />
                <stop offset="50%" stopColor="#059669" />
                <stop offset="100%" stopColor="#7c3aed" />
              </linearGradient>
            </defs>

            {/* Inner shine */}
            <circle
              cx={centerX}
              cy={centerY}
              r={36}
              fill="none"
              stroke="rgba(255,255,255,0.2)"
              strokeWidth={2}
            />

            {/* Icon */}
            <foreignObject x={centerX - 12} y={centerY - 18} width={24} height={24}>
              <Layers style={{ color: 'white', width: 24, height: 24 }} />
            </foreignObject>

            {/* Text */}
            <text
              x={centerX}
              y={centerY + 14}
              textAnchor="middle"
              fill="white"
              fontSize={10}
              fontWeight={700}
            >
              GreenStack
            </text>
            <text
              x={centerX}
              y={centerY + 26}
              textAnchor="middle"
              fill="rgba(255,255,255,0.6)"
              fontSize={8}
            >
              {totalTechs} techs
            </text>
          </motion.g>
        </svg>

        {/* Bottom stats */}
        <div className="absolute bottom-3 left-0 right-0 flex justify-center gap-6">
          <motion.div
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-black/40 backdrop-blur-sm border border-white/10"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <div className="w-1.5 h-1.5 rounded-full bg-brand-green animate-pulse" />
            <span className="text-white/50 text-[10px]">{categories.length} Categories</span>
          </motion.div>
          <motion.div
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-black/40 backdrop-blur-sm border border-white/10"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
          >
            <div className="w-1.5 h-1.5 rounded-full bg-purple-500 animate-pulse" />
            <span className="text-white/50 text-[10px]">{totalTechs} Technologies</span>
          </motion.div>
        </div>

        {/* Hint */}
        <motion.div
          className="absolute top-3 left-1/2 -translate-x-1/2 text-white/30 text-[10px]"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2 }}
        >
          Click categories to expand tech branches
        </motion.div>
      </div>
    </div>
  );
};

export default TechStackMindMap;
