define ['app', 'moment', 'app.lib/dssView', 'vent', 'text!/tpl/UserListItemView'],
(App, moment, DssView, vent, Template)->
    class UserItemView extends DssView
        template: _.template(Template)
        className: "row"

        events:
            "click #follow-button": -> vent.trigger("user:follow", @model)
            "click #follow-button-login": -> vent.trigger("app:login", @model)

        initialize: =>
            @listenTo(@model, 'change:is_following', @render)

    UserItemView
