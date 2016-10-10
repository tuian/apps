import csv,json
print type(open('C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.csv'))

file = open('C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.csv')
print file
#print file.readlines(-1)
# for line in file:
#     print line

file.close()
print file
with open('C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.csv') as filec:
    #print filec
    csvDict = csv.DictReader(filec)
    print "DictReader() return type",type(csvDict)

    print "Field Names",csvDict.fieldnames,csvDict.line_num
    list_objs = [obj for obj in csvDict]
    print type(list_objs),len(list_objs)
    print type(list_objs[0])
    print list_objs[0].keys()
    print list_objs[0].values()
    csvDict.restkey
    print csvDict.restkey

print type(range(1,10+1))
list_num = [i for i in range(1,10+1)]

print list_num

list_num = [[1,2] in [[1,2],2,3]]

print list_num