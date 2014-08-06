@Dss.module "PlaylistApp.Models", (Models, App, Backbone) ->
    class Models.PlaylistItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "playlist/"
        relations: [
            type: Backbone.Many
            key: "mixes"
            relatedModel: App.MixApp.Models.MixItem
            collectionType: App.MixApp.Models.MixCollection
        ]

    class Models.PlaylistCollection extends Backbone.Collection
        model: Models.PlaylistItem

    Models.PlaylistCollection
