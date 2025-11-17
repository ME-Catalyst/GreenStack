# Greenstack Theme Management System

## Overview

The Greenstack theme management system provides a complete UI/UX customization solution while maintaining brand consistency. The system enforces the immutable brand green color (#3DB60F) across all themes while allowing comprehensive customization of all other color properties.

## Architecture

### Components

1. **Backend API** (`theme_routes.py`)
   - RESTful API for theme CRUD operations
   - SQLite persistence for custom themes
   - Built-in preset themes (greenstack, forest, midnight, light)
   - Brand color validation

2. **Frontend Components**
   - **ThemeManager**: Main interface for theme selection and management
   - **ThemeEditor**: Comprehensive color customization interface
   - **ColorPicker**: Color input with accessibility checking
   - **ThemeContext**: React context for theme state management

3. **Configuration** (`config/themes.js`)
   - Centralized theme definitions
   - Theme validation utilities
   - CSS variable generation

## Features

### Brand Protection
- **Immutable Brand Green**: #3DB60F is locked across all themes
- Validation on both frontend and backend
- Visual indicators for locked colors

### Theme Presets
1. **Greenstack** (Default)
   - Official dark theme with brand green
   - Locked - cannot be modified

2. **Forest Green**
   - Deep forest tones
   - Dark mode optimized

3. **Midnight Green**
   - Dark teal with green accents
   - High contrast

4. **Light Green**
   - Clean light theme
   - Green accent highlights

### Custom Themes
- Create unlimited custom themes
- Based on preset themes
- Full color customization (except brand green)
- Export/Import functionality

### Color Groups
Organized semantic color categories:
- **Primary**: Main interactive elements
- **Secondary**: Supporting UI elements
- **Accent**: Highlights and special elements
- **Semantic**: Success, warning, error, info
- **Surfaces**: Backgrounds and containers
- **Borders**: Lines and dividers
- **Text**: Typography colors

### Accessibility
- WCAG AA/AAA contrast checking
- Real-time contrast ratio calculation
- Accessibility warnings for low contrast

## API Endpoints

### GET /api/themes/presets
Get all built-in theme presets.

**Response:**
```json
{
  "presets": [
    {
      "id": "greenstack",
      "name": "Greenstack",
      "description": "The official Greenstack brand theme",
      "locked": true,
      "mode": "dark",
      "colors": { ... }
    }
  ],
  "brand_green": "#3DB60F"
}
```

### GET /api/themes
List all themes (presets + custom).

**Response:**
```json
{
  "themes": [...],
  "brand_green": "#3DB60F"
}
```

### GET /api/themes/active
Get currently active theme.

**Response:**
```json
{
  "id": "greenstack",
  "name": "Greenstack",
  "colors": { ... }
}
```

### POST /api/themes
Create a new custom theme.

**Request:**
```json
{
  "name": "My Custom Theme",
  "description": "A personalized theme",
  "preset_id": "greenstack",
  "colors": {
    "brand": "#3DB60F",
    "primary": "#3DB60F",
    "secondary": "#2d5016",
    ...
  }
}
```

**Response:**
```json
{
  "id": "custom-1",
  "name": "My Custom Theme",
  "message": "Custom theme created successfully"
}
```

### PUT /api/themes/{theme_id}
Update an existing custom theme.

**Request:**
```json
{
  "name": "Updated Theme Name",
  "description": "Updated description",
  "colors": { ... }
}
```

### DELETE /api/themes/{theme_id}
Delete a custom theme (cannot delete active theme).

### POST /api/themes/{theme_id}/activate
Activate a theme (preset or custom).

**Response:**
```json
{
  "id": "custom-1",
  "name": "My Custom Theme",
  "message": "Custom theme activated"
}
```

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS user_themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    preset_id TEXT,
    is_active BOOLEAN DEFAULT 0,
    theme_data TEXT NOT NULL,  -- JSON string
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Usage

### Accessing Theme Manager

1. Navigate to **Admin Console**
2. Click the **Appearance** tab
3. Browse available themes

### Creating a Custom Theme

1. Click "Create Custom Theme"
2. Choose a base preset
3. Customize colors using the theme editor
4. Preview changes in real-time
5. Save your custom theme

### Editing Colors

1. Select a theme to edit
2. Click "Edit" button
3. Use tabbed interface to navigate color groups:
   - Primary Colors
   - Secondary Colors
   - Accent Colors
   - Semantic Colors
   - Surfaces
   - Borders
   - Text Colors
4. Each color has:
   - Visual color picker
   - Hex input field
   - Preview swatch
   - Contrast checker (for text colors)
5. Click "Preview" to see changes live
6. Click "Save" to persist changes

### Switching Themes

1. Browse available themes
2. Click "Activate" on desired theme
3. Theme applies immediately

### Export/Import

**Export:**
1. Click download icon on any theme card
2. JSON file downloads automatically

**Import:**
1. Click "Import" button
2. Select a theme JSON file
3. Theme is imported as new custom theme

## Color Validation

All themes must pass validation:

```javascript
// Brand color must be #3DB60F
colors.brand === '#3DB60F'

// Required colors must be present
const requiredColors = [
  'brand', 'primary', 'secondary', 'accent',
  'success', 'warning', 'error', 'info',
  'background', 'surface', 'border', 'foreground'
];
```

## Best Practices

### Creating Themes

1. **Start with a preset**: Base your custom theme on an existing preset
2. **Test contrast**: Ensure text colors have adequate contrast
3. **Preview extensively**: Use preview mode before saving
4. **Name descriptively**: Use clear, descriptive names
5. **Document changes**: Add meaningful descriptions

### Color Selection

1. **Maintain hierarchy**: Keep visual hierarchy consistent
2. **Accessibility first**: Always check WCAG compliance
3. **Test in context**: Preview theme in actual UI
4. **Consider states**: Test hover, active, disabled states
5. **Dark/Light modes**: Design for both if applicable

### Performance

1. Themes are cached in localStorage
2. CSS variables update instantly
3. No page refresh required
4. Minimal performance impact

## Troubleshooting

### Theme Not Applying

1. Check browser console for errors
2. Verify theme data in localStorage
3. Clear cache and reload
4. Check network requests to API

### Invalid Theme Error

- Ensure brand color is #3DB60F
- Verify all required colors are present
- Check hex color format (#RRGGBB)
- Validate JSON structure for imports

### Contrast Warnings

- Increase color difference
- Use WCAG contrast checker
- Test with actual content
- Consider accessibility requirements

## Development

### Adding New Color Properties

1. Update `ThemeColors` model in `theme_routes.py`
2. Add to `colorGroups` in `ThemeEditor.jsx`
3. Update CSS variable generation in `themes.js`
4. Add to validation in `validateTheme()`

### Creating New Presets

1. Define in `THEME_PRESETS` in `theme_routes.py`
2. Add to `THEME_PRESETS` in `config/themes.js`
3. Ensure brand color is #3DB60F
4. Test in both light and dark modes

### Extending API

1. Add route to `theme_routes.py`
2. Update frontend API calls
3. Update TypeScript types if using
4. Document new endpoint

## Security Considerations

1. **Brand Protection**: Brand color validation on backend
2. **Input Validation**: All color values validated
3. **SQL Injection**: Parameterized queries used
4. **XSS Prevention**: JSON sanitization
5. **Access Control**: Consider adding user authentication

## Future Enhancements

- [ ] User-specific themes (multi-user support)
- [ ] Theme sharing/marketplace
- [ ] Advanced color harmonies
- [ ] CSS variable export
- [ ] Theme versioning
- [ ] Undo/redo in editor
- [ ] Color palette suggestions
- [ ] AI-powered theme generation
- [ ] Theme analytics
- [ ] Seasonal/event themes

## Support

For issues or questions:
1. Check documentation
2. Review error messages
3. Check browser console
4. Verify API connectivity
5. Contact support team

## License

Part of the Greenstack project - MIT License
