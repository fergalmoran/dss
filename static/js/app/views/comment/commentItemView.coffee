define ['app.lib/dssView', 'text!/tpl/CommentItemView'],
(DssView, Template) ->
    class CommentItemView extends DssView
        template: _.template(Template)

    CommentItemView