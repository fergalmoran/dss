define ['app.lib/dssView', 'utils', 'text!/tpl/CommentItemView'],
(DssView, utils, Template) ->
    class CommentItemView extends DssView
        template: _.template(Template)
        events: {
            "click #delete-comment": "deleteComment"
        }

        deleteComment: ->
            utils.messageBox "/dlg/DeleteCommentConfirm", =>
                @model.destroy()
    CommentItemView