import csv
import json
import pandas as pd

def csvToJson( inFile, outFile ):
    out = None;

    print "procesing csv to json {}".format(inFile)

    removeSpaceInColumnNames(inFile)

    with open( inFile, 'r') as csvFile:
        #Note this reads the first line as the keys we can add specific keys with:
        #csv.DictReader( csvFile, fieldnames=<LIST HERE>, restkey=None, restval=None, )

        csvDict = csv.DictReader( csvFile, restkey=None, restval=None, )

        #list , build it from csvDict object of objects. this list will have list of objects (each object is a dictionary)
        out = [obj for obj in csvDict]

    if out:
        with open( outFile, 'w' ) as jsonFile:
            jsonFile.write( json.dumps( out ) );
    else:
       print "Error creating csv dict!"

def removeSpaceInColumnNames(inFile):
    print "convering spaces to _ in the column names"
    #read the file as dataframe

    df = pd.read_csv(inFile, sep=",")

    #update the column names to remove the spaces
    #df.rename(columns=lambda x: x.replace(" ", "_"), inplace=True)
    df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)

    #write the file as dataframe
    df.to_csv(inFile, sep=",")

def processCSV_JSON():
    csvToJson("C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.csv",
              "C:/apps/apps/metadata/static/json/BTP_Phase1_2_Objects.json");
    csvToJson("C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings.csv",
              "C:/apps/apps/metadata/static/json/BTP_Phase1_2_Mappings.json");
    csvToJson("C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings_df_ux_vm_ifs_xsd_by_join.csv",
              "C:/apps/apps/metadata/static/json/BTP_Phase1_2_Mappings_df_ux_vm_ifs_xsd_by_join.json");


if __name__ == "__main__":

     # import argparse
     # parser = argparse.ArgumentParser()
     # parser.add_argument('inFile', nargs=1, help="Choose the in file to use")
     # parser.add_argument('outFile', nargs=1, help="Choose the out file to use")
     # args = parser.parse_args()
     # csvToJson( args.inFile[0] , args.outFile[0] );
    # removeSpaceInColumnNames("C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.csv")
    # removeSpaceInColumnNames("C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings.csv")

    processCSV_JSON()
    print "\n Process completed successfull :)"
