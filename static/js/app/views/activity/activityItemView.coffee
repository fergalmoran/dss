define ['marionette', 'text!/tpl/ActivityListItemView'],
(Marionette, Template) ->
    class ActivityItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "li"
        className: "media"