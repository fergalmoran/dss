define ['app.lib/backbone.dss.model'], \
    (DssModel) ->
        class UserItem extends DssModel
            urlRoot: com.podnoms.settings.urlRoot + "user/"

        UserItem