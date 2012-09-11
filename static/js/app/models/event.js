/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var Event = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "event/",
    isValid:function () {
        this.errors = {};
        if (com.podnoms.utils.isEmpty(this.get('event_description'))) {
            return this.addError('event_description', 'Please enter description');
        }
        return "";
    }
});
var EventCollection = TastypieCollection.extend({
    url:com.podnoms.settings.urlRoot + "event/",
    model:Event
});
