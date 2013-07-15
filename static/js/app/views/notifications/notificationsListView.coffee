define ['marionette', 'underscore', 'vent',
        'models/notifications/notificationCollection',
        'views/notifications/notificationsItemView',
        'text!/tpl/NotificationsListView'],
(Marionette, _, vent, NotificationCollection, NotificationsItemView, Template) ->
    class NotificationsListView extends Marionette.CompositeView

        template: _.template(Template),
        tagName: "span",
        className: "dropdown"
        itemView: NotificationsItemView,
        itemViewContainer: "#notif_list_node",
        events:
            "click #notifications-dropdown": "showNotifications"
        ui:
            notificationSurround: "#notification-surround"
            notificationCount: "#notification-count"

        initialize: ->
            #quick and dirty check to see if user is logged in
            @collection = new NotificationCollection
            @collection.fetch(
                success: =>
                    $(@ui.notificationCount).text(@collection.meta.is_new)
                    if @collection.meta.is_new == 0
                        $(@ui.notificationSurround).hide()
                error: =>
                    $(@ui.notificationSurround).hide()
            )

        showNotifications: ->
            $.ajax
                url: '/ajax/mark_read/'
                type: 'post'
                success: =>
                    $(@ui.notificationSurround).hide()

    NotificationsListView
