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
    get: function(url, options){
        /* Perform a CORS request. */
        _xhr = this.createXhr("GET", url);
        if(!_xhr){
            /* Figure out what to do here. The worst case scenario
             * is that this user simly does not get offered a rebate.
             * This should happen rarely according to http://caniuse.com/#search=CORS
             */
            return;
        }
        _xhr.onload = options.onload;
        _xhr.onerror = options.onerror;
        /* Content Type */
        _xhr.setRequestHeader("Accept", "application/json"); 
        if(options.headers){
            for(header in options.headers){
                _xhr.setRequestHeader(header, options.headers[header]);
            }
        }
        _xhr.send();
    },
    post: function(url, options){
        /* Perform a CORS request. */
        _xhr = this.createXhr("POST", url);
        if(!_xhr){
            /* Figure out what to do here. The worst case scenario
             * is that this user simly does not get offered a rebate.
             * This should happen rarely according to http://caniuse.com/#search=CORS
             */
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
