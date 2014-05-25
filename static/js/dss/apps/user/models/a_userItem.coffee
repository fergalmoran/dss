@Dss.module "UserApp.Models", (Models, App, Backbone, Marionette, $    ) ->
    class Models.UserItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "user/"
        relations: [
            type: Backbone.Many
            key: "followers"
            relatedModel: Backbone.Self
            collectionType: Models.UserCollection
        ]

