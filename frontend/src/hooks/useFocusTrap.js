import { useRef, useEffect } from 'react';
import { createFocusTrap } from 'focus-trap';

/**
 * Custom hook for focus trap functionality
 * Traps focus within a modal or dialog to improve accessibility
 *
 * @param {boolean} active - Whether the focus trap should be active
 * @param {Object} options - Focus trap configuration options
 * @returns {Object} - Ref to attach to the container element
 *
 * @example
 * function Modal({ isOpen, onClose }) {
 *   const modalRef = useFocusTrap(isOpen, {
 *     onDeactivate: onClose
 *   });
 *
 *   return (
 *     <div ref={modalRef} role="dialog" aria-modal="true">
 *       <h2>Modal Title</h2>
 *       <button onClick={onClose}>Close</button>
 *     </div>
 *   );
 * }
 */
export function useFocusTrap(active, options = {}) {
  const ref = useRef(null);
  const trapRef = useRef(null);

  useEffect(() => {
    if (!ref.current || !active) {
      // Deactivate trap if it exists but shouldn't be active
      if (trapRef.current && !active) {
        trapRef.current.deactivate();
        trapRef.current = null;
      }
      return;
    }

    // Create and activate focus trap
    try {
      trapRef.current = createFocusTrap(ref.current, {
        escapeDeactivates: true,
        returnFocusOnDeactivate: true,
        allowOutsideClick: true,
        initialFocus: false, // Let the modal determine initial focus
        ...options,
      });

      trapRef.current.activate();
    } catch (error) {
      console.error('Failed to activate focus trap:', error);
    }

    // Cleanup: deactivate trap when component unmounts or active changes
    return () => {
      if (trapRef.current) {
        try {
          trapRef.current.deactivate();
        } catch (error) {
          console.error('Failed to deactivate focus trap:', error);
        }
        trapRef.current = null;
      }
    };
  }, [active, options]);

  return ref;
}

export default useFocusTrap;
