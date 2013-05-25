define ['app.lib/backbone.dss.model'], \
    (DssModel) ->
        class MixItem extends DssModel
            urlRoot: com.podnoms.settings.urlRoot + "mix/"

        MixItem