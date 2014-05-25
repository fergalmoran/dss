@Dss.module "MixApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.MixTabHeaderView extends Marionette.ItemView
        template: "mixtabheaderview"
        tagName: "ul"
        className: "mix-toggle nav nav-pills"

        initialize: (options)->
            @options = options
            @listenTo(App.vent, "mix:showlist", @tabChanged)

        tabChanged: (options) ->
            $('#mix-tab li[id=li-' + options.order_by + ']', @el).addClass('active')
            true
