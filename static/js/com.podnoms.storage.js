/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};
Storage.prototype.setObject = function(key, value) {
    this.setItem(key, JSON.stringify(value));
};

Storage.prototype.getObject = function(key) {
    var value = this.getItem(key);
    return value && JSON.parse(value);
};

com.podnoms.storage = {
    setItem: function(key, value){
        localStorage.setItem(key, value);
    },
    getItem: function(key){
        return localStorage.getItem(key);
    },
    clearItem: function(key){
        localStorage.removeItem(key);
    }
};