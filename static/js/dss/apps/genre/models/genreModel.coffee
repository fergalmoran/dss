@Dss.module "GenresApp.Models", (Models, App, Backbone) ->
    class Models.GenreItem extends Backbone.AssociatedModel
        urlRoot: com.podnoms.settings.urlRoot + "genres"

    class Models.GenreCollection extends Backbone.Collection
            model: Models.GenreItem

    Models.GenreCollection
