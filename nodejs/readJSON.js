// read the json file
// display the values
var jsonfile = require('jsonfile')
var file = 'C:/MDR/Data/Repository/CSV_Sharepoint_Output/BTP_Phase1_2_Objects.json'

jsonfile.readFile(file, function(err, obj) {
  //console.dir(obj)
  //console.dir(obj[i]["Entity Name"])
	var count_ux = 0
	var count_vm = 0
	for (i=0;i<obj.length;i++){

		if(obj[i]["System Name"] == "UX Sitemap") count_ux++
		if(obj[i]["System Name"] == "Visual Map") count_vm++
	}
  
	console.log("UX Count :",count_ux)
	console.log("VM Count :",count_vm)
})
