define ['app', 'moment', 'app.lib/dssView', 'vent', 'text!/tpl/UserListItemView'],
(App, moment, DssView, vent, Template)->
    class UserItemView extends DssView
        template: _.template(Template)
        className: "row"

        events:
            "click #follow-button": "followUser"
            "click #follow-button-login": "promptLogin"

        initialize: =>
            @listenTo(@model, 'change:is_following', @render)

        followUser: ->
            console.log("UserItemView: followUser")
            vent.trigger("user:follow", @model)

        promptLogin:->
            vent.trigger("app:login", @model)

    UserItemView
