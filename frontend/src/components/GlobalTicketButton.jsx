import React, { useState, useEffect } from 'react';
import { Bug, MessageSquarePlus } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import EnhancedTicketModal from './EnhancedTicketModal';

/**
 * Global floating action button for creating tickets from any page
 * Automatically captures context from the current page/route
 */
const GlobalTicketButton = ({ API_BASE = '' }) => {
  const location = useLocation();
  const [showModal, setShowModal] = useState(false);
  const [context, setContext] = useState({});

  // Extract context from current page whenever location changes
  useEffect(() => {
    const extractContext = () => {
      const path = location.pathname;
      const searchParams = new URLSearchParams(location.search);

      let pageContext = {
        page: 'Unknown',
        section: '',
        url: window.location.href,
        timestamp: new Date().toISOString()
      };

      // Detect page from URL
      if (path === '/' || path === '/home') {
        pageContext.page = 'Home';
      } else if (path.startsWith('/eds')) {
        pageContext.page = 'EDS Devices';
        pageContext.deviceType = 'EDS';

        // Check if we're on a device detail page
        const deviceMatch = location.state;
        if (deviceMatch) {
          pageContext.deviceId = deviceMatch.id;
          pageContext.deviceName = deviceMatch.product_name || deviceMatch.name;
          pageContext.vendorName = deviceMatch.vendor_name;
          pageContext.productCode = deviceMatch.product_code;
        }

        // Detect active tab from hash
        if (location.hash) {
          pageContext.activeTab = location.hash.replace('#', '');
        }
      } else if (path.startsWith('/iodd')) {
        pageContext.page = 'IODD Devices';
        pageContext.deviceType = 'IODD';

        // Check for device details
        const deviceMatch = location.state;
        if (deviceMatch) {
          pageContext.deviceId = deviceMatch.id;
          pageContext.deviceName = deviceMatch.product_name || deviceMatch.name;
          pageContext.vendorName = deviceMatch.vendor_name;
          pageContext.productCode = deviceMatch.product_code;
        }
      } else if (path.startsWith('/pqa')) {
        pageContext.page = 'PQA Console';
        pageContext.section = 'Parameter Query';
      } else if (path.startsWith('/admin')) {
        pageContext.page = 'Admin Console';
      } else if (path.startsWith('/tickets')) {
        pageContext.page = 'Tickets';
      } else if (path.startsWith('/docs')) {
        pageContext.page = 'Documentation';
        // Extract doc section from path
        const parts = path.split('/').filter(Boolean);
        if (parts.length > 1) {
          pageContext.section = parts.slice(1).map(p =>
            p.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
          ).join(' / ');
        }
      }

      return pageContext;
    };

    setContext(extractContext());
  }, [location]);

  const handleOpenModal = () => {
    // Refresh context right before opening
    const freshContext = {
      ...context,
      timestamp: new Date().toISOString()
    };
    setContext(freshContext);
    setShowModal(true);
  };

  return (
    <>
      <button
        onClick={handleOpenModal}
        className="fixed bottom-6 right-6 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white rounded-full px-6 py-4 shadow-lg hover:shadow-xl transition-all transform hover:scale-105 flex items-center gap-2 z-40 group"
        title="Report an issue or provide feedback"
        aria-label="Report Issue"
      >
        <Bug className="w-5 h-5" />
        <span className="font-medium">Report Issue</span>
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
      </button>

      <EnhancedTicketModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        context={context}
        API_BASE={API_BASE}
      />
    </>
  );
};

export default GlobalTicketButton;
