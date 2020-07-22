function Appivator(__attrs){
    this.__attrs = __attrs;
    this.api_key = this.__attrs.api_key;
    this.api_secret = this.__attrs.api_secret;
}
Appivator.prototype = {
    constructor: Appivator,
    api_key: function(){
        return this.api_key;
    },

    getAppData: function(){
        appInfo = null;
        $.get( "/api/action/", {"api_key":this.api_key, "api_secret":this.api_secret},
        	function( data ) { 
			  
			  console.log(data[0])
			  first = data[0]
			  appInfo =  new AppInfo({"id": first["id"], "name": first["name"]})

			  $(".apiInfo").text(appInfo.id)
			  
			}); 
		
		return appInfo; 
	
    }
}

function AppInfo(__attrs){
    this.__attrs = __attrs;
    this.id = this.__attrs.id;
    this.name = this.__attrs.name;
}
AppInfo.prototype = {
	constructor: Appivator
}