var Comment = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "comments/"
});

var CommentCollection = TastypieCollection.extend({
    model:Comment,
    comparator: function(comment){
        return -comment.get("id");
    }
});