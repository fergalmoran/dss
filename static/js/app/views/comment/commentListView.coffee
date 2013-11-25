define ['marionette', 'models/comment/commentItem', 'views/comment/commentItemView', 'text!/tpl/CommentListView'],
(Marionette, CommentItem, CommentItemView, Template) ->
    class CommentListView extends Marionette.CompositeView

        template: _.template(Template)
        tagName: "ul"
        className: "activity-listing media-list"
        itemView: CommentItemView
        itemViewContainer: "#comment-list-container"

    CommentListView
