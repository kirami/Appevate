url ="http://localhost:8080/"


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
        $.get( url + "/api/action/", {"api_key":this.api_key, "api_secret":this.api_secret},
        	function( data ) { 
			  
			  console.log(data[0])
			  first = data[0]
			  appInfo =  new AppInfo({"id": first["id"], "name": first["name"]})

			  $(".apiInfo").text(appInfo.id)
			  
			}); 
		
		return appInfo; 
	
    },

    redeemCash:function(user_id){
        userInfo = null;
        $.get( url +"/api/payment/send-payment", {"api_key":this.api_key, "api_secret":this.api_secret, "user_id" : user_id},
            function( data ) { 
              
              console.log(data[0])
              
              //userInfo =  new UserInfo({"id": first["id"], "name": first["name"]})

              //$(".apiInfo").text(userInfo.id)
              
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

function UserInfo(__attrs){
    this.__attrs = __attrs;
    this.id = this.__attrs.id;
    this.name = this.__attrs.name;
}
UserInfo.prototype = {
    constructor: Appivator
}