Dear fellow IO-Link Device designer,

this package contains 

- IOL-Common_Profile_V1.2_Jan2024.pdf
	Specification

- IODD-CP-Snippets_V1.2.1.xml
	xml based snippets to be used in any device IODD and base for IODD Checker business rules

Please read the change log at the bottom very careful to get an overview of the changed aspects

Please provide any issue as a change request at www.io-link-projects.com with 
- your personal account 
- or by providing name and email address with the 
	login: IOL-SM-Profile 
	password: Report
 

Your participation ensures the success of this community, thank you

	The core team as host of the Common Profile

Change log:
_______________________________________________________________________________________________________________
IO-Link Common Profile V1.2:

# the CommonProfile V1.1 will be discontinued, please see separate schedule information on io-link.com

# new FunctionClass TeachRecommended
# optimized description of dependency between Device Status and Events
# optimized Locator state machine to reduce uncertainties in interpretation 
# further editorial enhancements


_______________________________________________________________________________________________________________
IO-Link Common Profile V1.1:

# the CommonProfile V1.0 will be discontinued, please see separate schedule information on io-link.com

# all aspects regarding creation of profile specifications are removed to a separate internal document
-- Only the Device designer aspects are maintained
-- more detailed design rules for Device designer according profile usage

# definition of Extension FunctionClasses to reduce the amount of specified types
-- Extension FunctionClasses cannot act on its own, only in combination with a full profile
-- Extension FunctionClasses can be added and provide additional functionality of the profile behavior

# added Extension FunctionClasses
-- Locator to identify specific Devices
-- ProductURI according upcoming IEC61406

# enhanced and more precise rules on parameter design like
-- ProfileCharacteristic
-- PVInD, PVOutD
-- Interconnection between Diagnosis parameters

# strict menu definition of profiled parameters 
-- including naming, IODD representation, and appearance in the IODD
-- xml snippets added to
   - act as test input for the extended IODD checker
   - to be used as template for IODD generation
-- see also the current version on project server

# test cases added to extend the conformance check of profiled Devices

# for further details, see the file containing the handled change requests
-- available on IO-Link-projects.com

