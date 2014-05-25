@Dss.module "CommentsApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.CommentItemView extends Marionette.ItemView
        template: "commentitemview"
        events: {
            "click #delete-comment": "deleteComment"
        }

        deleteComment: ->
            utils.messageBox "/dlg/DeleteCommentConfirm", =>
                @model.destroy()

    Views.CommentItemView