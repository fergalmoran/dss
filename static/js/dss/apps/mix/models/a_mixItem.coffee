@Dss.module "MixApp.Models", (Models, App, Backbone) ->
    class Models.MixItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "mix/"

        relations: [
            type: Backbone.Many
            key: "comments"
            relatedModel: App.CommentsApp.Models.CommentItem
            collectionType: App.CommentsApp.Models.CommentCollection
        ,
            type: Backbone.Many
            key: "genres"
            relatedModel: App.GenresApp.Models.GenreItem
            collectionType: App.GenresApp.Models.GenreCollection
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

    Models.MixItem