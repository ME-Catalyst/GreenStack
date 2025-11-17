/**
 * Debug utility to check theme state
 * Run this in browser console: window.debugTheme()
 */

export function debugTheme() {
  console.log('=== THEME DEBUG INFO ===');
  console.log('');

  // Check localStorage
  console.log('LocalStorage:');
  console.log('  - theme-mode:', localStorage.getItem('greenstack-theme-mode'));
  console.log('  - theme-preset:', localStorage.getItem('greenstack-theme-preset'));
  console.log('  - custom-theme:', localStorage.getItem('greenstack-custom-theme'));
  console.log('');

  // Check HTML classes
  console.log('HTML Element Classes:');
  console.log('  - classList:', document.documentElement.classList.toString());
  console.log('  - has "dark":', document.documentElement.classList.contains('dark'));
  console.log('  - has "light":', document.documentElement.classList.contains('light'));
  console.log('');

  // Check CSS variables
  console.log('CSS Variables:');
  const root = document.documentElement;
  const styles = getComputedStyle(root);
  console.log('  - --background:', styles.getPropertyValue('--background'));
  console.log('  - --foreground:', styles.getPropertyValue('--foreground'));
  console.log('  - --brand-green:', styles.getPropertyValue('--brand-green'));
  console.log('');

  // Check system preference
  console.log('System Preference:');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  console.log('  - prefers-dark:', prefersDark);
  console.log('  - prefers-light:', prefersLight);
  console.log('');

  console.log('======================');
}

// Make it available globally
if (typeof window !== 'undefined') {
  window.debugTheme = debugTheme;
}
