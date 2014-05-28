@Dss.module "ActivityApp.Models", (Models, App, Backbone) ->
    class Models.ActivityItem extends Backbone.Model
        urlRoot: com.podnoms.settings.urlRoot + "activity/"

        parse: (model) ->
            model.human_date = moment(model.date).fromNow()
            model

