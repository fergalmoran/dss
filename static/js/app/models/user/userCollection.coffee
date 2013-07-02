define ['backbone', 'models/user/userItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, UserItem, DssCollection) ->
        class UserCollection extends DssCollection
            page: 0
            limit: 20
            model: UserItem
            url: ->
                com.podnoms.settings.urlRoot + "user/?limit=" + @limit + "&offset=" + @page * @limit

        UserCollection

