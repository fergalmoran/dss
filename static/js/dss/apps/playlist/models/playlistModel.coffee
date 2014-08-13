@Dss.module "PlaylistApp.Models", (Models, App, Backbone) ->
    class Models.PlaylistItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "playlist/"
        relations: [
            type: Backbone.Many
            key: "mixes"
            relatedModel: App.MixApp.Models.MixItem
            collectionType: App.MixApp.Models.MixCollection
        ]

        containsMix: (mix, callback) ->
            mixes = @get("mixes")
            result = false
            if mixes.length != 0
                mixes.each (item) ->
                    if item.id == mix.id
                        result = true

            callback(result)

    class Models.PlaylistCollection extends Backbone.Collection
        model: Models.PlaylistItem

        containsMix: (mix, callback)->
            return callback(false) if item.length = 0
            @each (item) ->
                if item.containsMix(mix, callback)
                    return true

            return false

        save: (options)->
            Backbone.sync("create", this, options)
