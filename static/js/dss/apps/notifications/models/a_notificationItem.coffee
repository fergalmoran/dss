@Dss.module "NotificationApp.Models", (Models, App, Backbone, Marionette, $, _, vent) ->
    class Models.NotificationItem extends Backbone.Model
        urlRoot: com.podnoms.settings.urlRoot + "activity/"

        parse: (model) ->
            model.human_date = moment(model.date).fromNow()
            model

    Models.NotificationItem