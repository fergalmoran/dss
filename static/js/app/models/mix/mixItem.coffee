define  [
    'utils', 'vent',
    'models/comment/commentCollection', 'models/comment/commentItem', 'models/genre/genreCollection', 'models/genre/genreItem',
    'app.lib/backbone.dss.model'],
(utils, vent,
    CommentCollection, CommentItem, GenreCollection, GenreItem, DssModel) ->
    class MixItem extends DssModel
        urlRoot: com.podnoms.settings.urlRoot + "mix/"

        relations: [
            type: Backbone.Many
            key: "comments"
            relatedModel: CommentItem
            collectionType: CommentCollection
        ,
            type: Backbone.Many
            key: "genres"
            relatedModel: GenreItem
            collectionType: GenreCollection
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