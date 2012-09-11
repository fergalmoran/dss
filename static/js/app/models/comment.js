/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var Comment = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "comments/"
});

var CommentCollection = TastypieCollection.extend({
    model:Comment,
    comparator: function(comment){
        return -comment.get("id");
    }
});