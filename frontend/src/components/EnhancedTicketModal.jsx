import React, { useState, useEffect, useRef } from 'react';
import { X, AlertCircle, CheckCircle2, Paperclip, Camera, FileText, Trash2, Download } from 'lucide-react';
import axios from 'axios';
import html2canvas from 'html2canvas';

/**
 * Enhanced modal for creating tickets with auto-fill, screenshots, logs, and multi-file attachments
 *
 * Features:
 * - Context-aware auto-generated titles with timestamps
 * - Automatic screenshot capture on open
 * - Log collection from backend
 * - Multi-file attachments (any type, multiple files)
 * - Smart tagging based on current page/context
 * - Pre-filled description with system context
 */
const EnhancedTicketModal = ({
  isOpen,
  onClose,
  context = {}, // {page, section, deviceType, deviceId, deviceName, vendorName, productCode, etc.}
  API_BASE = ''
}) => {
  const fileInputRef = useRef(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    eds_reference: '',
    priority: 'medium',
    category: 'data_issue'
  });

  const [attachments, setAttachments] = useState([]); // Files to upload
  const [screenshot, setScreenshot] = useState(null); // Auto-captured screenshot
  const [logs, setLogs] = useState(''); // Collected logs
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [isCapturing, setIsCapturing] = useState(false);

  // Auto-fill form when modal opens with context
  useEffect(() => {
    if (isOpen && context) {
      // Generate auto-title with timestamp
      const timestamp = new Date().toLocaleString();
      const page = context.page || 'Unknown Page';
      const section = context.section || '';

      let autoTitle = `[${page}${section ? ` - ${section}` : ''}] Issue reported ${timestamp}`;

      // Generate context-aware description
      let autoDescription = `**Automatically Generated Report**\n\n`;
      autoDescription += `**Context:**\n`;
      autoDescription += `- Page: ${page}\n`;
      if (section) autoDescription += `- Section: ${section}\n`;
      if (context.deviceType) autoDescription += `- Device Type: ${context.deviceType}\n`;
      if (context.deviceName) autoDescription += `- Device: ${context.deviceName}\n`;
      if (context.vendorName) autoDescription += `- Vendor: ${context.vendorName}\n`;
      if (context.productCode) autoDescription += `- Product Code: ${context.productCode}\n`;
      if (context.activeTab) autoDescription += `- Active Tab: ${context.activeTab}\n`;
      autoDescription += `- Timestamp: ${timestamp}\n`;
      autoDescription += `- URL: ${window.location.href}\n`;
      autoDescription += `- User Agent: ${navigator.userAgent}\n\n`;
      autoDescription += `**Issue Description:**\n`;
      autoDescription += `(Please describe the issue you encountered)\n\n`;
      autoDescription += `**Steps to Reproduce:**\n`;
      autoDescription += `1. \n2. \n3. \n\n`;
      autoDescription += `**Expected Behavior:**\n\n`;
      autoDescription += `**Actual Behavior:**\n\n`;

      setFormData({
        title: autoTitle,
        description: autoDescription,
        eds_reference: context.edsReference || '',
        priority: context.priority || 'medium',
        category: context.category || 'data_issue'
      });

      // Auto-capture screenshot
      captureScreenshot();

      // Collect logs from backend
      collectLogs();
    }
  }, [isOpen, context]);

  const captureScreenshot = async () => {
    setIsCapturing(true);
    try {
      // Wait a bit for modal to render
      await new Promise(resolve => setTimeout(resolve, 100));

      // Capture the entire page (excluding the modal)
      const canvas = await html2canvas(document.body, {
        ignoreElements: (element) => {
          // Ignore the modal itself
          return element.classList?.contains('ticket-modal-overlay');
        },
        backgroundColor: '#1a1a1a',
        scale: 0.5, // Reduce quality for smaller file size
        logging: false
      });

      canvas.toBlob((blob) => {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const file = new File([blob], `screenshot-${timestamp}.png`, { type: 'image/png' });
        setScreenshot(file);
        setIsCapturing(false);
      }, 'image/png', 0.8);
    } catch (err) {
      console.error('Failed to capture screenshot:', err);
      setIsCapturing(false);
    }
  };

  const collectLogs = async () => {
    try {
      // Fetch recent logs from backend
      const response = await axios.get(`${API_BASE}/api/admin/logs`, {
        params: { limit: 100, level: 'INFO' }
      });

      if (response.data && response.data.logs) {
        const logText = response.data.logs.map(log =>
          `[${log.timestamp}] ${log.level}: ${log.message}`
        ).join('\n');
        setLogs(logText);
      }
    } catch (err) {
      console.error('Failed to collect logs:', err);
      // Don't fail the modal if logs can't be collected
      setLogs('(Log collection failed)');
    }
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setAttachments(prev => [...prev, ...files]);
  };

  const removeAttachment = (index) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  const removeScreenshot = () => {
    setScreenshot(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      // Create ticket first
      const ticketPayload = {
        device_type: context.deviceType || 'General',
        device_id: context.deviceId,
        device_name: context.deviceName,
        vendor_name: context.vendorName,
        product_code: context.productCode,
        ...formData
      };

      const ticketResponse = await axios.post(`${API_BASE}/api/tickets`, ticketPayload);
      const ticketId = ticketResponse.data.id;

      // Upload screenshot if available
      if (screenshot) {
        const screenshotFormData = new FormData();
        screenshotFormData.append('file', screenshot);
        await axios.post(`${API_BASE}/api/tickets/${ticketId}/attachments`, screenshotFormData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      // Upload logs as attachment if available
      if (logs) {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const logBlob = new Blob([logs], { type: 'text/plain' });
        const logFile = new File([logBlob], `logs-${timestamp}.txt`, { type: 'text/plain' });
        const logFormData = new FormData();
        logFormData.append('file', logFile);
        await axios.post(`${API_BASE}/api/tickets/${ticketId}/attachments`, logFormData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      // Upload all other attachments
      for (const file of attachments) {
        const formData = new FormData();
        formData.append('file', file);
        await axios.post(`${API_BASE}/api/tickets/${ticketId}/attachments`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      setSuccess(true);
      setTimeout(() => {
        onClose();
        setSuccess(false);
        resetForm();
      }, 1500);
    } catch (err) {
      console.error('Failed to create ticket:', err);
      setError(err.response?.data?.detail || 'Failed to create ticket');
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      description: '',
      eds_reference: '',
      priority: 'medium',
      category: 'data_issue'
    });
    setAttachments([]);
    setScreenshot(null);
    setLogs('');
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  if (!isOpen) return null;

  const getTotalAttachmentCount = () => {
    let count = attachments.length;
    if (screenshot) count++;
    if (logs) count++;
    return count;
  };

  return (
    <div className="ticket-modal-overlay fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-lg shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="border-b border-border p-6 flex items-center justify-between sticky top-0 bg-card z-10">
          <div>
            <h2 className="text-2xl font-semibold text-foreground">Report Issue</h2>
            <p className="text-sm text-muted-foreground mt-1">
              {context.deviceName || context.page || 'Create a bug report or feedback'}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Context Info */}
        {context.page && (
          <div className="px-6 py-4 bg-secondary/30 border-b border-border">
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Page:</span>
                <span className="ml-2 text-foreground font-medium">{context.page}</span>
              </div>
              {context.section && (
                <div>
                  <span className="text-muted-foreground">Section:</span>
                  <span className="ml-2 text-foreground font-medium">{context.section}</span>
                </div>
              )}
              {context.deviceType && (
                <div>
                  <span className="text-muted-foreground">Device Type:</span>
                  <span className="ml-2 text-foreground font-medium">{context.deviceType}</span>
                </div>
              )}
              {context.vendorName && (
                <div>
                  <span className="text-muted-foreground">Vendor:</span>
                  <span className="ml-2 text-foreground font-medium">{context.vendorName}</span>
                </div>
              )}
              {context.productCode && (
                <div>
                  <span className="text-muted-foreground">Product Code:</span>
                  <span className="ml-2 text-foreground font-medium">{context.productCode}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Attachments Summary */}
        {getTotalAttachmentCount() > 0 && (
          <div className="px-6 py-3 bg-accent/10 border-b border-border">
            <div className="flex items-center gap-2 text-sm text-accent">
              <CheckCircle2 className="w-4 h-4" />
              <span>
                {getTotalAttachmentCount()} attachment{getTotalAttachmentCount() > 1 ? 's' : ''} ready
                {screenshot && ' (including screenshot)'}
                {logs && ' (including logs)'}
              </span>
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Title <span className="text-error">*</span>
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
              placeholder="Auto-generated - you can edit"
            />
          </div>

          {/* Priority and Category */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                Priority
              </label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                Category
              </label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
              >
                <option value="bug">Bug</option>
                <option value="feature_request">Feature Request</option>
                <option value="data_issue">Data Issue</option>
                <option value="parser_bug">Parser Bug</option>
                <option value="ui_issue">UI Issue</option>
                <option value="performance">Performance</option>
                <option value="documentation">Documentation</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          {/* EDS/IODD Reference */}
          {(context.deviceType === 'EDS' || context.deviceType === 'IODD') && (
            <div>
              <label className="block text-sm font-medium text-foreground mb-2">
                {context.deviceType} Reference
              </label>
              <input
                type="text"
                value={formData.eds_reference}
                onChange={(e) => setFormData({ ...formData, eds_reference: e.target.value })}
                className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent"
                placeholder="e.g., Param2, Assem100, ME_Parameter"
              />
              <p className="text-xs text-muted-foreground mt-1">
                Reference to specific parameter, assembly, menu, or section
              </p>
            </div>
          )}

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Description <span className="text-error">*</span>
            </label>
            <textarea
              required
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={12}
              className="w-full px-4 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent resize-none font-mono text-sm"
              placeholder="Pre-filled with context - add your observations"
            />
          </div>

          {/* Attachments Section */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-foreground">
              Attachments
            </label>

            {/* Screenshot Preview */}
            {screenshot && (
              <div className="flex items-center gap-3 p-3 bg-secondary/50 border border-border rounded-lg">
                <Camera className="w-5 h-5 text-accent flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-foreground truncate">{screenshot.name}</div>
                  <div className="text-xs text-muted-foreground">{formatFileSize(screenshot.size)} (Auto-captured)</div>
                </div>
                <button
                  type="button"
                  onClick={removeScreenshot}
                  className="p-1 text-muted-foreground hover:text-error transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            )}

            {/* Logs Indicator */}
            {logs && (
              <div className="flex items-center gap-3 p-3 bg-secondary/50 border border-border rounded-lg">
                <FileText className="w-5 h-5 text-accent flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-foreground">System Logs</div>
                  <div className="text-xs text-muted-foreground">{formatFileSize(new Blob([logs]).size)} (Auto-collected)</div>
                </div>
              </div>
            )}

            {/* User Attachments */}
            {attachments.map((file, index) => (
              <div key={index} className="flex items-center gap-3 p-3 bg-secondary/50 border border-border rounded-lg">
                <Paperclip className="w-5 h-5 text-foreground flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-foreground truncate">{file.name}</div>
                  <div className="text-xs text-muted-foreground">{formatFileSize(file.size)}</div>
                </div>
                <button
                  type="button"
                  onClick={() => removeAttachment(index)}
                  className="p-1 text-muted-foreground hover:text-error transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}

            {/* Add Files Button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="w-full px-4 py-3 border-2 border-dashed border-border hover:border-accent rounded-lg text-muted-foreground hover:text-accent transition-colors flex items-center justify-center gap-2"
            >
              <Paperclip className="w-5 h-5" />
              <span>Add Files (any type, multiple allowed)</span>
            </button>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-error/20 border border-error/50 rounded-lg p-3 flex items-start gap-2">
              <AlertCircle className="w-5 h-5 text-error flex-shrink-0 mt-0.5" />
              <div className="text-sm text-error">{error}</div>
            </div>
          )}

          {/* Success Message */}
          {success && (
            <div className="bg-success/30 border border-success/50 rounded-lg p-3 flex items-start gap-2">
              <CheckCircle2 className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
              <div className="text-sm text-success">
                Ticket created successfully with {getTotalAttachmentCount()} attachment(s)!
              </div>
            </div>
          )}

          {/* Buttons */}
          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-6 py-2 border border-border text-foreground rounded-lg hover:bg-secondary transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || isCapturing || !formData.title || !formData.description}
              className="px-6 py-2 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isSubmitting ? 'Creating...' : isCapturing ? 'Capturing...' : 'Create Ticket'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EnhancedTicketModal;
