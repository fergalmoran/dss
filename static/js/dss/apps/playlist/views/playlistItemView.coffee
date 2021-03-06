@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.PlaylistItemView extends Marionette.ItemView
        template: "playlistitem"
        tagName: "ul"
        className: "item-list"

        ui:
            mixExistsIndicator: ".playlist-selected-indicator"

        events:
            "click #playlist-delete": "onDeletePlaylist"
            "click #playlist-open": "onOpenPlaylist"
            "click .profile-activity": "onClickItem"

        onClickItem: (e) ->
            e.stopPropagation()

            @model.containsMix @mix, (result) =>
                if result
                    @model.get("mixes").remove(@mix)
                else
                    @model.get("mixes").add(@mix)

                @model.save(
                    "mixes"
                    @model.get("mixes")
                    patch: true
                )

                @render()

        onDeletePlaylist: (e) ->
            utils.messageBox "/dlg/DeletePlaylistConfirm", =>
                @model.destroy()

            e.stopPropagation()

        onOpenPlaylist: (e) ->
            e.stopPropagation()
            App.Router.navigate("/playlist/" + @model.get("slug"), true)

        setContained: (contained)=>
            @ui.mixExistsIndicator.prop('checked', contained)


        onRender: ->
            @ui.mixExistsIndicator.hide()
            @model.containsMix(@mix, @setContained)
