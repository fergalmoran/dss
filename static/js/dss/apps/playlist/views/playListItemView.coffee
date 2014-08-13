@Dss.module "PlaylistApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.PlaylistItemView extends Marionette.ItemView
        template: "playlistitem"
        tagName: "ul"
        className: "item-list"

        ui:
            mixExistsIndicator: ".playlist-selected-indicator"

        events:
            "click .profile-activity": "onClickItem"

        onClickItem: (e) ->
            console.log("Clicky clicky")
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

        setContained: (contained)=>
            @ui.mixExistsIndicator.prop('checked', contained)


        onRender: ->
            @ui.mixExistsIndicator.hide()
            @model.containsMix(@mix, @setContained)
