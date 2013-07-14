define ['marionette', 'vent', 'models/mix/mixCollection', 'views/mix/mixItemView', 'text!/tpl/MixListView'],
(Marionette, vent, MixCollection, MixItemView, Template) ->
    class  MixListView extends Marionette.CompositeView

        template: _.template(Template)
        className: "mix-listing audio-listing"
        itemView: MixItemView
        itemViewContainer: "#mix-list-container-ul"

        currentMix = -1

        initialize: =>
            @collection = new MixCollection()
            @collection.fetch
                data: @options
            return

        mixPlay: (model) ->
            if currentMix != -1
                v = @children.findByModelCid(currentMix)
                v.mixStop(v.model)
            currentMix = model.cid
            return

        tabChanged: (type) ->
            $('#mix-tab li[id=li-' + type + ']', @el).addClass('active')
            true

    MixListView

