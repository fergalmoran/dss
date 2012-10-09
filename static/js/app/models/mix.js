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
    },
    isValid:function () {
        this.errors = {};
        if (com.podnoms.utils.isEmpty(this.get('title'))) {
            return this.addError('title', 'Please enter a title');
        }
        return "";
    }
});
window.MixCollection = TastypieCollection.extend({
    url:com.podnoms.settings.urlRoot + "mix/",
    model:Mix
});
