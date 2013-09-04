define ['backbone.relational', 'models/comment/commentCollection', 'models/comment/commentItem', 'app.lib/backbone.dss.model'], \
    (Backbone, CommentCollection, CommentItem, DSSModel) ->
        class MixItem extends DSSModel
            urlRoot: com.podnoms.settings.urlRoot + "mix/"
            """
            relations: [
                type: Backbone.HasMany
                key: "comments"
                relatedModel: CommentItem
                collectionType: CommentCollection
                reverseRelation:
                  key: "hasItems"
                  includeInJSON: "id"
              ]
            """
        MixItem