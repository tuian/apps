/*
var nav_menu = [
    { url:"/screens", lable:"Screens"},
    { url:"/dashboard", lable:"Dashboard"},
    { url:"/ldm", lable:"LDM"},
    { url:"/xsd", lable:"XSD"}
    
]

console.log("nav_menu items"+nav_menu);
*/

myapp = angular.module('menuApp', ['angular.filter']);

// start of menuController
myapp.controller('menuController', function($scope,$http) {
        console.log("Inside the menuController");
                $http.get('/static/json/menu_nav.json').success(function(data){
                    $scope.menu_items = data;

                    console.log("I'm called");
                    console.log($scope.menu_items);
                    
                }); // end of http.get.success
});
// end of menuController

// start of ldmController
myapp.controller('metadataObjController', function($scope,$http,$filter,$location,$log) {

    console.log("Inside the metadataObjController");
    
    // Default Value for System Name
    // $scope.system_name = "ABS" ; 
     $scope.system_name = "UX Sitemap" ; 
    // $scope.system_name = "" ; 
    
    // Default Value for Instance Name
    //    $scope.instance_name = "LDM";
    
    $scope.$watch('system_name', function(value) {
       console.log("system_name: "+value);
        $scope.system_name = value ; 
    // }); // end of watch
    

            $log.warn("Before HTTP GET | system_name: "+$scope.system_name+ " instance_name: "+$scope.instance_name);

            url_hash  = $location.hash()
            url_path  = $location.path()
            url_absUrl = $location.absUrl()

            $log.info("url_hash"+url_hash);$log.info("url_path"+url_path);$log.info("url_absUrl"+url_absUrl);
    
    
            $http.get('/static/json/BTP_Phase1_2_Objects.json').success(function(data){

                // $scope.rows = data;
                $log.warn("After HTTP GET | system_name: "+$scope.system_name + " instance_name: "+$scope.instance_name);            

                // Filter the rows from the json based on the page context , parameters initialized in the div ng-controller

                //$scope.rows = $filter('filter')(data, { "System Name": $scope.system_name,"Instance Name":$scope.instance_name });

                // strict comparison flat = true, to do an exact match
                $scope.rows = $filter('filter')(data,  {"System_Name": $scope.system_name},true);

                $scope.count_display_flag = true;
                $scope.rows_count = ($scope.rows).length;
                console.log("Length: "+ ($scope.rows).length + ", Size: " + $scope.rows.size)

                console.log("Display flag and count = "+ $scope.count_display_flag + " and " + $scope.rows_count );

                console.log("I'm called, ldm, http get success");
                //console.log($scope.rows);
                console.log("Display flag and count = "+ $scope.count_display_flag + " and " + ($scope.rows_count) );

            }); // end of http.get.success
        }); // end of watch
    }); // end of ldmController


myapp.controller('TableFilterController', function($scope,$http,$filter) {
                console.log("Inside the TableFilterController");
                $scope.names = ["PHP", "Python", "Ruby", "Scheme"];



                $scope.screen_status_filtered_count_flag = false;
                console.log("screen_status_filtered_count_flag= "+$scope.screen_status_filtered_count_flag);

                $scope.screen_status_count_flag = false;
                console.log("screen_status_count_flag="+$scope.screen_status_count_flag);


                $http.get('./screenobjects_json').success(function(data){
                    $scope.screen_objects_json = data;

                    console.log("I'm called");
                    console.log($scope.screen_objects_json);
                    $scope.screen_status_count_flag = true;
                    
                    $scope.screen_status_count = ($scope.screen_objects_json).length;
                    console.log("Screen Objects Length"+$scope.screen_status_count);
                    
                    console.log("screen_status_count_flag="+$scope.screen_status_count_flag);

                    $scope.screen_status_filtered_count_flag = true;
                    console.log("screen_status_filtered_count_flag="+$scope.screen_status_filtered_count_flag);

                }); // end of http.get.success


                $scope.$watch("f.Harvest_Status", function(query){
                    console.log("before ..watch Harvest status="+query);
                    $scope.screen_status_filtered_count = $filter("filter")($scope.screen_objects_json, query).length;
                    console.log("after..watch Harvest status="+query);
                });
                

                $scope.screen_objects_static = [
                    {
                      Functionality : 'Mercury',
                      Entity_x0020_Name : 0.4,
                      MDR_x0020_Release : 0.055
                    },
                    {
                      Functionality : 'Venus',
                      Entity_x0020_Name : 0.7,
                      MDR_x0020_Release : 0.815
                    },
                    {
                      Functionality : 'Earth',
                      Entity_x0020_Name: 1,
                      MDR_x0020_Release : 1
                    }
                ];

        });

myapp.directive('autoComplete', function($timeout) {
        return function(scope, iElement, iAttrs) {
            iElement.autocomplete({
                source: scope[iAttrs.uiItems],
                select: function() {
                    $timeout(function() {
                      iElement.trigger('input');
                        }, 0);
                    }
                });
            };
});

