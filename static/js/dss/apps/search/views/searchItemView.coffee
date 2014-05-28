@Dss.module "SearchApp.Views", (Views, App, Backbone, Marionette, $, _, vent) ->
    class Views.SearchItemView extends Marionette.ItemView
        template: "searchresultview"
        el: "li"