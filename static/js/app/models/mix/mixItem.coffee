define  ['utils', 'vent', 'models/comment/commentCollection', 'models/comment/commentItem', 'app.lib/backbone.dss.model'],
(utils, vent, CommentCollection, CommentItem, DssModel) ->
    class MixItem extends DssModel
        urlRoot: com.podnoms.settings.urlRoot + "mix/"

        relations: [
            type: Backbone.Many #nature of the relation
            key: "comments" #attribute of Model
            relatedModel: CommentItem #AssociatedModel for attribute key
        ]

        addComment: (comment, success, error) ->
            c = undefined
            if comment
                c = @get("comments").create(
                    comment: comment
                    mix_id: @get("slug")
                ,
                    success: ->
                        success()

                    error: ->
                        error()
                )
            else
                error "Comment cannot be empty"

        MixItem