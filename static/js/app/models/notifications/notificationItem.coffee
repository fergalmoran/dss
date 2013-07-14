define ['backbone', 'moment'], \
    (Backbone, moment) ->
        class NotificationItem extends Backbone.Model
            urlRoot: com.podnoms.settings.urlRoot + "activity/"

            parse: (model) ->
                model.human_date = moment(model.date).fromNow()
                model

        NotificationItem