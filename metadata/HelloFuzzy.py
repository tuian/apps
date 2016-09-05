from mdr_util import *

orphaned_string_list = ["hisismy_word","Thisismy_words"]

orphaned_string = "BTFG$UI_NTFCN_LIST.NTFCN"
list_of_strings = ["BTFG$UI_NTFCN_LIST#NTFCN","BTFG$UI_NTFCN_LIST.NTFCN.XSD","BTFG$UI_NTFCN#LIST.NTFCN.XSD"]
control_limit = 0.80

# d = L.distance(orphaned_string,list_of_strings[0])
# print "Levenshtein distance for Orphaned String '{}' with Matching String '{}' : {}".format(orphaned_string,list_of_strings[0],d)
# print "'{}'\n'{}'\n{} ".format(orphaned_string,list_of_strings[0],d)

#j = L.jaro_winkler(orphaned_string, list_of_strings[0], control_limit)
# j = L.jaro(orphaned_string, list_of_strings[0])

# print "Levenshtein jaro_winkler score for Orphaned String '{}' with Matching String '{}' : {}".format(orphaned_string,list_of_strings[0],j)
# print "'{}'\n'{}'\n{} ".format(orphaned_string,list_of_strings[0],j)

output_dict_list_sequence_match = SeqMatch(orphaned_string,list_of_strings,control_limit)
#output_dict_list_jara_winkler   = LevenshteinMatch(orphaned_string,list_of_strings,control_limit)
#print output_dict_list

for item in output_dict_list_sequence_match:
    #print item["Algorithm"],item["Orphaned_String"], item["Control_Limit"],item["Match_String"], item["Match_Percentage"]
    print item

# for item in output_dict_list_jara_winkler:
#     print item["Algorithm"],item["Orphaned_String"], item["Control_Limit"],item["Match_String"], item["Match_Percentage"]

#print diff.get_close_matches('appel', ['ape', 'apple', 'peach', 'puppy'])
# s.find_longest_match(0, 5, 0, 9)
# print diff.Match(a=0, b=4, size=5)
