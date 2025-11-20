*******************************************************************************
***                                                                         ***
***             IODD IO Device Description Specification V1.1.4             ***
***                                                                         ***
*******************************************************************************

This package contains

- Schemas\
	- IODD1.1.xsd
	- IODD-Communication1.1.xsd
	- IODD-Datatypes1.1.xsd
	- IODD-Events1.1.xsd
	- IODD-Primitives1.1.xsd
	- IODD-StandardDefinitions1.1.xsd
	- IODD-UserInterface1.1.xsd
	- IODD-Variables1.1.xsd
	- IODD-WirelessCommunication1.1.xsd
	- IOL-ProfileDefinition1.1.xsd
	- xml.xsd

- Specification\
	- IO-Device-Desc-Spec_10012_V1.1.4_Jun24.pdf

- StandardDefinitions\
	- IODD-StandardDefinitions1.1.xml
	- IODD-StandardDefinitions1.1-de.xml
	- IODD-StandardDefinitions1.1-es.xml
	- IODD-StandardDefinitions1.1-fr.xml
	- IODD-StandardDefinitions1.1-it.xml
	- IODD-StandardDefinitions1.1-ja.xml
	- IODD-StandardDefinitions1.1-ko.xml
	- IODD-StandardDefinitions1.1-pt.xml
	- IODD-StandardDefinitions1.1-ru.xml
	- IODD-StandardDefinitions1.1-zh.xml
	- IODD-StandardUnitDefinitions1.1.xml

- StandardDefinitions_1.0.1_for_compatibility\
	- IODD-StandardDefinitions1.0.1.xml
	- IODD-StandardDefinitions1.0.1-de.xml
	- IODD-StandardDefinitions1.0.1-fr.xml
	- IODD-StandardUnitDefinitions1.0.1.xml

- Templates\
	- IODD-SystemCommandDefinitions_V114.xml
	- Tool-MenuUserRole_X114.xml

For validity periods, see document "Specification Validity Periods" on
	https://io-link.com/downloads

Please provide any issue as a change request at www.io-link-projects.com by providing name and email address with
	login:    IO-Link-DD
	password: Report

Your participation ensures the success of this community, thank you

	The IO-Link IODD team


Change log:
_______________________________________________________________________________________________________________
IO-Device-Desc-Spec_10012_V114_Jun24_Update202507.zip
- CR45 IODD-StandardUnitDefinitions1.0.1.xml: Define new unit codes for turbidity / Trübung (1713..1718)
- CR49 IODD-StandardUnitDefinitions1.0.1.xml: Add new units to StandardUnitDefinition (1719)

_______________________________________________________________________________________________________________
IO-Device-Desc-Spec_10012_V114_Jun24_Update202502.zip
- Update IOL-ProfileDefinition1.1.xsd (RecordItemInfoT)

_______________________________________________________________________________________________________________
IO-Device-Desc-Spec_10012_V114_Jun24.zip
- CR01 Clarify subindexAccessSupported default value
- CR03 Syntax for additionalDeviceIDs unclear
- CR04 Improve description of button behaviour
- CR05 Increase maximum number of menus in menu collection
- CR07 Usage of ProcessDataRef for VariableRef V_ProcessDataInput/V_ProcessDataOutput
- CR13 Writeable variable of type RecordT without subindex access must be writeable completely in each user role
- CR16 A few details in the 1.1.3 version seem screwed up
- CR17 A sentence that looks incomplete
- CR21 Condition variable for ProcessData: All allowed values must have a corresponding ProcessData
- CR25 missing plural 's' in english Command descriptions
- CR26 Adding new units to the StandardUnitDefinition
- CR32 New physical unit r/s^2
- CR34 Add snippet rules to IODD specification
- CR36 New strict rules for tools
- CR37 referencing old specification

_______________________________________________________________________________________________________________
2022-03-30
- CR20 Integrate updated Wireless Schema
- CR18 StandardDefinitions\IODD-StandardDefinitions1.1-ko.xml
       --> correct content //Text[@id='STD_TN_0x5111']/@value
- CR19 StandardDefinitions\IODD-StandardUnitDefinitions1.1.xml
       StandardDefinitions 1.0.1 for compatibility\IODD-StandardUnitDefinitions1.0.1.xml
       --> add //Unit[@code'1702'] mm/s²

_______________________________________________________________________________________________________________
2021-03-24 
- Release IODD specification package 2020