@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.PlaylistLayout extends Marionette.CompositeView
        template: "playlistlayout"
        childView: Views.PlaylistItemView
        childViewContainer: "#existing-playlists"

        ui:
            newPlaylistName: "#new-playlist-name"
            newPlaylistLayout: "#new-playlist-wrapper"

        events:
            "click #add-playlist": "addPlaylist"
            "click form": "stopDefaults"

        constructor: ->
            Marionette.CompositeView::constructor.apply this, arguments
            @mix = arguments[0].mix

        stopDefaults: (e)->
            e.stopPropagation()

        onBeforeAddChild: (child)->
            child.mix = @mix

        renderIntermediate: ->
            debugger
            @render()

        addPlaylist: (e)=>
            console.log("Clicked")
            unless typeof(App.currentUser) is "undefined"
                playlistName = @ui.newPlaylistName.val()
                if not not playlistName
                    playlist = new App.PlaylistApp.Models.PlaylistItem
                        name: playlistName
                        mixes: [id: @mix.id]

                    playlist.save()
                    @collection.add(playlist)
                    console.log("Adding new: " + playlistName)
                else
                    @ui.newPlaylistLayout.addClass('has-error')

            e.stopPropagation()
