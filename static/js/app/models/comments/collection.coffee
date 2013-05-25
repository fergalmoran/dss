define ['backbone', 'models/comments/item', 'app.lib/backbone.dss.model.collection'],
(Backbone, CommentItem, DssCollection) ->
    class CommentCollection extends DssCollection
        model: CommentItem

    CommentCollection