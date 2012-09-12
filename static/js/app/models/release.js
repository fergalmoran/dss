/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var Release = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "release/",
    isValid:function () {
        this.errors = {};
        if (isEmpty(this.get('release_label'))) {
            return this.addError('release_label', 'Please choose a label');
        }
        if (isEmpty(this.get('release_title'))) {
            return this.addError('release_title', 'Please choose a title');
        }
        if (isEmpty(this.get('release_artist'))) {
            return this.addError('release_artist', 'Please choose an artist');
        }
        if (isEmpty(this.get('release_date'))) {
            return this.addError('release_date', 'Please choose a valid date');
        }
        if (isEmpty(this.get('release_description'))) {
            return this.addError('release_description', 'Please enter a description of some sort');
        }
        return "";
    }
});
var ReleaseCollection = TastypieCollection.extend({
    url:com.podnoms.settings.urlRoot + "release/",
    model:Release
});
