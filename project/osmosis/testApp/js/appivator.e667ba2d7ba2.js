//url ="https://appivator.sharemagnet.net"

url = "http://127.0.0.1:8080"

/* SocialRebate CORS request library.
 * Copyright ShareMagnet LLC 2015 All rights reserved.
 */
function CORS(){}

CORS.prototype = {
    constructor: CORS,
    createXhr: function(method, url){
        /* Create an xhr that is CORS capable */
        var _xhr = new XMLHttpRequest();
            if ("withCredentials" in _xhr){
            /* XHR for Chrome/Firefox/Opera/Safari. */
            _xhr.open(method, url, true);
        }else if(typeof XDomainRequest != "undefined"){
            /* XDomainRequest for IE. */
            _xhr = new XDomainRequest();
            _xhr.open(method, url);
        }else{
            /* CORS not supported. */
            _xhr = null; 
        }
        return _xhr;
    },
    post: function(url, options){
        
        /* Perform a CORS request. */
        _xhr = this.createXhr("POST", url);
        if(!_xhr){

            return;
        }
        _xhr.onload = options.onload;
        _xhr.onerror = options.onerror;
        /* Content Type */
        _xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        _xhr.setRequestHeader("Accept", "application/json"); 
        if(options.headers){
            for(header in options.headers){
                _xhr.setRequestHeader(header, options.headers[header]);
            }
        }
        _xhr.send(options.post_data || null);
    },
    get: function(url, options){
        
        /* Perform a CORS request. */
        _xhr = this.createXhr("GET", url);
        if(!_xhr){

            return;
        }
        _xhr.onload = options.onload;
        _xhr.onerror = options.onerror;
        /* Content Type */
        _xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        _xhr.setRequestHeader("Accept", "application/json"); 
        if(options.headers){
            for(header in options.headers){
                _xhr.setRequestHeader(header, options.headers[header]);
            }
        }
        _xhr.send(options.post_data || null);
    },

    put: function(url, options){
        
        /* Perform a CORS request. */
        _xhr = this.createXhr("PUT", url);
        if(!_xhr){
 
            return;
        }
        _xhr.onload = options.onload;
        _xhr.onerror = options.onerror;
        /* Content Type */
        _xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        _xhr.setRequestHeader("Accept", "application/json"); 
        if(options.headers){
            for(header in options.headers){
                _xhr.setRequestHeader(header, options.headers[header]);
            }
        }
        _xhr.send(options.post_data || null);
    }
}

CORS = new CORS();


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

    getUserInfo: function(id){
        userInfo = null;
        options = {
            "onload": function() {
                
                updateUser(this.responseText)
                  

            },
            "onerror": function() {console.log("bad")}
        }
        CORS.get( url + "/api/user/" + id+"/?api_key="+this.api_key + "&api_secret="+this.api_secret, options)
       
    
    },

    redeemCash:function(user_id){
        userInfo = null;

        
        options = {
            "onload": function() {

            },
            "onerror": function() {console.log("bad")}
        }
        CORS.get( url + "/api/payment/send-payment/?api_key="+this.api_key + "&api_secret="+this.api_secret + "&id=" + user_id , options)
        
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
    this.email = this.__attrs.email;
    this.paypal_email = this.__attrs.paypal_email;
    this.phone_number = this.__attrs.phone_number;
}
UserInfo.prototype = {
    constructor: Appivator
}



