define ['backbone', 'models/mix/mixItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, MixItem, DssCollection) ->
        class MixCollection extends DssCollection
            model: MixItem
            url:com.podnoms.settings.urlRoot + "mix/"

            _parse: (data) ->
                console.log("MixCollection: parse")

        MixCollection

