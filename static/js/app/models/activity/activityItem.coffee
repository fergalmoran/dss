define ['backbone'], \
    (Backbone) ->
        class ActivityItem extends Backbone.Model
            urlRoot: com.podnoms.settings.urlRoot + "activity/"

