# Metadata Miner - An automated data mining framework to mine metadata from source code (Html files), design documents (interface specification word / excel documents) and database table schema definitions.
Data lineage and tracability from ‘what is shown on the user screens’ to the actual ‘source of truth’

## Data Sourcing & Extraction
* Ability to connect to SharePoint, Github repository, Source Databases
* Extract metadata from unstructured sources like PDFs, Word Documents
* Delta extraction based on document last modified date, Github source code versions.

## Data Cleansing & de-duplication & Transformation
* Cleanse and reformat data fields based on the transformation rules and requirements 
* Remove duplication
* Check for data quality and correctness

## Data Loading and reconciliation
* Generate metadata load files (delta load files using batch control parameters). 
* Format / transform metadata load files accordingly defined templates.
* Run data analysis reports and checks – to test and ensure the load files are correct, before sending to EIM team
* Reconcile and confirm data load to target repository

