@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.PlaylistShowListLayout extends Marionette.LayoutView
        template: "mixlistlayout"
        regions:
            headerRegion: "#mix-list-heading"
            bodyRegion: "#mix-list-body"

        initialize: (options)->
            @showPlaylists(options)

        showPlaylists: (options) ->
            @model = new App.PlaylistApp.Models.PlaylistItem({id: options.slug})
            @model.fetch
                success: (result)=>
                    if result
                        @bodyRegion.show(new App.MixApp.Views.MixListView({collection: result.get("mixes")}))
                        @headerRegion.show(new Views.PlaylistDetailHeaderView({model: @model}))

    Views.PlaylistShowListLayout