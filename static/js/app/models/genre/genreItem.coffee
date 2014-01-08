define ['backbone', 'backbone-associations'],
(Backbone) ->
    class GenreItem extends Backbone.Model
        urlRoot: com.podnoms.settings.urlRoot + "genres"

    GenreItem