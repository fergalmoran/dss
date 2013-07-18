define ['backbone', 'vent', 'models/notifications/notificationItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, vent, NotificationItem, DssCollection) ->
        class NotificationCollection extends DssCollection
            model: NotificationItem
            url:com.podnoms.settings.urlRoot + "notification/"
            limit: 5

            initialize: ->
                @listenTo vent, "model:notification:new", (url) =>
                    console.log("NotificationCollection: notification:new")
                    item = new NotificationItem()
                    item.fetch
                        url: url,
                        success: (response) =>
                            console.log("NotificationCollection: item fetched")
                            console.log(response)
                            @add response

            comparator: (item)->
                -item.id

        NotificationCollection