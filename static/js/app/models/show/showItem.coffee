define ['models/user/userCollection', 'app.lib/backbone.dss.model'],
(UserCollection, DssModel) ->
    class UserItem extends DssModel
        urlRoot: com.podnoms.settings.urlRoot + "user/"
        relations: [
            type: Backbone.Many
            key: "followers"
            relatedModel: Backbone.Self
            collectionType: UserCollection
        ]

    UserItem