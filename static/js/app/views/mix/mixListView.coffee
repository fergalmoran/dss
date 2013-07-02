define ['marionette', 'vent', 'models/mix/mixCollection', 'views/mix/mixItemView', 'text!/tpl/MixListView'],
(Marionette, vent, MixCollection, MixItemView, Template) ->
    class  MixListView extends Marionette.CompositeView

        template: _.template(Template)
        className: "mix-listing audio-listing"
        itemView: MixItemView
        itemViewContainer: "#mix-list-container-ul"

        currentMix = -1

        initialize: =>
            console.log "MixListView: initialize"
            @collection = new MixCollection()
            @collection.fetch(
                data: @options
                success: =>
                    console.log("MixListView: Collection fetched")
                    @tabChanged(@options.order_by)
                    @listenTo(vent, 'mix:play', @mixPlay)
                    true
            )
            return

        mixPlay: (model) ->
            console.log "MixListView: mixPlay"

            if currentMix != -1
                v = @children.findByModelCid(currentMix)
                v.mixStop(v.model)
            currentMix = model.cid
            return

        tabChanged: (type) ->
            console.log("MixListView: tab changed")
            $('#mix-tab li[id=li-' + type + ']', @el).addClass('active')
            true

    MixListView

