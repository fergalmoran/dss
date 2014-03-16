define ['app.lib/dssView', 'text!/tpl/NotificationsItemView'],
(DssView, Template) ->
    class NotificationsItemView extends DssView
        template: _.template(Template)
        tagName: "li"
