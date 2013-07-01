define ['backbone', 'vent', 'models/activity/activityItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, vent, ActivityItem, DssCollection) ->
        class ActivityCollection extends DssCollection
            model: ActivityItem
            url:com.podnoms.settings.urlRoot + "activity/"

            initialize: ->
                @listenTo vent, "model:activity:new", (url) =>
                    console.log("ActivityCollection: activity:new")
                    item = new ActivityItem()
                    item.fetch
                        url: url,
                        success: (response) =>
                            console.log("ActivityCollection: item fetched")
                            console.log(response)
                            @add response

            comparator: (item)->
                -item.id

        ActivityCollection