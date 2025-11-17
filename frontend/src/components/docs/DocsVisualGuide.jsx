import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Check, Info, AlertTriangle, Lightbulb } from 'lucide-react';
import { Button } from '../ui';

/**
 * DocsVisualGuide - Interactive Visual Guide Component
 *
 * Creates step-by-step visual guides with illustrations, tips, and warnings
 */

// GuideStep - Individual step in the visual guide
const GuideStep = ({ number, title, description, image, tip, warning, children }) => {
  return (
    <div className="flex gap-6 items-start">
      {/* Step Number */}
      <div className="flex-shrink-0">
        <div className="w-12 h-12 rounded-full bg-brand-green/10 border-2 border-brand-green flex items-center justify-center">
          <span className="text-xl font-bold text-brand-green">{number}</span>
        </div>
      </div>

      {/* Step Content */}
      <div className="flex-1 space-y-4">
        <div>
          <h4 className="text-lg font-semibold text-foreground mb-2">{title}</h4>
          {description && (
            <p className="text-muted-foreground">{description}</p>
          )}
        </div>

        {/* Visual/Image placeholder */}
        {image && (
          <div className="border-2 border-border rounded-lg overflow-hidden bg-surface/50">
            <img
              src={image}
              alt={title}
              className="w-full h-auto"
            />
          </div>
        )}

        {/* Code or custom content */}
        {children && (
          <div className="pl-4 border-l-4 border-brand-green/30">
            {children}
          </div>
        )}

        {/* Tip callout */}
        {tip && (
          <div className="flex gap-3 p-4 bg-brand-green/5 border border-brand-green/20 rounded-lg">
            <Lightbulb className="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">Tip</p>
              <p className="text-sm text-muted-foreground">{tip}</p>
            </div>
          </div>
        )}

        {/* Warning callout */}
        {warning && (
          <div className="flex gap-3 p-4 bg-warning/5 border border-warning/20 rounded-lg">
            <AlertTriangle className="w-5 h-5 text-warning flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-semibold text-foreground mb-1">Warning</p>
              <p className="text-sm text-muted-foreground">{warning}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// InteractiveGuide - Guide with step-by-step navigation
const InteractiveGuide = ({ title, description, steps, children }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const totalSteps = React.Children.count(children);

  const goToNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const goToPrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const stepsArray = React.Children.toArray(children);

  return (
    <div className="my-8 border border-border rounded-xl overflow-hidden">
      {/* Header */}
      <div className="bg-brand-green/5 border-b border-border p-6">
        <h3 className="text-xl font-bold text-foreground mb-2">{title}</h3>
        {description && (
          <p className="text-muted-foreground">{description}</p>
        )}

        {/* Progress bar */}
        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">
              Step {currentStep + 1} of {totalSteps}
            </span>
            <span className="text-sm font-medium text-brand-green">
              {Math.round(((currentStep + 1) / totalSteps) * 100)}% Complete
            </span>
          </div>
          <div className="h-2 bg-surface rounded-full overflow-hidden">
            <div
              className="h-full bg-brand-green transition-all duration-300 ease-out"
              style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
            />
          </div>
        </div>

        {/* Step indicators */}
        <div className="flex items-center gap-2 mt-4 flex-wrap">
          {stepsArray.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentStep(index)}
              className={`
                w-8 h-8 rounded-full flex items-center justify-center
                transition-all duration-200
                ${index === currentStep
                  ? 'bg-brand-green text-white'
                  : index < currentStep
                    ? 'bg-brand-green/30 text-brand-green'
                    : 'bg-surface text-muted-foreground hover:bg-surface-hover'
                }
              `}
            >
              {index < currentStep ? (
                <Check className="w-4 h-4" />
              ) : (
                <span className="text-xs font-medium">{index + 1}</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Current Step Content */}
      <div className="p-6">
        {stepsArray[currentStep]}
      </div>

      {/* Navigation Footer */}
      <div className="border-t border-border p-4 flex items-center justify-between bg-surface/50">
        <Button
          variant="outline"
          onClick={goToPrevious}
          disabled={currentStep === 0}
          className="flex items-center gap-2"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </Button>

        <Button
          onClick={goToNext}
          disabled={currentStep === totalSteps - 1}
          className="flex items-center gap-2"
        >
          {currentStep === totalSteps - 1 ? 'Finish' : 'Next'}
          <ChevronRight className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
};

// StaticGuide - Non-interactive guide showing all steps
const StaticGuide = ({ title, description, children }) => {
  return (
    <div className="my-8 space-y-8">
      {(title || description) && (
        <div className="text-center pb-4 border-b border-border">
          {title && (
            <h3 className="text-xl font-bold text-foreground mb-2">{title}</h3>
          )}
          {description && (
            <p className="text-muted-foreground">{description}</p>
          )}
        </div>
      )}
      <div className="space-y-8">
        {React.Children.map(children, (child, index) =>
          React.cloneElement(child, { number: index + 1 })
        )}
      </div>
    </div>
  );
};

// Export components
export default {
  Interactive: InteractiveGuide,
  Static: StaticGuide,
  Step: GuideStep,
};

export { InteractiveGuide, StaticGuide, GuideStep };
