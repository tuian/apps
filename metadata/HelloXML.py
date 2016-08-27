import xml
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd

def setAttribute(system_name,element_count,xsd_name,element_type,obj_name,sub_element_count,attribute_name,attribute_desc,xpath):

    dict_object = {}
    dict_object["System Name"] = system_name
    dict_object["Instance Name"] = "Default"
    dict_object["Owner"] = ""
    dict_object["Parent"] = ""
    dict_object["URL"] = ""
    dict_object["Document Name"] = ""

    dict_object["XPATH"] = xpath

    dict_object["Element_Count"] = element_count
    dict_object["Entity Name"] = xsd_name
    dict_object["Element Type"] = element_type
    dict_object["Type"] = "Attribute"
    dict_object["Complex_Object_Name"] = obj_name
    dict_object["SubElement_Count"] = sub_element_count
    dict_object["Element_Name"] = attribute_name

    if(str(obj_name) <> ''):
        dict_object["Attribute Name"] = str(obj_name)+"$"+str(attribute_name)
    else:
        dict_object["Attribute Name"] = attribute_name

    dict_object["Description"] = attribute_desc

    return dict_object

def sentToCSV(output_filepath,output_filename,list_objects):
    import pandas as pd
    #required_columns = ["Element_Count","SubElement_Count","System Name","Instance Name","Owner","Parent","Entity Name","Type","Complex_Object_Name","Element_Name","Attribute Name","Attribute Description"]
    required_columns    = ["System Name", "Instance Name", "Entity Name",  "Element Type","Attribute Name", "Owner", "Parent","Type","Description","URL","Document Name","XPATH"]
    #columns_objects_csv = ["System Name", "Instance Name", "Entity Name",  "Attribute Name", "Owner", "Parent", "Type","Description"]
    #print list_objects
    df = pd.DataFrame(data=list_objects,columns=required_columns,index=None)
    df.to_csv(output_filepath + output_filename, sep=",", index=False, header=True)

def processXML(system_name,folder_path_input,xsd_filename,folder_path_output,output_csv_filename):

    list_object = []

    tree = ET.parse(folder_path_input + xsd_filename)
    root = tree.getroot()

    #print root.tag
    #print root.attrib
    #
    # print len(root)
    # print root[0].text
    count = 1
    # for child in root:
    #      print count, child.tag, child.attrib
    #      count = count + 1

    desc = ""
    pattern = re.compile(r'</?p>|<p >|,', re.I)

    for simpleType in root.iter('{http://www.w3.org/2001/XMLSchema}simpleType'):
        #print count
        print "{}. SimpleType: {} ".format(count,simpleType.get('name'))
        desc_simple = "Values should be any one of the following : "
        desc_simple_e = ""
        desc = ""

        if (simpleType.findall('{http://www.w3.org/2001/XMLSchema}restriction/{http://www.w3.org/2001/XMLSchema}enumeration') <> None):

            enums  = simpleType.findall('{http://www.w3.org/2001/XMLSchema}restriction/{http://www.w3.org/2001/XMLSchema}enumeration')

            for e in enums:



                if (e.find('{http://www.w3.org/2001/XMLSchema}annotation/{http://www.w3.org/2001/XMLSchema}documentation') <> None):
                    description = e.find('{http://www.w3.org/2001/XMLSchema}annotation/{http://www.w3.org/2001/XMLSchema}documentation')
                    if(description.text <> None):
                        desc = description.text.encode('utf-8')
                        desc = desc.replace('\n', ' ')
                        desc = pattern.sub('', desc)
                        desc = desc.replace('\'', '')
                    #print desc
                else:
                    desc = ""

                desc_simple_e = desc_simple_e + e.get('value') + " - "+ desc + " | "

            desc_simple = desc_simple + desc_simple_e
            print desc_simple
        else:
            desc_simple = ""

        list_object.append(setAttribute(system_name,count,xsd_filename,"SimpleType","","",simpleType.get('name'),desc_simple,""))
        count = count + 1

    for complexType in root.iter('{http://www.w3.org/2001/XMLSchema}complexType'):
        #print count
        #print count, "ComplextType", complexType.get('name')
        element_count = 1
        xpath_value = ""
        for element in complexType.iter('{http://www.w3.org/2001/XMLSchema}element'):
            if(element.get('name') <> ''):

                if(element.find('{http://www.w3.org/2001/XMLSchema}annotation/{http://www.w3.org/2001/XMLSchema}documentation') <> None):
                    description = element.find('{http://www.w3.org/2001/XMLSchema}annotation/{http://www.w3.org/2001/XMLSchema}documentation')
                    desc = description.text.encode('utf-8')
                    desc = desc.replace('\n',' ')
                    desc = pattern.sub('',desc)
                    desc = desc.replace('\'', '')
                    print desc
                else:
                    desc  = ""

                xpath_value = element.get('type')

                print "{}. | Complex Type Name: {} | {}.{}. | Complex Element Name: {} | Description: {} | XPATH: {}".format(count,complexType.get('name'),count,element_count,element.get('name'),desc,xpath_value)
                list_object.append(setAttribute(system_name,count, xsd_filename,"ComplexType", complexType.get('name'),str(count)+"."+str(element_count), element.get('name'),desc,xpath_value))
                element_count = element_count + 1

        count = count + 1

    sentToCSV(folder_path_output,output_csv_filename,list_object)

# for item in list_object:
#     print item["Type"]


def getXSDFiles(input_folder_path):

    list_xsd_filenames = []
    #print "Input Folder Path:",input_folder_path

    for file in os.listdir(input_folder_path):
        if file.endswith(".xsd"):
            #print os.path.abspath(file)
            #list_xsd_filenames.append(os.path.abspath(file))
            list_xsd_filenames.append(file)
    # print "\n List of xsd files:"
    # for item in list_xsd_filenames:
    #     print "\t File: ", item

    return list_xsd_filenames


xml_folder_path_input = "C:\\MDR\\Data\XML\\input\\"
xml_folder_path_output = "C:\\MDR\\Data\XML\\output\\"


xml_filename_1 = "SVC0418_MaintainIPContactMethods_v1.xsd"
xml_filename_2 = "SVC0258_RetrieveDetailsAndArrangementRelationshipsForIPs_v10.xsd"
xml_filename_3 = "SVC0338_ModifyIndividualCustomer_v2.xsd"
xml_filename_4 = "SVC0339_ModifyOrganisationCustomer_v2.xsd"
xml_filename_5 = "OnboardingReplyV3_0.xsd"
xml_filename_6 = "OnboardingRequestV3_0.xsd"

output_xml_filename_1 = "SVC0418_MaintainIPContactMethods.csv"
output_xml_filename_2 = "SVC0258_RetrieveDetailsAndArrangementRelationshipsForIPs.csv"
output_xml_filename_3 = "SVC0338_ModifyIndividualCustomer.csv"
output_xml_filename_4 = "SVC0339_ModifyOrganisationCustomer.csv"
output_xml_filename_5 = "OnboardingReplyV3_0.csv"
output_xml_filename_6 = "OnboardingRequestV3_0.csv"

output_xml_filename   = "BTICC_GESB_XSD_Fields.csv"

def merge_csv_files():

    df1 = pd.read_csv(xml_folder_path_output + output_xml_filename_1, sep=",")
    df2 = pd.read_csv(xml_folder_path_output + output_xml_filename_2, sep=",")
    df3 = pd.read_csv(xml_folder_path_output + output_xml_filename_3, sep=",")
    df4 = pd.read_csv(xml_folder_path_output + output_xml_filename_4, sep=",")
    df5 = pd.read_csv(xml_folder_path_output + output_xml_filename_5, sep=",")
    df6 = pd.read_csv(xml_folder_path_output + output_xml_filename_6, sep=",")

    df = [df1 , df2 , df3 , df4 , df5 , df6]

    df = pd.concat(df)

    df.to_csv(xml_folder_path_output+output_xml_filename,sep=",", index=False, header=True)


processXML("GESB",xml_folder_path_input,xml_filename_1,xml_folder_path_output,output_xml_filename_1)
processXML("GESB",xml_folder_path_input,xml_filename_2,xml_folder_path_output,output_xml_filename_2)
processXML("GESB",xml_folder_path_input,xml_filename_3,xml_folder_path_output,output_xml_filename_3)
processXML("GESB",xml_folder_path_input,xml_filename_4,xml_folder_path_output,output_xml_filename_4)
processXML("BTICC",xml_folder_path_input,xml_filename_5,xml_folder_path_output,output_xml_filename_5)
processXML("BTICC",xml_folder_path_input,xml_filename_6,xml_folder_path_output,output_xml_filename_6)
merge_csv_files()

# list_xsd_files = getXSDFiles(xml_folder_path)
# print "\n List of xsd files:"
# for xsd_file in list_xsd_files:
#     print "\t", xsd_file