@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.PlaylistItemView extends Marionette.ItemView
        template: "playlistitem"
