@Dss.module "MixApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.MixListView extends Marionette.CompositeView
        template: "mixlistview"
        className: "mix-listing audio-listing"
        itemView: Views.MixItemView
        itemViewContainer: "#mix-list-container-ul"

        currentMix = -1

        mixPlay: (model) ->
            if currentMix != -1
                v = @children.findByModelCid(currentMix)
                v.mixStop(v.model)
            currentMix = model.cid
            return

        onRender: ->
            window.scrollTo 0, 0

    Views.MixListView