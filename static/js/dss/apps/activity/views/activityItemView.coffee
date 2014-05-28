@Dss.module "ActivityApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.ActivityItemView extends Marionette.ItemView
        template: "activityitemview"
        tagName: "div"

        onRender: (itemView) ->
            $(itemView.el).addClass('animated flash')
            true
