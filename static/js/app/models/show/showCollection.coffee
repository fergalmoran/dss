define ['backbone', 'models/show/showItem', 'app.lib/backbone.dss.model.collection'],
(Backbone, ShowItem, DssCollection) ->
    class ScheduleCollection extends DssCollection
        model: ShowItem
        page: 0
        limit: 20
        url: ->
            com.podnoms.settings.urlRoot + "show/?limit=" + @limit + "&offset=" + Math.max(@page-1, 0) * @limit

        initialize: ->
            if not ShowItem
                @model = require('models/show/showItem')

    ScheduleCollection

