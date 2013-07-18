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
            @listenTo(vent, "user:showdetail", @showUserView)

        onShow: ->
            @headerRegion.show(new MixTabHeaderView())

        showMixList: (options)->
            @bodyRegion.show(new MixListView(options))

        showUserView: (options) ->
            @headerRegion.close()
            @bodyRegion.show(new MixListView(options))

    MixListRegionView