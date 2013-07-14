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
            @collection = new NotificationCollection
            @collection.fetch(
                success: =>
                    $(@ui.notificationCount).text(@collection.meta.is_new)
            )

        showNotifications: ->
            console.log("Marking read")

    NotificationsListView
