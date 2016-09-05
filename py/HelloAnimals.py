from pandas.util.testing import assert_frame_equal
import pandas as pd


xls_file_Animals = pd.ExcelFile('./data/Animals.xlsx')
df_Animals = xls_file_Animals.parse('Sheet1')

xls_file_Animals_New = pd.ExcelFile('./data/Animals_New.xlsx')
df_Animals_New = xls_file_Animals_New.parse('Sheet1')

print "Animals"
print df_Animals

print "Animals New"
print df_Animals_New

# #if(df_Animals_New != df_Animals): print "Hello"
# try:
#     assert_frame_equal(df_Animals_New, df_Animals)
#     print "Inside Try"
# except:
#     # appeantly AssertionError doesn't catch all
#     #return False
#     print "Inside Except"

df = pd.concat([df_Animals_New, df_Animals])
df = df.reset_index(drop=True)
df_gpby = df.groupby(list(df.columns))
idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
df.reindex(idx)

print df