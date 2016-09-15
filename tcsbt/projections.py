from __future__ import division
from util import *
import pandas as pd



def setKeyValues(key,value):
    object = {}
    object["Key"] = key
    object["Value"] = value
    return object

def getActiveResourceCount(data_frame,month,key):

    data_frame = data_frame[data_frame["Resource_Name"] <> ""]

    object = {}
    object["Key"] = key
    object["Value"] = len(data_frame)

    return object

def getValueByKey(key, list):
    for item in list:

        if (item["Key"] == key): val = item["Value"]

    return val

def getProjectionDataFromSharepoint():

    rows = getSharepointListRowsByListName(GV_SHAREPOINT_LIST_NAME)

    data = []

    for row in rows:
        row_object = {}

        row_object["WON"] = str(row.Non_x002d_MSA_x0020_Role_x0020__)
        row_object["Resource_Name"] = row.Supplier_x0020_Resource_x0020_Na
        row_object["Role"] = row.Role
        row_object["Portfolio_Manager"] = row.Portfolio_x0020_Manager
        row_object["Location"] = row.Location

        # if(row.Sep_x0020_Business_x0020_Days <> ""):
        #     row_object["Sep_Business_Days"] = row.Sep_x0020_Business_x0020_Days
        # else:
        #     row_object["Sep_Business_Days"] = 0
        row_object["Sep_Business_Days"] = row.Sep_x0020_Business_x0020_Days
        row_object["Sep_Leave"] = row.Sep_x0020_Leave
        row_object["Sep_Billable_Days"] = row.Sep_x0020_Billable_x0020_Days
        row_object["Sep_Cost"] = row.Sep_x0020_Cost

        data.append(row_object)

    return data

def processProjections():

    required_columns_sharepoint = ["WON", "Resource_Name", "Role", "Portfolio_Manager", "Location","Sep_Business_Days", "Sep_Leave", "Sep_Billable_Days", "Sep_Cost"]
    required_columns_projection = ["WON","Resource_Name","Team_Name","Role","Portfolio_Manager","Location","Sep_Business_Days","Sep_Leave","Sep_Billable_Days","Sep_Cost"]
    required_columns_stats = ["Key","Value"]

    df_sharepoint = pd.DataFrame(getProjectionDataFromSharepoint(),columns=required_columns_sharepoint)
    df_sharepoint["WON"] = df_sharepoint["WON"].astype(str)
    df_sharepoint = df_sharepoint[df_sharepoint["Portfolio_Manager"] == "Shan"]
    df_sharepoint = df_sharepoint[df_sharepoint["Sep_Business_Days"] > 0]
    df_sharepoint.sort_values(by=["WON","Resource_Name"], inplace=True)

    print df_sharepoint

    df_resource_team = pd.read_excel(io=GV_INPUT_FOLDER+GV_INPUT_FILE,sheetname="Resource_Team")

    df_resource_team["WON"] = df_resource_team["WON"].astype(str)

    df_resource_team.sort_values(by=["WON","Resource_Name"], inplace=True)
    print df_resource_team

    df = pd.merge(left=df_sharepoint,right=df_resource_team,left_on=["WON","Resource_Name"],right_on=["WON","Resource_Name"],how='left')

    print "MERGED=",df.head()

    #apply all the filters

    #df.dropna(subset=["Resource_Name"],inplace=True)
    # df = df[df["Portfolio_Manager"] == "Shan"]
    # df = df[df["Sep_Business_Days"] > 0]
    # df.sort_values(by=["WON"],inplace=True)

    # split by Location, apply some function or analysis, combine into a DF or Series
    #location_df = pd.DateFrame()

    # print df.head()
    # print df.info()
    # print df.describe()
    # print df.shape
    # print df.isnull()
    #print df.Sep_Business_Days.sum()
    #print df.groupby("Location").Sep_Business_Days.sum()
    #print df.groupby("Location").sum()
    #print df.groupby(["WON"]).agg(sum)
    #print df.groupby(["WON"]).sum()
    df_groupby_WON_SUM = df.groupby(["WON"]).sum()
    df_groupby_WON_COUNT = pd.DataFrame(df.groupby(["WON"]).Resource_Name.count())
    df_groupby_WON_COUNT.rename(columns={"Resource_Name":"Resource Count"},inplace=True)

    print df_groupby_WON_SUM
    print df_groupby_WON_COUNT
    print "Location=",df.groupby(["Location"]).Sep_Business_Days.sum()
    print "Location=Onshore", df[df["Location"]=='Onshore'].Sep_Business_Days.sum()
    print "Location=Offshore", df[df["Location"] == 'Offshore'].Sep_Business_Days.sum()

    df_team_onsite_offshore = pd.DataFrame(df.groupby(["Team_Name", "Location"]).Resource_Name.count())
    print "Team_Name & Location=", df_team_onsite_offshore



    stats_list = []

    df_groupby = df.groupby("Location")

    for group_key,group_data in df_groupby:

        if(group_key <> ""):
            print "Key=",group_key
            group_data = group_data[group_data["Resource_Name"] <> '']
            stats_list.append(setKeyValues("Resource_Count_By_Location_"+group_key,len(group_data)))

    # t = (Location_Total.append(k) for k,group in df_groupby)
    # #print type(t)
    # for i in t:
    #     # location_df = location_df.append(i)
    #     print i

    #df = df[df["Resource_Name"] <> ""]

    #print df.head()
    print stats_list


    onsite   = getValueByKey("Resource_Count_By_Location_Onshore",stats_list)
    offshore = getValueByKey("Resource_Count_By_Location_Offshore",stats_list)
    onsite_offshore_ratio_value = round((onsite / (onsite + offshore)) * 100, 2)

    onsite_real = df[df["Location"]=='Onshore'].Sep_Business_Days.sum()
    offshore_real = df[df["Location"] == 'Offshore'].Sep_Business_Days.sum()
    onsite_offshore_ratio_value_real = round((onsite_real / (onsite_real + offshore_real)) * 100, 2)



    stats_list.append(getActiveResourceCount(df,"Sep","Active_Resource_Count_Total"))
    stats_list.append(setKeyValues("Onsite_Offshore_Ratio_Resource_Count",onsite_offshore_ratio_value))
    stats_list.append(setKeyValues("Onsite_Offshore_Ratio_By_Location_Days", onsite_offshore_ratio_value_real))

    print stats_list

    df_stats = pd.DataFrame(stats_list)


    writer = pd.ExcelWriter(GV_OUTPUT_FOLDER+"Projection_Data.xlsx")
    df.to_excel(writer,sheet_name="Projection_Data",columns=required_columns_projection,index=False)
    df_stats.to_excel(writer,sheet_name="Statistics",columns=required_columns_stats,index=False)
    df_groupby_WON_COUNT.to_excel(writer,sheet_name="Resource Count - By WON",index=True)
    df_groupby_WON_SUM.to_excel(writer, sheet_name="Billable Cost - By WON", index=True)
    df_team_onsite_offshore.to_excel(writer, sheet_name="Team Split", index=True)
    #df = pd.read_json(rows)

processProjections()
