# Greenstack Color Audit Report

Generated: 2025-11-17T03:47:28.343Z

## Executive Summary

- **Total Files Scanned:** 24
- **Files with Issues:** 2
- **Total Color Issues Found:** 48
- **Files Clean:** 22

## Issues by Pattern

| Pattern | Count | Files | Requires Replacement | Recommendation |
|---------|-------|-------|---------------------|----------------|
| HSL Colors | 48 | 2 | ⚠️  Review | Verify using CSS variables from theme system |

## Priority Files for Migration

| File | Issues | Critical Issues |
|------|--------|----------------|
| components\AnalyticsDashboard.jsx | 38 | 0 |
| App.jsx | 10 | 0 |

## Detailed Issues by File

### App.jsx

Total issues: 10 (0 require replacement)

**Line 3826:**
```jsx
? `hsl(${(bit.field.subindex * 137.5) % 360}, 70%, 50%)`
```

🟡 **HSL Colors**: `hsl(${(bit.field.subindex * 137.5)`
   - Verify using CSS variables from theme system

**Line 3827:**
```jsx
: 'hsl(var(--muted-foreground))';
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 3838:**
```jsx
backgroundColor: bit.field ? `${color}20` : 'hsl(var(--background))',
```

🟡 **HSL Colors**: `hsl(var(--background)`
   - Verify using CSS variables from theme system

**Line 3839:**
```jsx
borderColor: bit.field ? `${color}80` : 'hsl(var(--border))',
```

🟡 **HSL Colors**: `hsl(var(--border)`
   - Verify using CSS variables from theme system

**Line 3868:**
```jsx
const color = `hsl(${(item.subindex * 137.5) % 360}, 70%, 50%)`;
```

🟡 **HSL Colors**: `hsl(${(item.subindex * 137.5)`
   - Verify using CSS variables from theme system

**Line 4007:**
```jsx
? `hsl(${(bit.field.subindex * 137.5) % 360}, 70%, 50%)`
```

🟡 **HSL Colors**: `hsl(${(bit.field.subindex * 137.5)`
   - Verify using CSS variables from theme system

**Line 4008:**
```jsx
: 'hsl(var(--muted-foreground))';
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 4019:**
```jsx
backgroundColor: bit.field ? `${color}20` : 'hsl(var(--background))',
```

🟡 **HSL Colors**: `hsl(var(--background)`
   - Verify using CSS variables from theme system

**Line 4020:**
```jsx
borderColor: bit.field ? `${color}80` : 'hsl(var(--border))',
```

🟡 **HSL Colors**: `hsl(var(--border)`
   - Verify using CSS variables from theme system

**Line 4049:**
```jsx
const color = `hsl(${(item.subindex * 137.5) % 360}, 70%, 50%)`;
```

🟡 **HSL Colors**: `hsl(${(item.subindex * 137.5)`
   - Verify using CSS variables from theme system

---

### components\AnalyticsDashboard.jsx

Total issues: 38 (0 require replacement)

**Line 109:**
```jsx
color: 'hsl(var(--muted-foreground))',
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 113:**
```jsx
backgroundColor: 'hsl(var(--surface) / 0.9)',
```

🟡 **HSL Colors**: `hsl(var(--surface)`
   - Verify using CSS variables from theme system

**Line 114:**
```jsx
titleColor: 'hsl(var(--foreground))',
```

🟡 **HSL Colors**: `hsl(var(--foreground)`
   - Verify using CSS variables from theme system

**Line 115:**
```jsx
bodyColor: 'hsl(var(--muted-foreground))',
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 116:**
```jsx
borderColor: 'hsl(var(--border))',
```

🟡 **HSL Colors**: `hsl(var(--border)`
   - Verify using CSS variables from theme system

**Line 122:**
```jsx
ticks: { color: 'hsl(var(--muted-foreground))' },
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 123:**
```jsx
grid: { color: 'hsl(var(--border) / 0.1)' },
```

🟡 **HSL Colors**: `hsl(var(--border)`
   - Verify using CSS variables from theme system

**Line 126:**
```jsx
ticks: { color: 'hsl(var(--muted-foreground))' },
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 127:**
```jsx
grid: { color: 'hsl(var(--border) / 0.1)' },
```

🟡 **HSL Colors**: `hsl(var(--border)`
   - Verify using CSS variables from theme system

**Line 139:**
```jsx
color: 'hsl(var(--muted-foreground))',
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 144:**
```jsx
backgroundColor: 'hsl(var(--surface) / 0.9)',
```

🟡 **HSL Colors**: `hsl(var(--surface)`
   - Verify using CSS variables from theme system

**Line 145:**
```jsx
titleColor: 'hsl(var(--foreground))',
```

🟡 **HSL Colors**: `hsl(var(--foreground)`
   - Verify using CSS variables from theme system

**Line 146:**
```jsx
bodyColor: 'hsl(var(--muted-foreground))',
```

🟡 **HSL Colors**: `hsl(var(--muted-foreground)`
   - Verify using CSS variables from theme system

**Line 147:**
```jsx
borderColor: 'hsl(var(--border))',
```

🟡 **HSL Colors**: `hsl(var(--border)`
   - Verify using CSS variables from theme system

**Line 160:**
```jsx
backgroundColor: 'hsl(var(--brand-green) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--brand-green)`
   - Verify using CSS variables from theme system

**Line 161:**
```jsx
borderColor: 'hsl(var(--brand-green))',
```

🟡 **HSL Colors**: `hsl(var(--brand-green)`
   - Verify using CSS variables from theme system

**Line 174:**
```jsx
backgroundColor: 'hsl(var(--primary) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--primary)`
   - Verify using CSS variables from theme system

**Line 175:**
```jsx
borderColor: 'hsl(var(--primary))',
```

🟡 **HSL Colors**: `hsl(var(--primary)`
   - Verify using CSS variables from theme system

**Line 188:**
```jsx
'hsl(var(--brand-green) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--brand-green)`
   - Verify using CSS variables from theme system

**Line 189:**
```jsx
'hsl(var(--primary) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--primary)`
   - Verify using CSS variables from theme system

**Line 190:**
```jsx
'hsl(var(--secondary) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--secondary)`
   - Verify using CSS variables from theme system

**Line 191:**
```jsx
'hsl(var(--accent) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--accent)`
   - Verify using CSS variables from theme system

**Line 194:**
```jsx
'hsl(var(--brand-green))',
```

🟡 **HSL Colors**: `hsl(var(--brand-green)`
   - Verify using CSS variables from theme system

**Line 195:**
```jsx
'hsl(var(--primary))',
```

🟡 **HSL Colors**: `hsl(var(--primary)`
   - Verify using CSS variables from theme system

**Line 196:**
```jsx
'hsl(var(--secondary))',
```

🟡 **HSL Colors**: `hsl(var(--secondary)`
   - Verify using CSS variables from theme system

**Line 197:**
```jsx
'hsl(var(--accent))',
```

🟡 **HSL Colors**: `hsl(var(--accent)`
   - Verify using CSS variables from theme system

**Line 211:**
```jsx
backgroundColor: 'hsl(var(--secondary) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--secondary)`
   - Verify using CSS variables from theme system

**Line 212:**
```jsx
borderColor: 'hsl(var(--secondary))',
```

🟡 **HSL Colors**: `hsl(var(--secondary)`
   - Verify using CSS variables from theme system

**Line 229:**
```jsx
'hsl(var(--brand-green) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--brand-green)`
   - Verify using CSS variables from theme system

**Line 230:**
```jsx
'hsl(var(--primary) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--primary)`
   - Verify using CSS variables from theme system

**Line 231:**
```jsx
'hsl(var(--secondary) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--secondary)`
   - Verify using CSS variables from theme system

**Line 232:**
```jsx
'hsl(var(--accent) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--accent)`
   - Verify using CSS variables from theme system

**Line 233:**
```jsx
'hsl(var(--chart-5) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--chart-5)`
   - Verify using CSS variables from theme system

**Line 234:**
```jsx
'hsl(var(--chart-6) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--chart-6)`
   - Verify using CSS variables from theme system

**Line 235:**
```jsx
'hsl(var(--chart-7) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--chart-7)`
   - Verify using CSS variables from theme system

**Line 236:**
```jsx
'hsl(var(--error) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--error)`
   - Verify using CSS variables from theme system

**Line 237:**
```jsx
'hsl(var(--chart-9) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--chart-9)`
   - Verify using CSS variables from theme system

**Line 238:**
```jsx
'hsl(var(--success) / 0.7)',
```

🟡 **HSL Colors**: `hsl(var(--success)`
   - Verify using CSS variables from theme system

---

## Migration Recommendations

### Phase 1: Critical Replacements

Focus on files with hardcoded cyan, blue, and purple colors that should use brand green:


### Phase 2: Semantic Color Replacements

Replace gray/slate colors with semantic theme colors:


### Phase 3: Hex Color Cleanup

Replace all hardcoded hex colors with CSS variables:


## Color Replacement Guide

### Tailwind Class Replacements

| Old Class | New Class | Use Case |
|-----------|-----------|----------|
| `text-cyan-400` | `text-brand-green` | Brand identity, primary text |
| `text-cyan-500` | `text-brand-green` | Brand identity, primary text |
| `bg-cyan-500` | `bg-brand-green` | Brand backgrounds |
| `border-cyan-500` | `border-brand-green` | Brand borders |
| `text-blue-400` | `text-primary` | Primary interactive elements |
| `text-purple-400` | `text-secondary` or `text-accent` | Secondary/accent colors |
| `text-slate-400` | `text-muted-foreground` | Muted text |
| `text-gray-300` | `text-foreground-secondary` | Secondary text |
| `bg-slate-800` | `bg-surface` | Card/surface backgrounds |
| `border-slate-700` | `border-border` | Standard borders |

### CSS Variable Usage

```jsx
// BEFORE
<div style={{ color: '#00d4ff' }}>Text</div>

// AFTER
<div style={{ color: 'var(--brand-green)' }}>Text</div>
// OR
<div className="text-brand-green">Text</div>
```

---

**Next Steps:**
1. Review this report and prioritize files for migration
2. Use the replacement guide to update components systematically
3. Run this audit script after each batch of changes to track progress
4. Verify visual appearance in browser after each component migration
