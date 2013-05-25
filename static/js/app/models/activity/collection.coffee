define ['backbone', 'models/activity/item', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, ActivityItem, DssCollection) ->
        class ActivityCollection extends DssCollection
            model: ActivityItem
            url:com.podnoms.settings.urlRoot + "activity/"

        ActivityCollection