@Dss.module "CommentsApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.CommentItemView extends Marionette.ItemView
        template: "commentitemview"
        events:
            "click #delete-comment": "deleteComment"
            "click #like-comment": "likeComment"

        deleteComment: ->
            utils.messageBox "/dlg/DeleteCommentConfirm", =>
                @model.destroy()

        likeComment: ->
            console.log("CommentItemView: likeComment")
            App.vent.trigger("comment:like", @model)
            true
