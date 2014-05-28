@Dss.module "UserApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.UserItemView extends Marionette.ItemView
        template: "useritemview"
        className: "row"

        events:
            "click #follow-button": -> App.vent.trigger("user:follow", @model)
            "click #follow-button-login": -> App.vent.trigger("app:login", @model)

        initialize: =>
            @listenTo(@model, 'change:is_following', @render)

    Views.UserItemView
