define ['backbone', 'app.lib/backbone.dss.model'], \
    (Backbone, DssModel) ->
        class MixItem extends Backbone.Model
            urlRoot: com.podnoms.settings.urlRoot + "mix/"

        MixItem