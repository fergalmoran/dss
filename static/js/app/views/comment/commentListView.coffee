define ['marionette', 'models/comment/commentItem', 'views/comment/commentItemView', 'text!/tpl/CommentListView'],
(Marionette, CommentItem, CommentItemView, Template) ->
    class CommentListView extends Marionette.CompositeView

        template: _.template(Template)
        tagName: "ul"
        className: "activity-listing media-list"
        itemView: CommentItemView
        itemViewContainer: "#comment-list-container"

        ui:
            commentText: '#comment-text'

        events:
            "click #btn-add-comment": "addComment"

        initialize: ->
            console.log "CommentListView: initialize"

        addComment: ->
            console.log "CommentListView: addComment"
            @collection.create
                mix_id: @collection.mix.get("id")
                comment: @ui.commentText.val()
            ,
              success: (newItem) =>
                @ui.commentText.val ""
                true

              error: (a, b, c) ->
                console.log a
                console.log b
                console.log c
                true

            true

    CommentListView
