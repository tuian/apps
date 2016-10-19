import pandas as pd
import time,csv,json,sys
folder = "C:/MDR/Data"
output_filename = ""

reload(sys)
sys.setdefaultencoding('utf8')

myList = ['a','b','c','d']
myString = ",".join(myList )

df = pd.read_excel(folder + 'MDR_LOADING.xlsx',sheetname="Mappings")

writer = pd.ExcelWriter(folder + output_filename)
df.to_excel(writer, sheet_name="Stats",index=False)

df = df[df["Status"].str.upper() == "Open".upper()]

if(df.empty): print "Dataframe is empty"

df_d = df[df.duplicated(subset=["Source Name", "Element Name"], keep='first')]

time.strftime('%Y-%m-%d %H:%M:%S')
df = df.drop('Modified_By', 1)
object_duplicated_by_columns = ["System Name","Entity Name", "Attribute Name","Type"]
object_sort_by_columns       = ["System Name", "Entity Name", "Attribute Name", "Type"]

df.drop_duplicates(subset=object_duplicated_by_columns, keep=False, inplace=True)
df.drop_duplicates(subset=object_duplicated_by_columns, keep='first', inplace=True)

df["Target Attribute Name"].replace('', np.nan)

df.rename(columns={"From":"To","LDM Text":"Attribute_Description"}, inplace=True)
df.rename(columns=lambda x: x.strip().replace(" ", "_"), inplace=True)

# strip or trim
df["Source_System_Name"] = df["Source_System_Name"].str.strip()

df.sort_values(by=object_sort_by_columns, inplace=True, na_position='first', ascending=[False, True, True, True])

#regex in dataframe cell
passRegex = r"^(?!.*\s)(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,50}$"
nameRegex = r"^[a-zA-Z0-9\s\-]{2,80}$"
df[(df['password'].str.contains(passRegex, regex=True)) & (df['first'].str.contains(nameRegex, regex=True)) & (df['last'].str.contains(nameRegex, regex=True))]


#ignore the rows with blank Entity Name
df = df[df["LDM Object"].notnull()]
df = df[df["Type"].isnull()]


# Read CSV
output_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
input_csv_folder_path = "C:\\MDR\\Data\\Repository\\CSV_Sharepoint_Output\\"
input_filename = ""
output_filename = "ABS_EntityName_T_E_A_Correct.csv"

required_columns = ["Entity Name", "Attribute Name"]

df = pd.read_csv(input_csv_folder_path + input_filename, sep=",",usecols=required_columns)
df.to_csv(output_csv_folder_path + "BTP_Phase1_2_Mappings.csv", sep=",")

df1,df2 = pd.DataFrame()

merged_df = pd.merge(left=df1,right=df2, on=["Entity Name","Attribute Name"],how='left')


def csvToJson( inFile, outFile ):
    out = None;

    with open( inFile, 'r') as csvFile:
        #Note this reads the first line as the keys we can add specific keys with:
        #csv.DictReader( csvFile, fieldnames=<LIST HERE>, restkey=None, restval=None, )
        csvDict = csv.DictReader( csvFile, restkey=None, restval=None, )
        out = [obj for obj in csvDict]

    if out:
        with open( outFile, 'w' ) as jsonFile:
            jsonFile.write( json.dumps( out ) );
    else:
       print "Error creating csv dict!"
