This README file was generated on 2026-06-25 by Valentine Grange. 
Last updated: 2026-06-25
 
# GENERAL INFORMATION
 ## Dataset title: Annual operational data for the 10 MWe Ello Fresnel concentrated solar power plant
 
## DOI: 
 
## Contact email: sylvain.rodat@promes.cnrs.fr 

# METHODOLOGICAL INFORMATION 
 ## Environmental/experimental conditions: Operational data under normal operating conditions
 
## Description of sources and methods used to collect and generate data:
The dataset was collected from the 10 MWe eLLO Concentrated Solar Power (CSP) plant, a commercial-scale Linear Fresnel Reflector (LFR) facility using Direct Steam Generation (DSG) and steam storage, located in Llo, France. Data sources consist of 124 sensors distributed across the plant, covering seven operational categories: meteorological data, solar field data (east and west), turbine and aero-condenser data, condensate and feedwater data, electricity production data, and storage system data.
 Data were acquired using the plant’s proprietary supervisory control and data acquisition (SCADA) system, which recorded real-time measurements. Two distinct timeframes were considered:
* A 24-hour high-resolution snapshot (July 16–17, 2025) with a 10-second sampling interval, capturing a full operational cycle, including daytime production and overnight storage dispatch.
* A year-long dataset (January 1, 2025–January 1, 2026) with hourly aggregated values, flagging erroneous or missing data as NaN (resulting in 338 usable days for 2025). 
The dataset adheres to the Central European Time (CET/CEST) convention, with the following seasonal adjustments:
* UTC+01:00 (CET) from January 1 to March 28 and from October 25 to December 31,
* UTC+02:00 (CEST) from March 29 to October 24.

## Methods for processing the data: 
Erroneous sensor measurements were systematically replaced with NaN to ensure data consistency.
Additionally, flow rate measurements were manually corrected based on valve positions (these adjustments are not included in the provided dataset): whenever the corresponding valve position was zero or negative, the flow rate was set to zero.
The following flow rates were adjusted according to this principle:
* West-field tank purge flow rate [t/h]
* East-field tank purge flow rate [t/h]
* Steam flow rate at turbine 1 inlet downstream of superheater [t/h]
* Steam bypass flow rate from turbine to aero-condenser [t/h]
* Condensate flow rate from feedwater heater to deaerator [t/h]
* Demineralized water flow rate to deaerator [t/h]
* Feedwater flow rate to storage tanks [t/h]
* Steam injection flow rate to storage [t/h]
* Steam pressurization flow rate to storage [t/h]
* Storage water flow rate to West-field recirculation [t/h]
The following flow rates were further adjusted based on both the main valve position and bypass valve position:
* West-field feedwater flow rate [t/h]
* East-field feedwater flow rate [t/h]
* Steam flow rate from HP collector to superheater [t/h]
* Feedwater flow rate to East Field [t/h]
* Feedwater flow rate to West Field [t/h]
 
# DATA & FILE OVERVIEW
## File naming convention:
 
## File hierarchy convention: 
 The dataset is structured into three sheets across both Excel (.xlsx) and CSV (.csv) formats. « Description » provides a comprehensive inventory of all variables, including their unique identifier numbers (as referenced in the plant schematics), detailed descriptions, and units of measurement. « 24-hour period » contains high-resolution operational data for all variables over a 24-hour snapshot (July 16–17, 2025, 10-second intervals), while « Year 2025 » includes hourly aggregated data for the entire year (January 1, 2025–January 1, 2026). Additionally, annotated plant schematics are provided, illustrating the sensor locations across the three main zones: “solar field”, “storage system”, and “power block”. These schematics serve as a visual reference to contextualize the spatial distribution of measurements within the facility.
 # DATA-SPECIFIC INFORMATION 
 Decimal separator: point
## Variable List:
* Time (DD/MM/YYYY HH: MM: SS)
* GHI = Global Horizontal Irradiance (output L11) 	[W/m²]	
* East-field DNI = Direct Normal Irradiance (Aero-condenser) [W/m²]	
* West-field DNI = Direct Normal Irradiance (output L11) 	[W/m²]	
* West-field DNI 2= Direct Normal Irradiance (input L27) 	[W/m²]	
* External Temperature [°C]	
* External Temperature, West-field low [°C]	
* External Temperature, West separator tank [°C]	
* External Temperature, East-field low [°C]	
* External Temperature, ACC zone[°C]	
* External Temperature, between ACC 1&2	[°C]	
* External Temperature, between ACC 2&3 	[°C]	
* Wind Speed at 1 m height 	[km/h]	
* Wind Direction at 1 m height [°]	
* Wind Speed at 10 m height 	[km/h]	
* Wind Direction at 10 m height [°]	
* Atmospheric pressure in the turbine hall 	[mbarA]	
* Number of heliostats focusing, West Field	
* West-field separator tank pressure [barg]	
* West-field separator tank level [mm]	
* West-field feedwater flow rate [t/h]	
* West-field steam flow rate at tank outlet 	[t/h]	
* West-field tank steam dome temperature [°C]	
* West-field recirculation flow rate at pump discharge [t/h]	
* West-field recirculation pump discharge water temperature [°C]	
* West-field recirculation pump 1 discharge pressure [barg]	
* West-field recirculation pump 2 discharge pressure [barg]	
* West-field common outlet temperature (lines 11 to 27) 	[°C]	
* West-field tank purge flow rate [t/h]
* Number of heliostats focusing, East Field
* East-field separator tank pressure [barg]	
* East-field separator tank level [mm]	
* East-field feedwater flow rate [t/h]	
* East-field steam flow rate at tank outlet 	[t/h]	
* East-field tank steam dome temperature 	[°C]	
* East-field recirculation flow rate at pump discharge [t/h]	
* East-field recirculation pump discharge water temperature [°C]	
* East-field recirculation pump discharge pressure [barg]	
* East-field common outlet temperature (lines 1 to 3) [°C]	
* East-field common outlet temperature (lines 4 to 10) [°C]	
* East-field tank purge flow rate [t/h]	
* HP collector pressure [barg]
* HP collector calculated saturation temperature 	[°C]
* HP collector measured temperature [°C]	
* Steam flow rate to turbine [t/h]	
* Steam pressure to turbine upstream of superheater after expansion 	[barg]	
* Steam temperature to turbine upstream of superheater after expansion [°C]
* Steam pressure at turbine 1 inlet downstream of superheater 	[barg]	
* Steam temperature at turbine 1 inlet downstream of superheater [°C]
* Steam flow rate at turbine 1 inlet downstream of superheater 	[t/h]	
* Steam flow rate from HP collector to superheater [t/h]	
* Steam bypass flow rate from turbine to aero-condenser [t/h]	
* R1 extraction pressure [barg]	
* R1 extraction temperature [°C]	
* R1 extraction flow rate [t/h]	
* Steam pressure to turbine upstream of resuperheater [barg]	
* Steam temperature to turbine upstream of resuperheater [°C] 
* Steam pressure at turbine 2 inlet downstream of resuperheater [barg]	
* Steam temperature at turbine 2 inlet downstream of resuperheater 	[°C]
* Steam flow rate at turbine 2 inlet downstream of reheater [t/h]	
* Steam flow rate from HP collector to reheater [t/h]	
* Superheater and reheater flash tank pressure [barg]
* Superheater and reheater flash tank level [mm]	
* R1 extraction steam pressure to feedwater heater [barg]	
* R1 extraction steam temperature to feedwater heater 	[°C]	
* Condensate flow rate from feedwater heater to deaerator[t/h]
* R2 extraction pressure [barg]	
* R2 extraction temperature 	[°C]	
* R2 extraction flow rate to deaerator[t/h]
* R2 extraction steam pressure to deaerator[barg]	
* R2 extraction steam temperature to deaerator [°C]	
* R3 extraction temperature to condensate heater [°C]	
* R3 extraction flow rate to condensate heater [t/h]	
* Condensate temperature from condensate heater [°C]	
* Turbine exhaust pressure 	[barA]	
* Turbine exhaust steam temperature [°C]	
* Steam flow rate at turbine outlet [t/h]	
* Steam temperature at aero-condenser inlet [°C]	
* Condensate temperature at aero-condenser 1 outlet [°C]	
* Condensate temperature at aero-condenser 2 outlet [°C]	
* Condensate tank level [mm]	
* Condensate tank water temperature [°C]	
* Condensate pump discharge pressure [barg]	
* Condensate temperature at pump discharge[°C]	
* Condensate temperature downstream of turbine steam condenser [°C]	
* Condensate temperature downstream of deaerator steam condenser [°C]
* Condensate temperature downstream of condensate heater [°C]
* Condensate flow rate to deaerator [t/h]	
* Demineralized water flow rate to deaerator [t/h]	
* Deaerator level [mm]	
* Deaerator water temperature [°C]	
* Deaerator pressure	[barg]	
* Feedwater pump discharge pressure [barg]	
* Total feedwater flow rate [t/h]	
* Feedwater temperature downstream of feedwater heater [°C]	
* Feedwater flow rate to East Field	[t/h]	
* Feedwater flow rate to West Field	[t/h]
* Feedwater flow rate to storage tank [t/h]	
* Electrical power output from generator [MW]	
* Electrical power at export meter 	[MW]	
* Total active electrical power at delivery substation [kW]	
* Steam injection flow rate to storage [t/h]	
* Steam storage discharge flow rate	[t/h]	
* Steam pressurization flow rate to storage [t/h]	
* Storage pump 1 suction water temperature [°C]
* Storage pump 2 suction water temperature [°C]	
* Storage water flow rate to West-field recirculation [t/h]	
* Storage steam tank 1 pressure [barg]	
* Storage steam tank 1 level 	[mm]	
* Storage steam tank 2 pressure [barg]	
* Storage steam tank 2 level 	[mm]	
* Storage steam tank 3 pressure [barg]	
* Storage steam tank 3 level 	[mm]	
* Storage steam tank 4 pressure [barg]	
* Storage steam tank 4 level 	[mm]	
* Storage steam tank 5 pressure [barg]	
* Storage steam tank 5 level 	[mm]	
* Storage steam tank 6 pressure [barg]	
* Storage steam tank 6 level 	[mm]	
* Storage steam tank 7 pressure [barg]	
* Storage steam tank 7 level 	[mm]	
* Storage steam tank 8 pressure [barg]	
* Storage steam tank 8 level 	[mm]	
* Storage steam tank 9 pressure [barg]	
* Storage steam tank 9 level 	[mm]	

## Missing data codes: Erroneous sensor measurements were replaced with NaN.
 
## Additional information: 
A few key points should be noted regarding the measurements:
* Wind direction is defined such that 0° corresponds to a wind blowing from south to north, and 90° to a wind blowing from west to east.
* For tank level measurements, the 0 mm reference is set at the center of the tank, which explains why negative values may occur when the water level falls below this midpoint.
* The sensors in the solar fields are positioned along specific solar lines, which are numbered as follows: the East Solar Field includes 10 lines (L1 to L10), while the West Solar Field comprises 17 lines (L11 to L27).
