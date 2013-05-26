define ['backbone', 'models/comment/commentItem', 'app.lib/backbone.dss.model.collection'],
(Backbone, CommentItem, DssCollection) ->
    class CommentCollection extends DssCollection
        model: CommentItem

    CommentCollection