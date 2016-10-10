// variables in the global namesspace
var myApp = angular.module("myApp",['ngRoute']);

day = "Monday";

// everything in javascript is an object, even a function is an object

var Person = function(firstname,lastname){
    this.fistname = firstname;
    this.lastname = lastname;
    
}

// -----------------------------------------
// dependency inside the function
function logPerson1(){
    var john = new Person('John','Mc Donald')
    console.log(john.fistname+ " "+john.lastname)
}

//logPerson1()
// -----------------------------------------

// dependency injected into the function (as function parameter)
function logPerson2(person){
    console.log(person.fistname+ " "+person.lastname)
}

var john = new Person('John','Mc Donald')
//logPerson2(john)
// -----------------------------------------

myApp.config(function($routeProvider){
    $routeProvider
    .when('/',{
        templateUrl: 'pages/main.html',
        controller: 'myController'
    })
    .when('/second',{
        templateUrl: 'pages/second.html',
        controller: 'secondController'
    })
});

myApp.controller("myController",['$scope','$location',function($scope,$location){
$scope.day = "Wednesday"
console.log("Location, absUrl :" +$location.absUrl());
console.log("Location, hash   :" +$location.hash());
console.log("Location, path   :" +$location.path());
console.log("Location, url    :" +$location.url());
//console.log(day);
//console.log($scope);

}]);

myApp.controller("secondController",['$scope','$location',function($scope,$location){
$scope.day = "Wednesday"
console.log("Location, absUrl :" +$location.absUrl());
console.log("Location, hash   :" +$location.hash());
console.log("Location, path   :" +$location.path());
console.log("Location, url    :" +$location.url());
//console.log(day);
//console.log($scope);

}]);

// function and function as a string... 
console.log(Person)
// when i get the string, I can parse the input parameters and do something with it..
console.log(Person.toString())
console.log(angular.injector().annotate(Person));

var Person1 = function(firstname,$scope,lastname){
    this.fistname = firstname;
    this.lastname = lastname;
    
}
console.log(angular.injector().annotate(Person1));

