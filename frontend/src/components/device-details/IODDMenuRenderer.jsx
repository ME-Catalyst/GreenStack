import React, { useState, useEffect } from 'react';
import {
  Card, CardHeader, CardContent, CardTitle, CardDescription,
  Button, Badge, Tabs, TabsList, TabsTrigger, TabsContent
} from '@/components/ui';
import {
  Menu, User, Wrench, Eye, Stethoscope, Info,
  ChevronRight, AlertCircle, Loader2
} from 'lucide-react';
import axios from 'axios';

/**
 * IODD Menu Renderer Component
 *
 * Renders the complete IODD UserInterface menu structure for an IO-Link device
 * exactly as defined in the IODD file, with proper text resolution and parameter data.
 *
 * Features:
 * - Role-based menu sets (Observer, Maintenance, Specialist)
 * - Tab interface for each menu (Identification, Parameter, Observation, Diagnosis)
 * - Parameter display with metadata (type, range, units, enumerations)
 * - Support for VariableRef, RecordItemRef, Button, and MenuRef menu items
 */
const IODDMenuRenderer = ({ deviceId, API_BASE }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [menuData, setMenuData] = useState(null);
  const [selectedRole, setSelectedRole] = useState('observer');
  const [activeMenu, setActiveMenu] = useState(null);

  useEffect(() => {
    if (deviceId) {
      loadMenuData();
    }
  }, [deviceId]);

  const loadMenuData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`${API_BASE}/api/iodd/${deviceId}/menus`);
      setMenuData(response.data);

      // Set default active menu from first role set
      if (response.data.role_sets && response.data.role_sets.length > 0) {
        const defaultRoleSet = response.data.role_sets.find(rs => rs.role_type === 'observer')
          || response.data.role_sets[0];
        setSelectedRole(defaultRoleSet.role_type);
        setActiveMenu(defaultRoleSet.identification_menu || defaultRoleSet.parameter_menu || defaultRoleSet.observation_menu);
      }
    } catch (err) {
      console.error('Error loading menu data:', err);
      setError(err.response?.data?.detail || 'Failed to load menu structure');
    } finally {
      setLoading(false);
    }
  };

  const getRoleIcon = (role) => {
    switch (role) {
      case 'observer': return Eye;
      case 'maintenance': return Wrench;
      case 'specialist': return Stethoscope;
      default: return User;
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'observer': return 'bg-blue-500/20 text-blue-400 border-blue-500/50';
      case 'maintenance': return 'bg-orange-500/20 text-orange-400 border-orange-500/50';
      case 'specialist': return 'bg-purple-500/20 text-purple-400 border-purple-500/50';
      default: return 'bg-secondary text-foreground border-border';
    }
  };

  const getAccessRightColor = (accessRight) => {
    switch (accessRight) {
      case 'ro': return 'bg-blue-500/20 text-blue-400 border-blue-500/50';
      case 'rw': return 'bg-green-500/20 text-green-400 border-green-500/50';
      case 'wo': return 'bg-warning/20 text-warning border-warning/50';
      default: return 'bg-secondary text-foreground border-border';
    }
  };

  const renderMenuItem = (item, index) => {
    return (
      <div
        key={index}
        className="p-4 rounded-lg bg-secondary/30 border border-border hover:border-brand-green/50 transition-all"
      >
        <div className="flex items-start justify-between gap-4">
          {/* Left: Parameter Info */}
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h4 className="font-semibold text-foreground">
                {item.parameter_name || item.variable_id || item.record_item_ref || 'Unknown'}
              </h4>
              {item.type === 'RecordItemRef' && item.subindex && (
                <Badge className="bg-brand-green/20 text-brand-green text-xs">
                  Subindex: {item.subindex}
                </Badge>
              )}
            </div>

            {item.parameter_description && (
              <p className="text-sm text-muted-foreground mb-2">
                {item.parameter_description}
              </p>
            )}

            {/* Parameter Metadata */}
            <div className="flex flex-wrap gap-2 mt-2">
              {item.data_type && (
                <Badge className="bg-secondary text-foreground text-xs">
                  Type: {item.data_type}
                </Badge>
              )}
              {item.access_right_restriction && (
                <Badge className={`text-xs ${getAccessRightColor(item.access_right_restriction)}`}>
                  {item.access_right_restriction.toUpperCase()}
                </Badge>
              )}
              {item.unit_code && (
                <Badge className="bg-secondary text-foreground text-xs">
                  Unit: {item.unit_code}
                </Badge>
              )}
              {item.display_format && (
                <Badge className="bg-secondary text-foreground text-xs">
                  Format: {item.display_format}
                </Badge>
              )}
            </div>

            {/* Value Range */}
            {(item.min_value !== null && item.min_value !== undefined) && (item.max_value !== null && item.max_value !== undefined) && (
              <div className="mt-2 p-2 rounded bg-brand-green/10 border border-brand-green/30">
                <p className="text-xs text-brand-green">
                  Range: {item.min_value} - {item.max_value}
                </p>
              </div>
            )}

            {/* Enumeration Values */}
            {item.enumeration_values && Object.keys(item.enumeration_values).length > 0 && (
              <div className="mt-2 p-2 rounded bg-success/10 border border-success/30 max-h-32 overflow-y-auto">
                <p className="text-xs text-success font-semibold mb-1">Valid Values:</p>
                <div className="space-y-1">
                  {Object.entries(item.enumeration_values).map(([value, name]) => (
                    <div key={value} className="text-xs text-foreground flex items-center gap-2">
                      <span className="font-mono bg-secondary px-2 py-0.5 rounded">{value}</span>
                      <ChevronRight className="w-3 h-3 text-muted-foreground" />
                      <span>{name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right: Default Value (if available) */}
          {item.default_value && (
            <div className="text-right">
              <p className="text-xs text-muted-foreground">Default</p>
              <p className="text-lg font-mono text-foreground">{item.default_value}</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderMenu = (menuId) => {
    const menu = menuData.menus.find(m => m.menu_id === menuId);
    if (!menu) return null;

    return (
      <div className="space-y-3">
        {menu.items.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            <Menu className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No items in this menu</p>
          </div>
        ) : (
          menu.items.map((item, idx) => renderMenuItem(item, idx))
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-brand-green mb-4" />
        <p className="text-muted-foreground">Loading menu structure...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Card className="bg-error/10 border-error/30">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-error flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-error mb-1">Failed to Load Menu Structure</h4>
              <p className="text-sm text-muted-foreground">{error}</p>
              <Button
                onClick={loadMenuData}
                className="mt-3 bg-error/20 hover:bg-error/30 text-error"
                size="sm"
              >
                Retry
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!menuData || menuData.menus.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        <Menu className="w-12 h-12 mx-auto mb-2 opacity-50" />
        <p>No menu structure available for this device</p>
      </div>
    );
  }

  const currentRoleSet = menuData.role_sets.find(rs => rs.role_type === selectedRole);

  return (
    <div className="space-y-4">
      {/* Role Selector */}
      <Card className="bg-gradient-to-r from-brand-green/5 to-brand-green/10 border-brand-green/30">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Menu className="w-5 h-5 text-brand-green" />
            IODD Menu Interface
          </CardTitle>
          <CardDescription>
            Select a role to view the corresponding menu set
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {menuData.role_sets.map((roleSet) => {
              const RoleIcon = getRoleIcon(roleSet.role_type);
              return (
                <Button
                  key={roleSet.role_type}
                  onClick={() => {
                    setSelectedRole(roleSet.role_type);
                    setActiveMenu(roleSet.identification_menu || roleSet.parameter_menu || roleSet.observation_menu);
                  }}
                  className={selectedRole === roleSet.role_type
                    ? getRoleColor(roleSet.role_type)
                    : 'bg-secondary/50 text-muted-foreground hover:bg-secondary'}
                >
                  <RoleIcon className="w-4 h-4 mr-2" />
                  {roleSet.role_type.charAt(0).toUpperCase() + roleSet.role_type.slice(1)} Role
                </Button>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Menu Tabs */}
      {currentRoleSet && (
        <Card className="bg-card/80 backdrop-blur-sm border-border">
          <CardHeader>
            <CardTitle className="text-foreground">
              {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)} Menus
            </CardTitle>
            <CardDescription>
              IO-Link device parameters organized by menu type
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeMenu} onValueChange={setActiveMenu} className="w-full">
              <TabsList className="bg-secondary/50 border border-border p-1 flex flex-wrap h-auto">
                {currentRoleSet.identification_menu && (
                  <TabsTrigger
                    value={currentRoleSet.identification_menu}
                    className="data-[state=active]:bg-brand-green/20 data-[state=active]:text-brand-green"
                  >
                    <Info className="w-4 h-4 mr-2" />
                    Identification
                  </TabsTrigger>
                )}
                {currentRoleSet.parameter_menu && (
                  <TabsTrigger
                    value={currentRoleSet.parameter_menu}
                    className="data-[state=active]:bg-brand-green/20 data-[state=active]:text-brand-green"
                  >
                    <Wrench className="w-4 h-4 mr-2" />
                    Parameters
                  </TabsTrigger>
                )}
                {currentRoleSet.observation_menu && (
                  <TabsTrigger
                    value={currentRoleSet.observation_menu}
                    className="data-[state=active]:bg-brand-green/20 data-[state=active]:text-brand-green"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    Observation
                  </TabsTrigger>
                )}
                {currentRoleSet.diagnosis_menu && (
                  <TabsTrigger
                    value={currentRoleSet.diagnosis_menu}
                    className="data-[state=active]:bg-brand-green/20 data-[state=active]:text-brand-green"
                  >
                    <Stethoscope className="w-4 h-4 mr-2" />
                    Diagnosis
                  </TabsTrigger>
                )}
              </TabsList>

              {/* Menu Content */}
              {currentRoleSet.identification_menu && (
                <TabsContent value={currentRoleSet.identification_menu} className="mt-4">
                  {renderMenu(currentRoleSet.identification_menu)}
                </TabsContent>
              )}
              {currentRoleSet.parameter_menu && (
                <TabsContent value={currentRoleSet.parameter_menu} className="mt-4">
                  {renderMenu(currentRoleSet.parameter_menu)}
                </TabsContent>
              )}
              {currentRoleSet.observation_menu && (
                <TabsContent value={currentRoleSet.observation_menu} className="mt-4">
                  {renderMenu(currentRoleSet.observation_menu)}
                </TabsContent>
              )}
              {currentRoleSet.diagnosis_menu && (
                <TabsContent value={currentRoleSet.diagnosis_menu} className="mt-4">
                  {renderMenu(currentRoleSet.diagnosis_menu)}
                </TabsContent>
              )}
            </Tabs>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default IODDMenuRenderer;
