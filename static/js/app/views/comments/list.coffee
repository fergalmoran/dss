define ['marionette', 'views/comments/item', 'text!/tpl/CommentListView'],
(Marionette, CommentItemView, Template) ->
    class CommentListView extends Marionette.CompositeView

        template: _.template(Template)
        tagName: "ul"
        className: "activity-listing media-list"
        itemView: CommentItemView
        itemViewContainer: "#comment-list-container"

        initialize: ->
            console.log "CommentListView: initialize"

    CommentListView
