import pandas as pd

# Loading a CSV file
#df = pd.read_csv('../data/example.csv')

# Loading a EXLS file
# xls_file = pd.ExcelFile('./data/LDM OBJ Report.xlsx')
# df = xls_file.parse('export0')
#
# print df

def generateLDMObjectReport():
    #Analysis:
    #LDM Objects are straight forward. Just extract the full contents from the report without much manipulation.
    # the column "Internal ID" is the important column that uniquely identifies the rows (pretty much)

    print "###############   LDM Object Report  ###################################\n"
    print "Please ensure you have deleted the first column from the Avaloq report\n"

    print "Confirm if you have deleted the first column in the Avaloq report ? [Yes/No]:"
    answer = raw_input()
    if(answer == 'Yes'):
        print "Generating CSV file, please wait.....\n"

        input_excel_filename = "LDM_OBJ_REPORT.xlsx"
        output_csv_filename =  "LDM_OBJ_REPORT_Output.csv"

        df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)
        #print df.head()

        #xls_file = pd.ExcelFile('./data/input/raw/LDM_OBJ_REPORT.xlsx')
        #df = xls_file.parse('export0',index_col="Field")

        #df.insert(1,'LDM Object New', "-")

        #print df.loc[0, 'LDM Object']

        # insert two new columns for LDM Object and LDM Field. Copy the value of Internal ID into these two columns
        df.insert(10,"Internal ID LDM Object",df["Internal ID"])
        df.insert(11,"Internal ID LDM Field" ,df["Internal ID"])

        ''' '''
        # Go through each row and make corrections to cell values
        for i in range(1, len(df)):
            #print df.loc[i,'LDM Object']

            #split the value by $ delimiter to get the LDM Object and LDM Field
            if ('$' in str(df.loc[i,"Internal ID"])):
                list_of_values = df.loc[i,"Internal ID"].split("$")
                df.loc[i,"Internal ID LDM Object"]  = list_of_values[0]
                df.loc[i,"Internal ID LDM Field"]  = list_of_values[1]

            else:
                #df.loc[i, "Internal ID LDM Object"] = df.loc[i,"Internal ID"]
                df.loc[i, "Internal ID LDM Object"] = ""
                df.loc[i, "Internal ID LDM Field"] = ""

            if(pd.isnull(df.loc[i,'LDM Object'])):
                #print "Inside None"
                df.loc[i, 'LDM Object'] = df.loc[i-1, 'LDM Object']

        # drop rows with Field as blank
        df = df.dropna(subset=['Field'])
        # drop rows with Field Type as blank
        df = df.dropna(subset=['Field Type'])

        #print df.head(10)


        df.to_csv("./data/output/"+output_csv_filename,sep=",",index=False,header=True)

        print "Program completed successfully."
        print "Check the output csv file in the folder: ", output_csv_filename

    else:
        print "Not generating CSV file.....\n"
        print "Re-Run the program after deleting the first column in Avaloq report.\n"
        print "Thank You !\n"


def generateLDMInterfaceReport():
    #Analysis / Notes:
    #
    # There are essentially two types of fields: Complex Fields and Simple Fields.
    # XSD Simple Fields are mapped  by the Internal ID to the LDM Simple Fields - Directly
    # For XSD Complex Fields, LDM Object Name is given in the LDM Field
    # Use LDM Text Type - to find if the mapping is to a simple field or complex object

    print "###############   LDM Interface Report  ###################################\n"
    print "Please ensure you have deleted the first column from the Avaloq report\n"

    print "Confirm if you have deleted the first column in the Avaloq report ? [Yes/No]:"
    answer = raw_input()
    if(answer.upper() == 'Yes'.upper()):
        print "Generating CSV file, please wait.....\n"

        input_excel_filename = "LDM_INTF_Report.xlsx"
        output_csv_filename  = "LDM_INTF_Report_Output.csv"

        df = pd.read_excel('./data/input/raw/'+input_excel_filename,sheetname="export0",index_col=None)


        #xls_file = pd.ExcelFile('./data/input/raw/LDM_OBJ_REPORT.xlsx')
        #df = xls_file.parse('export0',index_col="Field")


        #print df.loc[0, 'LDM Object']


        # insert two new columns
        df.insert(6, "LDM Text Type",df["LDM Text"])
        df.insert(7, "Internal ID"  ,df["LDM Text"])

        #print df.head()
        ''' '''
        # Go through each row and make corrections to cell values
        for i in range(1, len(df)):
            #print df.loc[i,'LDM Object']

            if (pd.isnull(df.loc[i, 'LDM Field'])):
                # print "Inside None"
                df.loc[i, 'LDM Field'] = df.loc[i, 'LDM Object']

            #split the value by $ delimiter to get the LDM Object and LDM Field
            if ("." in str(df.loc[i,"LDM Text"])):
                list_of_values = df.loc[i,"LDM Text"].split(".")
                df.loc[i,"LDM Text Type"]  = str(list_of_values[0]).replace("LDM:btfg$code_","")
                df.loc[i,"Internal ID"]    = list_of_values[1]

            else:
                #df.loc[i, "Internal ID LDM Object"] = df.loc[i,"Internal ID"]
                df.loc[i, "LDM Text Type"] = ""
                df.loc[i, "Internal ID"]   = ""

            if(pd.isnull(df.loc[i,'Interface Name'])):
                #print "Inside None"
                df.loc[i, 'Interface Name'] = df.loc[i-1, 'Interface Name']

            if (pd.isnull(df.loc[i, 'Source Name'])):
                # print "Inside None"
                df.loc[i, 'Source Name'] = df.loc[i - 1, 'Source Name']


        # drop rows if column "Element Name" is blank
        df = df.dropna(subset=['Element Name'])

        # drop rows if column "LDM Field" is blank
        # df = df.dropna(subset=['LDM Field']) # Do not drop the LDM Field if blank, rather copy the LDM Object column value

        #print df.head(10)


        df.to_csv("./data/output/"+output_csv_filename,sep=",",index=False,header=True)

        print "Program completed successfully."
        print "Check the output csv file in the folder: ", output_csv_filename

    else:
        print "Not generating CSV file.....\n"
        print "Re-Run the program after deleting the first column in Avaloq report.\n"
        print "Thank You !\n"




generateLDMObjectReport()
generateLDMInterfaceReport()
