import React, { useState, useEffect } from 'react';
import {
  Palette, Check, Edit, Trash2, Plus, Download, Upload,
  Lock, Moon, Sun, Sparkles, RefreshCw
} from 'lucide-react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  Button,
  Badge,
  Alert,
  AlertTitle,
  AlertDescription,
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from './ui';
import { useTheme } from '../contexts/ThemeContext';
import ThemeEditor from './ThemeEditor';

/**
 * ThemeManager Component
 *
 * Main interface for theme management
 * - Display current active theme
 * - List of preset themes with preview cards
 * - Quick preset switching
 * - Edit/customize theme functionality
 * - Export/Import theme
 */
const ThemeManager = ({ API_BASE = '', toast }) => {
  const { currentTheme, setThemePreset, setCustomTheme, availablePresets, brandGreen } = useTheme();
  const [themes, setThemes] = useState([]);
  const [activeThemeId, setActiveThemeId] = useState('greenstack');
  const [loading, setLoading] = useState(true);
  const [showEditor, setShowEditor] = useState(false);
  const [editingTheme, setEditingTheme] = useState(null);

  useEffect(() => {
    loadThemes();
    loadActiveTheme();
  }, []);

  const loadThemes = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/themes`);
      setThemes(response.data.themes || []);
    } catch (error) {
      console.error('Failed to load themes:', error);
      toast?.({
        title: 'Error',
        description: 'Failed to load themes',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const loadActiveTheme = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/themes/active`);
      const activeTheme = response.data;
      setActiveThemeId(activeTheme.id || 'greenstack');
    } catch (error) {
      console.error('Failed to load active theme:', error);
    }
  };

  const handleActivateTheme = async (themeId) => {
    try {
      const response = await axios.post(`${API_BASE}/api/themes/${themeId}/activate`);
      const activatedTheme = response.data;

      // Update local state
      setActiveThemeId(themeId);

      // Apply theme through context
      if (themeId.startsWith('custom-')) {
        setCustomTheme(activatedTheme);
      } else {
        setThemePreset(themeId);
      }

      toast?.({
        title: 'Success',
        description: `Theme "${activatedTheme.name}" activated`,
      });

      // Reload themes to update active status
      loadThemes();
    } catch (error) {
      console.error('Failed to activate theme:', error);
      toast?.({
        title: 'Error',
        description: 'Failed to activate theme',
        variant: 'destructive'
      });
    }
  };

  const handleEditTheme = (theme) => {
    setEditingTheme(theme);
    setShowEditor(true);
  };

  const handleCreateCustomTheme = () => {
    // Start with greenstack as base
    const baseTheme = availablePresets.find(p => p.id === 'greenstack') || availablePresets[0];
    setEditingTheme({
      ...baseTheme,
      name: 'New Custom Theme',
      description: 'A custom theme based on ' + baseTheme.name,
      preset_id: baseTheme.id
    });
    setShowEditor(true);
  };

  const handleSaveTheme = async (themeData) => {
    try {
      let response;

      if (editingTheme?.id?.startsWith('custom-')) {
        // Update existing custom theme
        response = await axios.put(
          `${API_BASE}/api/themes/${editingTheme.id}`,
          {
            name: themeData.name,
            description: themeData.description,
            colors: themeData.colors
          }
        );
      } else {
        // Create new custom theme
        response = await axios.post(`${API_BASE}/api/themes`, {
          name: themeData.name,
          description: themeData.description,
          preset_id: editingTheme?.preset_id || editingTheme?.id,
          colors: themeData.colors
        });
      }

      toast?.({
        title: 'Success',
        description: `Theme "${themeData.name}" saved successfully`,
      });

      setShowEditor(false);
      setEditingTheme(null);
      loadThemes();
    } catch (error) {
      console.error('Failed to save theme:', error);
      toast?.({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to save theme',
        variant: 'destructive'
      });
    }
  };

  const handleDeleteTheme = async (themeId) => {
    if (!confirm('Are you sure you want to delete this custom theme?')) {
      return;
    }

    try {
      await axios.delete(`${API_BASE}/api/themes/${themeId}`);

      toast?.({
        title: 'Success',
        description: 'Theme deleted successfully',
      });

      loadThemes();
    } catch (error) {
      console.error('Failed to delete theme:', error);
      toast?.({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to delete theme',
        variant: 'destructive'
      });
    }
  };

  const handleExportTheme = (theme) => {
    const dataStr = JSON.stringify(theme, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);

    const exportFileDefaultName = `${theme.name.replace(/\s+/g, '-').toLowerCase()}-theme.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();

    toast?.({
      title: 'Success',
      description: 'Theme exported successfully',
    });
  };

  const handleImportTheme = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';

    input.onchange = (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async (event) => {
        try {
          const importedTheme = JSON.parse(event.target.result);

          // Validate that brand color is correct
          if (importedTheme.colors?.brand !== brandGreen) {
            toast?.({
              title: 'Warning',
              description: 'Imported theme has incorrect brand color. It will be corrected.',
              variant: 'default'
            });
            importedTheme.colors.brand = brandGreen;
          }

          // Create as new custom theme
          const response = await axios.post(`${API_BASE}/api/themes`, {
            name: importedTheme.name || 'Imported Theme',
            description: importedTheme.description || 'An imported theme',
            preset_id: importedTheme.preset_id,
            colors: importedTheme.colors
          });

          toast?.({
            title: 'Success',
            description: `Theme "${importedTheme.name}" imported successfully`,
          });

          loadThemes();
        } catch (error) {
          console.error('Failed to import theme:', error);
          toast?.({
            title: 'Error',
            description: 'Failed to import theme. Check file format.',
            variant: 'destructive'
          });
        }
      };

      reader.readAsText(file);
    };

    input.click();
  };

  const ThemePreviewCard = ({ theme }) => {
    const isActive = theme.id === activeThemeId;
    const isCustom = theme.custom || theme.id?.startsWith('custom-');
    const isLocked = theme.locked;

    return (
      <Card className={`relative overflow-hidden transition-all ${
        isActive
          ? 'border-brand-green shadow-lg shadow-brand-green/20'
          : 'border-border hover:border-primary/50'
      }`}>
        {/* Color Preview Bar */}
        <div className="h-16 flex">
          <div className="flex-1" style={{ backgroundColor: theme.colors?.primary || '#3DB60F' }} />
          <div className="flex-1" style={{ backgroundColor: theme.colors?.secondary || '#2d5016' }} />
          <div className="flex-1" style={{ backgroundColor: theme.colors?.accent || '#51cf66' }} />
          <div className="flex-1" style={{ backgroundColor: theme.colors?.background || '#0a0e27' }} />
        </div>

        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-foreground flex items-center gap-2">
                {theme.name}
                {isActive && (
                  <Check className="w-4 h-4 text-brand-green" />
                )}
                {isLocked && (
                  <Lock className="w-3 h-3 text-warning" />
                )}
              </CardTitle>
              <CardDescription className="mt-1">
                {theme.description || 'No description'}
              </CardDescription>
            </div>
            <div className="flex gap-1">
              <Badge variant={theme.mode === 'light' ? 'default' : 'secondary'}>
                {theme.mode === 'light' ? (
                  <Sun className="w-3 h-3 mr-1" />
                ) : (
                  <Moon className="w-3 h-3 mr-1" />
                )}
                {theme.mode}
              </Badge>
              {isCustom && (
                <Badge variant="outline" className="border-primary text-primary">
                  <Sparkles className="w-3 h-3 mr-1" />
                  Custom
                </Badge>
              )}
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <div className="flex gap-2">
            {!isActive && (
              <Button
                size="sm"
                onClick={() => handleActivateTheme(theme.id)}
                className="flex-1"
              >
                <Check className="w-4 h-4 mr-1" />
                Activate
              </Button>
            )}

            {isActive && (
              <Button
                size="sm"
                variant="outline"
                className="flex-1 border-brand-green text-brand-green"
                disabled
              >
                <Check className="w-4 h-4 mr-1" />
                Active
              </Button>
            )}

            {!isLocked && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => handleEditTheme(theme)}
              >
                <Edit className="w-4 h-4 mr-1" />
                Edit
              </Button>
            )}

            <Button
              size="sm"
              variant="ghost"
              onClick={() => handleExportTheme(theme)}
            >
              <Download className="w-4 h-4" />
            </Button>

            {isCustom && !isActive && (
              <Button
                size="sm"
                variant="ghost"
                onClick={() => handleDeleteTheme(theme.id)}
              >
                <Trash2 className="w-4 h-4 text-error" />
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <RefreshCw className="w-8 h-8 text-brand-green animate-spin" />
      </div>
    );
  }

  if (showEditor) {
    return (
      <ThemeEditor
        baseTheme={editingTheme}
        onSave={handleSaveTheme}
        onCancel={() => {
          setShowEditor(false);
          setEditingTheme(null);
        }}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground flex items-center gap-2">
            <Palette className="w-6 h-6 text-brand-green" />
            Theme Manager
          </h2>
          <p className="text-muted-foreground mt-1">
            Customize your Greenstack appearance
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleImportTheme} variant="outline">
            <Upload className="w-4 h-4 mr-2" />
            Import
          </Button>
          <Button onClick={handleCreateCustomTheme}>
            <Plus className="w-4 h-4 mr-2" />
            Create Custom Theme
          </Button>
        </div>
      </div>

      {/* Brand Color Info */}
      <Alert className="bg-warning/10 border-warning/50">
        <Lock className="w-4 h-4 text-warning" />
        <AlertTitle className="text-warning">Brand Identity Protected</AlertTitle>
        <AlertDescription className="text-foreground">
          The Greenstack brand green ({brandGreen}) is locked and cannot be modified across all themes.
          All other colors can be customized to match your preferences.
        </AlertDescription>
      </Alert>

      {/* Current Active Theme */}
      {currentTheme && (
        <Card className="bg-gradient-to-br from-brand-green/10 via-primary/10 to-secondary/10 border-brand-green/30">
          <CardHeader>
            <CardTitle className="text-foreground flex items-center gap-2">
              <Check className="w-5 h-5 text-brand-green" />
              Currently Active
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-lg font-semibold text-foreground">
                  {themes.find(t => t.id === activeThemeId)?.name || 'Greenstack'}
                </p>
                <p className="text-sm text-muted-foreground">
                  {themes.find(t => t.id === activeThemeId)?.description || 'The official Greenstack brand theme'}
                </p>
              </div>
              <Badge variant="outline" className="border-brand-green text-brand-green">
                <Sparkles className="w-3 h-3 mr-1" />
                Active
              </Badge>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Theme Grid */}
      <div>
        <h3 className="text-lg font-semibold text-foreground mb-4">Available Themes</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {themes.map(theme => (
            <ThemePreviewCard key={theme.id} theme={theme} />
          ))}
        </div>
      </div>

      {/* Empty State */}
      {themes.length === 0 && (
        <Card className="border-dashed">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Palette className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground text-center mb-4">
              No custom themes yet. Create your first custom theme to get started.
            </p>
            <Button onClick={handleCreateCustomTheme}>
              <Plus className="w-4 h-4 mr-2" />
              Create Custom Theme
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ThemeManager;
