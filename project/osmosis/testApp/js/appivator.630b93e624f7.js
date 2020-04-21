//url ="https://appivator.sharemagnet.net"

APPIVATOR_URL = "http://127.0.0.1:8080"

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
    },
    patch: function(url, options){
        
        /* Perform a CORS request. */
        _xhr = this.createXhr("PATCH", url);
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

appInfo = null

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
        
        $.get( APPIVATOR_URL + "/api/app/", {"api_key":this.api_key, "api_secret":this.api_secret},
        	function( data ) { 
			  
			 
			  first = data[0]
			  appInfo =  new AppInfo({"id": first["id"], "name": first["name"], "url":first["url"], "stripe_account":first["stripe_account"],"stripe_id":first["stripe_id"]})

			    //$(".apiInfo").text(appInfo.id)
                $(".appId").text(appInfo.id)
                $(".appURL").text(appInfo.url)
                $("#stripe_id").val(appInfo.stripe_id)
                $("#stripe_account").val(appInfo.stripe_account)
			  
			}); 
		
		return appInfo; 
	
    },

    getProgramData: function(active){

        options = {
            "onload": function() {
                res = JSON.parse(this.responseText)[0]; 
                //console.log(res)
                $("#name").val(res.name)
                $("#budget").val(res.budget)
                if(res.CPM)
                    $("#CPM").prop('checked', true);
                if(res.CPC)
                    $("#CPC").prop('checked', true);
                if(res.CPA)
                    $("#CPA").prop('checked', true);
                
                programId = res.id 

            },
            "onerror": function() {console.log("bad")}
        }
        url = APPIVATOR_URL + "/api/program/?api_key="+this.api_key + "&api_secret="+this.api_secret
        if (active)
            url +="&is_active=true"
        else
            url +="&is_active="
        CORS.get( url , options)
    
    },

    getUserInfo: function(id){
        userInfo = null;
        options = {
            "onload": function() {
                
                updateUser(this.responseText)
                  

            },
            "onerror": function() {console.log("bad")}
        }
        CORS.get( APPIVATOR_URL+ "/api/user/" + id+"/?api_key="+this.api_key + "&api_secret="+this.api_secret, options)
       
    
    },

    redeemCash:function(user_id){
        userInfo = null;

        
        options = {
            "onload": function() {

            },
            "onerror": function() {console.log("bad")}
        }
        CORS.get( APPIVATOR_URL+ "/api/payment/send-payment/?api_key="+this.api_key + "&api_secret="+this.api_secret + "&id=" + user_id , options)
        
    }
}

function AppInfo(__attrs){
    this.__attrs = __attrs;
    this.id = this.__attrs.id;
    this.name = this.__attrs.name;
    this.url = this.__attrs.url;
    this.stripe_account = this.__attrs.stripe_account;
    this.stripe_id = this.__attrs.stripe_id;
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



