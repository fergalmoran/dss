define ['marionette', 'vent', 'views/widgets/mixTabHeaderView', 'views/mix/mixListView', 'text!/tpl/MixListLayoutView'],
(Marionette, vent, MixTabHeaderView, MixListView, Template) ->

    class MixListRegionView extends Marionette.Layout
        template: _.template(Template)
        regions:{
            headerRegion: "#mix-list-heading"
            bodyRegion: "#mix-list-body"
        }

        initialize: ->
            @listenTo(vent, "mix:showlist", @showMixList)

        onShow: ->
            @headerRegion.show(new MixTabHeaderView())

        showMixList: (options)->
            console.log("Layout: showoing mixlist")
            @bodyRegion.show(new MixListView(options))
            @tabChanged(options.order_by)

        tabChanged: (type) ->
            $('#mix-tab li[id=li-' + type + ']', @el).addClass('active')
            true

    MixListRegionView