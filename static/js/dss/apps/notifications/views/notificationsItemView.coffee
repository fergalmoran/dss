@Dss.module "NotificationApp.Views", (Views, App, Backbone, Marionette) ->
    class Views.NotificationsItemView extends Marionette.CompositeView
        template: "notificationsitemview"
        tagName: "li"
