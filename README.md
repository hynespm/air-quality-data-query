## Description: Codebase to ingest data to an RDS database and then visualise it

### Author: Patrick Hynes

Repository Structure

 * [README.md](README.md)
 * [data-set](data-set)
 * [function](function.py)
 * [app](app) - Express app to display queried data 
 * [database.template](database.template) - Database template
 * [database-parameters.json](database-parameters.json) - Database template parameters

### Dataset - http://archive.ics.uci.edu/ml/datasets/air+quality

The dataset contains 9358 instances of hourly averaged responses from an array of 5 metal oxide chemical sensors embedded in an Air Quality Chemical Multisensor Device. The device was located on the field in a significantly polluted area, at road level,within an Italian city. Data were recorded from March 2004 to February 2005 (one year)representing the longest freely available recordings of on field deployed air quality chemical sensor devices responses. Ground Truth hourly averaged concentrations for CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx) and Nitrogen Dioxide (NO2) and were provided by a co-located reference certified analyzer. Evidences of cross-sensitivities as well as both concept and sensor drifts are present as described in De Vito et al., Sens. And Act. B, Vol. 129,2,2008 (citation required) eventually affecting sensors concentration estimation capabilities. Missing values are tagged with -200 value.
This dataset can be used exclusively for research purposes. Commercial purposes are fully excluded.


### Data Attribute Information:

* 0 Date (DD/MM/YYYY)
* 1 Time (HH.MM.SS)
* 2 True hourly averaged concentration CO in mg/m^3 (reference analyzer)
* 3 PT08.S1 (tin oxide) hourly averaged sensor response (nominally CO targeted)
* 4 True hourly averaged overall Non Metanic HydroCarbons concentration in microg/m^3 (reference analyzer)
* 5 True hourly averaged Benzene concentration in microg/m^3 (reference analyzer)
* 6 PT08.S2 (titania) hourly averaged sensor response (nominally NMHC targeted)
* 7 True hourly averaged NOx concentration in ppb (reference analyzer)
* 8 PT08.S3 (tungsten oxide) hourly averaged sensor response (nominally NOx targeted)
* 9 True hourly averaged NO2 concentration in microg/m^3 (reference analyzer)
* 10 PT08.S4 (tungsten oxide) hourly averaged sensor response (nominally NO2 targeted)
* 11 PT08.S5 (indium oxide) hourly averaged sensor response (nominally O3 targeted)
* 12 Temperature in Â°C
* 13 Relative Humidity (%)
* 14 AH Absolute Humidity


## Process

These are the steps execute by this script

1. Create an RDS MySQL instances in AWS
2. Parse the dataset and insert into the database
3. Create an express app locally on port 8080 


### Web application

The express application exposes three endpoints for the following queries

* /query_1 : Select the days with at least 1-hour NO2 average concentration greater than the [EU Air Quality Standard](http://ec.europa.eu/environment/air/quality/standards.htm) for NO2
* /query_2 : Show total number of days matching the query requirements
* /query_3 : Show also the full record for each day matching the query requirements


### Requirements

1. Sufficient permissions to interact with an AWS account of your choice
2. Port 8080 to be open for traffic depending on where you deploy
