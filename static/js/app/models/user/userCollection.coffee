define ['backbone', 'models/user/userItem', 'app.lib/backbone.dss.model.collection'],
(Backbone, UserItem, DssCollection) ->
    class UserCollection extends DssCollection
        model: UserItem
        page: 0
        limit: 20
        url: ->
            com.podnoms.settings.urlRoot + "user/?limit=" + @limit + "&offset=" + Math.max(@page-1, 0) * @limit
        initialize: ->
            if not UserItem
                @model = require('models/user/userItem')

    UserCollection

