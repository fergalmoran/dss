define ['backbone', 'models/user/userItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, UserItem, DssCollection) ->
        class UserCollection extends DssCollection
            model: UserItem
            url:com.podnoms.settings.urlRoot + "user/"

        UserCollection

