define ['app.lib/backbone.dss.model'],
(DssModel) ->
    class ShowItem extends DssModel
        urlRoot: com.podnoms.settings.urlRoot + "show/"
    ShowItem
