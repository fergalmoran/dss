@Dss.module "ActivityApp.Models", (Models, App, Backbone) ->
    class Models.ActivityCollection extends Backbone.Collection
        model: Models.ActivityItem
        url:com.podnoms.settings.urlRoot + "activity/"

        initialize: ->
            @listenTo App.vent, "model:activity:new", (url) =>
                console.log("ActivityCollection: activity:new")
                item = new Models.ActivityItem()
                item.fetch
                    url: url,
                    success: (response) =>
                        console.log("ActivityCollection: item fetched")
                        console.log(response)
                        @add response

        comparator: (item)->
            -item.id

