@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.PlaylistDetailHeaderView extends Marionette.ItemView
        template: "playlistheaderview"

        events:
            "click #playlist-rss-feed": "showPlaylistRssFeed"
            "click .share-button": "playlistShare",


        showPlaylistRssFeed: (e) ->
            window.open("/podcast/playlist?type=playlist&name=" + @model.get("name"))

        playlistShare: (e) ->
            mode = $(e.currentTarget).data("mode");
            console.log("PlaylistDetailHeaderView: " + mode)
            App.vent.trigger("playlist:share", mode, @model)

