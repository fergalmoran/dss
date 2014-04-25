define ['marionette', 'vent', 'models/mix/mixCollection', 'views/mix/mixItemView', 'text!/tpl/MixListView'],
(Marionette, vent, MixCollection, MixItemView, Template) ->
    class  MixListView extends Marionette.CompositeView

        template: _.template(Template)
        className: "mix-listing audio-listing"
        emptyView: Marionette.ItemView.extend(template: "#mix-empty-view")
        itemView: MixItemView
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

    MixListView

