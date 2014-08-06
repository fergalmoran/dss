@Dss.module "MixApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.MixListLayout extends Marionette.LayoutView
        template: "mixlistlayout"
        regions:
            headerRegion: "#mix-list-heading"
            bodyRegion: "#mix-list-body"

        initialize: (options)->
            @listenTo(App.vent, "mix:showlist", @showMixList)
            @listenTo(App.vent, "user:showdetail", @showUserView)
            @showMixList(options)

        onShow: ->
            @headerRegion.show(new Views.MixTabHeaderView())

        showMixList: (options) ->
            @collection = new App.MixApp.Models.MixCollection()
            @collection.fetch
                data: options
                success: (collection)=>
                    if collection.length > 0
                        @bodyRegion.show(new Views.MixListView({collection: collection}))

        showUserView: (options) ->
            @bodyRegion.show(new Views.MixListView(options))
            user = new UserItem({id: options.user})
            user.fetch(
                success: =>
                    @headerRegion.show(new UserItemView({model: user}))
            )

    Views.MixListLayout