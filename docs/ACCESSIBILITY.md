# GreenStack Accessibility Guide

## Overview

GreenStack follows WCAG 2.1 Level AA guidelines to ensure the application is accessible to all users, including those with disabilities.

## Implemented Accessibility Features

### Semantic HTML

- `<aside>` for sidebar navigation
- `<nav>` for navigation menus
- `<header>` for page headers
- `<main>` for main content
- `<section>` for content sections
- `<article>` for self-contained content

### ARIA Labels and Roles

#### Navigation
- Sidebar has `role="navigation"` and `aria-label="Main navigation"`
- Navigation items have `aria-current="page"` for active items
- Navigation items have descriptive `aria-label` including badge counts

#### Buttons and Controls
- Collapse/expand button has dynamic `aria-label` and `aria-expanded`
- All icon-only buttons have descriptive `aria-label`
- Decorative icons have `aria-hidden="true"`

#### Content Regions
- Main sections have `aria-labelledby` pointing to their heading
- Headings follow proper hierarchy (h1 → h2 → h3)

### Keyboard Navigation

- All interactive elements are keyboard accessible
- Tab order follows logical flow
- Keyboard shortcuts available (see Keyboard Shortcuts guide)
- Focus indicators visible on all interactive elements

### Color and Contrast

- All text meets WCAG AA contrast requirements (4.5:1 for normal text, 3:1 for large text)
- UI components have sufficient contrast
- Information not conveyed by color alone
- Theme toggle available for user preference

### Focus Management

- Visible focus indicators on all interactive elements
- Focus trap in modals and dialogs
- Focus restoration when closing modals
- Skip to main content link (can be added)

### Screen Reader Support

- Semantic HTML ensures proper reading order
- ARIA labels provide context for screen readers
- Status messages announced via ARIA live regions
- Form inputs have associated labels

## Accessibility Checklist

### High Priority (WCAG A)

- [x] All images have alt text or aria-label
- [x] Form inputs have associated labels
- [x] Keyboard navigation works for all functionality
- [x] Page has a descriptive title
- [x] Language of page specified in HTML
- [x] No keyboard traps
- [x] Link text is descriptive

### Medium Priority (WCAG AA)

- [x] Color contrast meets 4.5:1 ratio
- [x] Text can be resized to 200% without loss of content
- [x] Headings and labels are descriptive
- [x] Focus is visible
- [x] Multiple ways to navigate (menu, search, shortcuts)
- [x] Consistent navigation
- [x] Error identification and suggestions
- [ ] Labels or instructions provided for user input (partial)

### Future Enhancements (WCAG AAA / Best Practices)

- [ ] Add skip to main content link
- [ ] Implement comprehensive form validation with error messages
- [ ] Add more ARIA live regions for dynamic updates
- [ ] Provide text alternatives for time-based media
- [ ] Add help documentation for complex interactions
- [ ] Implement breadcrumb navigation
- [ ] Add progress indicators for long-running operations

## Testing

### Automated Testing

Use these tools for automated accessibility testing:

```bash
# Install axe-core for automated testing
npm install --save-dev @axe-core/react

# Run Lighthouse accessibility audit
lighthouse http://localhost:5173 --only-categories=accessibility --view
```

### Manual Testing

#### Keyboard Navigation Test

1. Use Tab key to navigate through all interactive elements
2. Use Enter/Space to activate buttons and links
3. Use Arrow keys for lists and menus
4. Use Escape to close modals and dialogs
5. Ensure focus indicator is always visible

#### Screen Reader Test

Test with popular screen readers:
- **NVDA** (Windows, free): https://www.nvaccess.org/
- **JAWS** (Windows, paid): https://www.freedomscientific.com/products/software/jaws/
- **VoiceOver** (macOS/iOS, built-in): Cmd+F5 to enable
- **TalkBack** (Android, built-in): Settings → Accessibility

#### Color Contrast Test

1. Use browser dev tools color picker
2. Check contrast ratios
3. Test with color blindness simulators
4. Try using application in grayscale mode

### Testing Checklist

- [ ] Navigate entire app using only keyboard
- [ ] Test with screen reader (NVDA/JAWS/VoiceOver)
- [ ] Verify color contrast meets requirements
- [ ] Test at 200% zoom
- [ ] Test with browser accessibility tools
- [ ] Test with high contrast mode
- [ ] Verify ARIA labels are descriptive
- [ ] Check heading hierarchy
- [ ] Verify form validation messages
- [ ] Test error handling and recovery

## Code Guidelines

### General Principles

1. **Use semantic HTML first**
   - Don't use `<div>` when `<button>` is appropriate
   - Don't use `<div>` when `<nav>`, `<main>`, `<article>` are appropriate

2. **Add ARIA only when necessary**
   - Native HTML is usually better than ARIA
   - Use ARIA to enhance, not replace, semantic HTML

3. **Always provide text alternatives**
   - Alt text for images
   - Aria-label for icon-only buttons
   - Captions/transcripts for media

4. **Maintain focus management**
   - Preserve focus order
   - Return focus after modal closes
   - Implement focus traps in modals

### Examples

#### Good: Semantic button with aria-label

```jsx
<button
  onClick={handleClick}
  aria-label="Delete device"
  className="..."
>
  <Trash2 className="w-4 h-4" aria-hidden="true" />
</button>
```

#### Bad: Div pretending to be button

```jsx
{/* DON'T DO THIS */}
<div onClick={handleClick}>
  <Trash2 className="w-4 h-4" />
</div>
```

#### Good: Navigation with proper semantics

```jsx
<nav aria-label="Primary navigation">
  <button
    aria-current={active ? 'page' : undefined}
    aria-label="Overview"
  >
    <Home aria-hidden="true" />
    Overview
  </button>
</nav>
```

#### Good: Form with labels

```jsx
<label htmlFor="device-name">
  Device Name
  <input
    id="device-name"
    type="text"
    aria-required="true"
    aria-describedby="name-help"
  />
</label>
<p id="name-help" className="text-sm text-muted-foreground">
  Enter a unique name for the device
</p>
```

#### Good: Error message with live region

```jsx
<div
  role="alert"
  aria-live="assertive"
  className="error-message"
>
  Error: Failed to import device. Please try again.
</div>
```

#### Good: Heading hierarchy

```jsx
<main>
  <h1>GreenStack Dashboard</h1>
  <section aria-labelledby="devices-heading">
    <h2 id="devices-heading">IO-Link Devices</h2>
    <article>
      <h3>Device Details</h3>
      ...
    </article>
  </section>
</main>
```

## Common Issues and Fixes

### Issue: Missing alt text on images

**Problem:**
```jsx
<img src="/device-icon.png" />
```

**Fix:**
```jsx
<img src="/device-icon.png" alt="Device icon" />
{/* Or if decorative: */}
<img src="/device-icon.png" alt="" role="presentation" />
```

### Issue: Icon-only button without label

**Problem:**
```jsx
<button onClick={handleDelete}>
  <Trash2 />
</button>
```

**Fix:**
```jsx
<button onClick={handleDelete} aria-label="Delete device">
  <Trash2 aria-hidden="true" />
</button>
```

### Issue: Div used as button

**Problem:**
```jsx
<div onClick={handleClick} className="button">
  Click me
</div>
```

**Fix:**
```jsx
<button onClick={handleClick} className="button">
  Click me
</button>
```

### Issue: Form input without label

**Problem:**
```jsx
<input type="text" placeholder="Search..." />
```

**Fix:**
```jsx
<label htmlFor="search-input" className="sr-only">
  Search devices
</label>
<input
  id="search-input"
  type="text"
  placeholder="Search..."
  aria-label="Search devices"
/>
```

### Issue: Poor heading hierarchy

**Problem:**
```jsx
<h1>Dashboard</h1>
<h3>Devices</h3>  {/* Skipped h2 */}
```

**Fix:**
```jsx
<h1>Dashboard</h1>
<h2>Devices</h2>  {/* Proper hierarchy */}
<h3>Device Details</h3>
```

### Issue: No focus indicator

**Problem:**
```css
button:focus {
  outline: none;  /* DON'T DO THIS */
}
```

**Fix:**
```css
button:focus-visible {
  outline: 2px solid var(--brand-green);
  outline-offset: 2px;
}
```

## Resources

### WCAG Guidelines
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WCAG 2.1 Understanding Docs](https://www.w3.org/WAI/WCAG21/Understanding/)

### ARIA
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [ARIA Roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)

### Testing Tools
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE Browser Extension](https://wave.webaim.org/extension/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Pa11y](https://pa11y.org/)

### Screen Readers
- [NVDA](https://www.nvaccess.org/) - Free, Windows
- [JAWS](https://www.freedomscientific.com/products/software/jaws/) - Paid, Windows
- VoiceOver - Built-in, macOS/iOS
- TalkBack - Built-in, Android

### Learn More
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [Inclusive Components](https://inclusive-components.design/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

## Support

If you encounter accessibility issues:
1. Open a GitHub issue with "Accessibility" label
2. Provide details about the issue and how to reproduce
3. Include which assistive technology you're using
4. Suggest improvements if possible

We're committed to making GreenStack accessible to everyone!

---

**Last Updated:** 2025-01-18
**WCAG Level:** AA (target)
**Maintained by:** Frontend Team
