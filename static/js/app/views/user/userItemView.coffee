define ['app', 'moment', 'marionette', 'vent', 'text!/tpl/UserListItemView'],
(App, moment, Marionette, vent, Template)->
    class UserItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "div"
        className: "row-fluid"

        events:
            "click #follow-button": "followUser"
            "click #follow-button-login": "promptLogin"

        templateHelpers:
            humanise: (date)->
                moment(date).fromNow()

        initialize: =>
            @listenTo(@model, 'change:is_following', @render)

        followUser: ->
            console.log("UserItemView: followUser")
            vent.trigger("user:follow", @model)

        promptLogin:->
            vent.trigger("app:login", @model)

    UserItemView
