/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
define(['jquery'], function ($) {

    $(document).ready(function () {
        if (window.location.hash == '#_=_') {
            window.location.hash = "";
        }
        if (window.location.hash == 'upload#') {
            Backbone.history.navigate("/");
        }
        if (!Array.prototype.indexOf) {
            console.log("Shimming indexOf for IE8");
            Array.prototype.indexOf = function (searchElement /*, fromIndex */) {
                'use strict';
                if (this == null) {
                    throw new TypeError();
                }
                var n, k, t = Object(this),
                    len = t.length >>> 0;

                if (len === 0) {
                    return -1;
                }
                n = 0;
                if (arguments.length > 1) {
                    n = Number(arguments[1]);
                    if (n != n) { // shortcut for verifying if it's NaN
                        n = 0;
                    } else if (n != 0 && n != Infinity && n != -Infinity) {
                        n = (n > 0 || -1) * Math.floor(Math.abs(n));
                    }
                }
                if (n >= len) {
                    return -1;
                }
                for (k = n >= 0 ? n : Math.max(len - Math.abs(n), 0); k < len; k++) {
                    if (k in t && t[k] === searchElement) {
                        return k;
                    }
                }
                return -1;
            };
        }
    });

    $(document).ajaxError(function (event, xhr, settings) {
        //catch the 401's and don't log them, assume app is handling these
        console.log("Site: ajaxError");
    });

    $(document).ajaxSend(function (event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });


    if (com.podnoms.settings.isDebug) {
    } else {
        console.log("Looking under the hood? Check us out on github https://github.com/fergalmoran/dss");
        var console = {};
        console.log = function (message) {
        };
    }
});
