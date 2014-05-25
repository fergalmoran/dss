@Dss.module "CommentsApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.CommentListView extends Marionette.CompositeView
        template: "commentlistview"
        tagName: "ul"
        className: "activity-listing media-list"
        itemView: Views.CommentItemView
        itemViewContainer: "#comment-list-container"

    Views.CommentListView
