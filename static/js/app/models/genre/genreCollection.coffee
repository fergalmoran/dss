define ['backbone', 'models/genre/genreItem', 'app.lib/backbone.dss.model.collection'],
(Backbone, GenreItem, DssCollection) ->
    class GenreCollection extends DssCollection
        model: GenreItem

    GenreCollection