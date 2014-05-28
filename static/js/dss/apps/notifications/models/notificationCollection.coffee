@Dss.module "NotificationApp.Models", (Models, App, Backbone, Marionette, $, _, vent) ->
    class Models.NotificationCollection extends Backbone.Collection
        page: 0
        model: Models.NotificationItem
        limit: 5

        newCount: ->
          return @is_new

        url: ->
            com.podnoms.settings.urlRoot + "notification/?limit=" + @limit + "&offset=" + Math.max(@page - 1, 0) * @limit

        initialize: ->
            @listenTo App.vent, "model:notification:new", (url) =>
                console.log("NotificationCollection: notification:new")
                item = new NotificationItem()
                item.fetch
                    url: url
                    success: (response) =>
                        console.log("NotificationCollection: item fetched")
                        console.log(response)
                        @add response

        comparator: (item)->
            -item.id

    Models.NotificationCollection