console.log("Entered") 
   
window.addEventListener('hashchange',function(){
   console.log("hash changed") 
   console.log("host= "+window.location.host) 
   console.log("hostname= "+window.location.hostname) 
   console.log("Hash= "+window.location.hash) 
});