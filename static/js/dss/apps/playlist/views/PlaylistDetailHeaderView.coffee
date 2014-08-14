@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.PlaylistDetailHeaderView extends Marionette.ItemView
        template: "playlistheaderview"

        events:
            "click #playlist-rss-feed": "showPlaylistRssFeed"


        showPlaylistRssFeed: (e) ->
            window.open("/podcast/playlist?type=playlist&name=" + @model.get("name"))