/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var Activity = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "activity/"
});

var ActivityCollection = TastypieCollection.extend({
    model: Activity,
    url:com.podnoms.settings.urlRoot + "activity/",
    comparator: function (activity) {
        return -activity.get("id");
    }
});