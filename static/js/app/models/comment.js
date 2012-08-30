var Comment = DSSModel.extend({
    urlRoot:window.appSettings.urlRoot + "comments/"
});

var CommentCollection = TastypieCollection.extend({
    model:Comment,
    comparator: function(comment){
        return -comment.get("id");
    }
});