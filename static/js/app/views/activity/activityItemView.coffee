define ['marionette', 'text!/tpl/ActivityListItemView', 'libs/jquery-ui'],
(Marionette, Template) ->
    class ActivityItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "li"
        className: "media"

        onDomRefresh: ->
            @$el.effect("bounce", "slow")
