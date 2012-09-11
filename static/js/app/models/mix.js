/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
window.Mix = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "mix/",
    schema:{
        title:'Text',
        description:'Text'
    }
});
window.MixCollection = TastypieCollection.extend({
    url:com.podnoms.settings.urlRoot + "mix/",
    model:Mix
});
