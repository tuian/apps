import csv
import json

def csvToJson( inFile, outFile ):
    out = None;

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

if __name__ == "__main__":

     # import argparse
     # parser = argparse.ArgumentParser()
     # parser.add_argument('inFile', nargs=1, help="Choose the in file to use")
     # parser.add_argument('outFile', nargs=1, help="Choose the out file to use")
     # args = parser.parse_args()
     # csvToJson( args.inFile[0] , args.outFile[0] );
    csvToJson( "C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.csv" , "C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.json");
    csvToJson("C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings.csv","C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Mappings.json");