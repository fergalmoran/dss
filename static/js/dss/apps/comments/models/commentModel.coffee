@Dss.module "CommentsApp.Models", (Models, App, Backbone) ->
    class Models.CommentItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "comments"

    class Models.CommentCollection extends Backbone.Collection
        model: Models.CommentItem

    Models.CommentCollection
