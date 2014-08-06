@Dss.module "UserApp.Models", (Models, App, Backbone, Marionette, $    ) ->
    class Models.UserItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "user/"
        relations: [
            type: Backbone.Many
            key: "followers"
            relatedModel: Backbone.Self
            collectionType: Models.UserCollection
        ,
            type: Backbone.Many
            key: "playlists"
            relatedModel: App.PlaylistApp.Models.PlaylistItem
            collectionType: App.PlaylistApp.Models.PlaylistCollection
        ]



