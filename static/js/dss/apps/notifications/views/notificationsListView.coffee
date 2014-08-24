@Dss.module "NotificationApp.Views", (Views, App, Backbone, Marionette) ->
    class Views.NotificationsListView extends Marionette.CompositeView

        template: "notificationslistview"
        childView: Views.NotificationsItemView
        childViewContainer: "#notif_list_node"
        tagName: "li"

        events:
            "click #notifications-dropdown": "showNotifications"
        ui:
            notificationSurround: "#notification-surround"
            notificationCountBadge: "#notification-count-badge"
            notificationCount: "#notification-count"

        initialize: =>
            @listenTo App.vent, "model:notification:new", @initialize
            #quick and dirty check to see if user is logged in
            @collection = new App.NotificationApp.Models.NotificationCollection
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
                $(@ui.notificationCountBadge).hide()
            else
                $(@ui.notificationCount).text(newCount + " new notifications")
                $(@ui.notificationCountBadge).show()
                $(@ui.notificationCountBadge).addClass('animate pulse')
                console.log("Animating bell")
                $('#notification-icon', @el).addClass('icon-animated-bell')

                $(@ui.notificationCountBadge).text(newCount)

        showNotifications: ->
            console.log("NotificationsListView: showNotifications")
            $.ajax
                url: '/ajax/mark_read/'
                type: 'post'
                success: =>
                    $(@ui.notificationCountBadge).hide()
                    @collection.meta.is_new = 0

    Views.NotificationsListView
