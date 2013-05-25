define ['marionette', 'text!/tpl/CommentItemView'],
(Marionette, Template) ->
    class CommentItemView extends Marionette.ItemView
        template: _.template(Template)

    CommentItemView