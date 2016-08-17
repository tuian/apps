import htql;


file = open("d_details.html","r")
lines = file.readlines()
file.close()

print(lines);
print(lines.__str__());

query_data_view_component_div ="<div>:data-component-name";
query_data_view_component_form ="<form><div>:data-component-name";

#print lines

page="<a href=a.html>1</a><a href=b.html>2</a><a href=c.html>3</a>";

query_All ="<a>:href,tx";
query_href ="<a>:href";

"""
for url,text in htql.HTQL(page, query_All):
    print url;
    print text;

for url in htql.HTQL(page, query_href):
    print(url);
"""

for d_v_c_values in htql.HTQL(lines.__str__(), query_data_view_component_div):
    print(d_v_c_values);

for d_v_c_values in htql.HTQL(lines.__str__(), query_data_view_component_form):
    print(d_v_c_values);


