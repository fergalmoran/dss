define ['marionette', 'text!/tpl/NotificationsItemView'],
(Marionette, Template) ->
    class NotificationsItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "li"
