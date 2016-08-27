import docx
import pandas as pd
import openpyxl #install openpyxl first
import os
import xlsxwriter
import sys
import datetime
import re
import warnings
reload(sys)
sys.setdefaultencoding('utf8')
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

def cleanString(input_string):

    input_string = input_string.strip()
    input_string = input_string.replace('\n','')
    input_string = input_string.replace('\r', '')
    input_string = input_string.replace(u"\xa0",'')

    if(input_string==''):
        output_string = "-"
    else:
        output_string = input_string
    #print "Input_String:#",output_string.strip() + "#\n"
    return output_string

def processRow(row,method):
    dict = {}
    cell_length = len(row.cells)
    print "Cell Length", cell_length
    #for i in range(len(row.cells)):
        # if((row.cells[i].text) == u'\xc2'):
        #     print "-"
        # else:
        #     print cleanString(row.cells[i].text)
    dict["Element"] = cleanString(row.cells[1].text)
    dict["Description"] = cleanString(row.cells[2].text)
    dict["Type"] = cleanString(row.cells[3].text)

    if(cell_length == 12):
        # only for IFS document 339
        dict["Path"] = cleanString(row.cells[11].text)
    else:
        # all other IFS documents
        dict["Path"] = cleanString(row.cells[8].text)

    dict["Method"] = method

    #print dict
    return dict



    # print row.cells[0].text.encode("utf-8"),\
    #     row.cells[1].text.encode("utf-8"),\
    #     row.cells[2].text.encode("utf-8"), \
    #     row.cells[3].text.encode("utf-8")

    # if(row.cells[0].text == row.cells[1].text):
    #     print "Values are same"

def iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def getListofFiles(gesb_ifs_document_path,control_file_name):
    list = []
    df = pd.read_excel(gesb_ifs_document_path+control_file_name)
    #print df.head()
    df = df[df["Flag"] == "Open"]
    #print df.head()

    # for i in range(0, len(df)):
    #     #if (".XSD" in str(df2.loc[i, "Entity Name"])):
    #     print df.loc[i,"Flag"]
    #     list.append(df.loc[i,"Flag"])

    return df

def getAllDocs(gesb_ifs_document_path,control_file_name):
    print "--------------------GEBS IFS Documents Extractor--------------------------------------"
    print "\t IFS Documents Folder =",gesb_ifs_document_path
    df_files = getListofFiles(gesb_ifs_document_path,control_file_name)
    for i in range(0, len(df_files)):
        #if (".XSD" in str(df2.loc[i, "Entity Name"])):
        print df_files.loc[i,"Input GESB IFS Name"], df_files.loc[i,"Output File Name"], df_files.loc[i,"Flag"]
        print gesb_ifs_document_path + df_files.loc[i, "Input GESB IFS Name"], gesb_ifs_document_path + df_files.loc[i, "Output File Name"]
        processIFS(gesb_ifs_document_path+ df_files.loc[i,"Input GESB IFS Name"],gesb_ifs_document_path+df_files.loc[i,"Output File Name"])







'''
#create mapping excel sheet
outputDirectory = gesb_ifs_document_path+'\\Output'

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

fileName= outputDirectory + '\\mappingsheet' +  datetime.datetime.now().strftime("%Y%m%d-%H%M%S") +".xlsx"
workbook = xlsxwriter.Workbook(fileName)

worksheet_IFS = workbook.add_worksheet("IFS Objects")
worksheet_XSD = workbook.add_worksheet("XSD Objects")
worksheet2 = workbook.add_worksheet("Mapping Specification")
#sets the column width for the given range. E.g. set the columns from 0 to 8 a width of 30 characters

worksheet_IFS.set_column(0, 1 ,15)
worksheet_IFS.set_column(2, 3 ,30)
worksheet_IFS.set_column(4, 6 ,10)
'''

def processIFS(input_file,output_file):

    gesb_ifs_document_path = "C:\\01 BT\\00 MDR\\Phase2\\GCM Data\\GESB IFS\\"

    gesb_ifs_document_name = 'WBC SVC0339 - ModifyOrganisationCustomer IFS_v2.docx'
    gesb_ifs_document_name_output = "WBC SVC0339 - ModifyOrganisationCustomer IFS_v2.csv"

    #sectionName = "Request Attributes_X"
    #sectionName = "Positive Response Attributes_X"

    # gesb_ifs_document_name = "WBC SVC0338 - ModifyIndividualCustomer IFS v2.docx"
    # gesb_ifs_document_name_output = "WBC SVC0338 - ModifyIndividualCustomer IFS v2.csv"

    # gesb_ifs_document_name = "WBC_SVC0418-WBC-Maintaint_IP_Contact_Methods_IFS.docx"
    # gesb_ifs_document_name_output = "WBC_SVC0418-WBC-Maintaint_IP_Contact_Methods_IFS.csv"

    # gesb_ifs_document_name        = "SVC0258-RetrieveDetailsAndArrangementRelationshipsForIPs_v10.docx"
    # gesb_ifs_document_name_output = "SVC0258-RetrieveDetailsAndArrangementRelationshipsForIPs_v10.csv"

    sectionName_1 = "Request Attributes"
    sectionName_2 = "Positive Response Attributes"


    # gesb_file_input = gesb_ifs_document_path + gesb_ifs_document_name
    # gesb_file_output = gesb_ifs_document_path + gesb_ifs_document_name_output

    gesb_file_input = input_file
    gesb_file_output = output_file

    print gesb_file_input
    #print "TEST",u"\xa0" + ":"

    print "\t Processing IFS Document: " + gesb_file_input
    ispara = False

    #pat = re.compile(r'\n')
    cell_0 = ""
    list_rows = []
    required_columns = ["Method","Element","Description","Type","Path"]

    try:
        doc1 = docx.Document(gesb_file_input)

        for block in iter_block_items(doc1):

            if (isinstance(block, Table)):
                #print ("Table found")
                if (ispara):
                    print ("Found the table we wanted :", sectionName_1 + " | " + sectionName_2)
                    ispara = False
                    count = 0
                    total_rows = len(block.rows)

                    for row in block.rows:
                        print "Row {} of {}: ".format(count,total_rows)

                        #if(count < 200):
                        list_rows.append(processRow(row,section_name_found))

                        # if(row.cells[0].text == row.cells[1].text):
                        #     print "Values are same"
                        #print cleanString(row.cells[0].text),cleanString(row.cells[1].text),cleanString(row.cells[2].text),cleanString(row.cells[3].text),cleanString(row.cells[4].text),cleanString(row.cells[5].text)


                        #print row.cells[0].text.encode("utf-8"), row.cells[1].text.encode("utf-8"),row.cells[2].text.encode("utf-8"), row.cells[3].text.encode("utf-8")
                        count = count + 1

            if (isinstance(block, Paragraph)):
                #print ("Paragraph found")
                block_sectionName = block.text.encode("utf-8").strip()
                #print block_sectionName
                if ((block_sectionName.upper() == (sectionName_1.strip()).upper()) | (block_sectionName.upper() == (sectionName_2.strip()).upper())):
                    print("Matching section found")
                    section_name_found = block_sectionName
                    ispara = True

        #sent the information in the list to a CSV file
        df = pd.DataFrame(data=list_rows, columns=required_columns, index=None)
        df.to_csv(gesb_file_output, sep=",", index=False, header=True)
    except IOError as e:
        print "ERROR in reading a document. Check if the file exists or the filename"
        print e
        #workbook.close()
        exit()


#processIFS()
gesb_ifs_document_path = "C:\\01 BT\\00 MDR\\Phase2\\GCM Data\\GESB IFS\\"
control_file_name = "GEBS_IFS_Documents_List.xlsx"
getAllDocs(gesb_ifs_document_path,control_file_name)