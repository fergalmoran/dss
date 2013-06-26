define ['marionette', 'text!/tpl/ActivityListItemView', 'libs/jquery-ui'],
(Marionette, Template) ->
    class ActivityItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "li"
        className: "media"

        onRender: (itemView) ->
            $(itemView.el).effect("bounce", "slow")
            $(itemView.el).effect("highlight", {}, 3000)
            true
