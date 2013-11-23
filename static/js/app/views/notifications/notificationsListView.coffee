define ['marionette', 'underscore', 'vent', 'utils',
        'models/notifications/notificationCollection',
        'views/notifications/notificationsItemView',
        'text!/tpl/NotificationsListView'],
(Marionette, _, vent, utils, NotificationCollection, NotificationsItemView, Template) ->
    class NotificationsListView extends Marionette.CompositeView

        template: _.template(Template)
        itemView: NotificationsItemView
        itemViewContainer: "#notif_list_node"
        tagName: "li"
        events:
            "click #notifications-dropdown": "showNotifications"
        ui:
            notificationSurround: "#notification-surround"
            notificationCountBadge: "#notification-count-badge"
            notificationCount: "#notification-count"

        initialize: =>
            #quick and dirty check to see if user is logged in
            @collection = new NotificationCollection
            @collection.fetch(
                success: =>
                    @renderBeacon()
                    @collection.on 'add': (model, collection)=>
                        @collection.meta.is_new += 1
                        @renderBeacon(model)
                error: =>
                    $(@ui.notificationSurround).hide()
            )

        renderBeacon: (model) ->
            newCount = @collection.meta.is_new
            if newCount == 0
                $(@ui.notificationCount).text("Notifications")
                $(@ui.notificationSurround).hide()
            else
                $(@ui.notificationCountBadge).text(newCount)
                $(@ui.notificationCount).text(newCount + " Notifications")
                $(@ui.notificationSurround).show()
                $(@ui.notificationSurround).addClass('animate pulse')
                if model
                    utils.showAlert(model.get('notification_text'))

        showNotifications: ->
            console.log("NotificationsListView: showNotifications")
            $.ajax
                url: '/ajax/mark_read/'
                type: 'post'
                success: =>
                    $(@ui.notificationSurround).hide()
                    @collection.meta.is_new = 0

    NotificationsListView
