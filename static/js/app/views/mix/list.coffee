define ['marionette', 'models/mix/collection', 'views/mix/item', 'text!/tpl/MixListView'],
(Marionette, MixCollection, MixItemView, Template) ->
    class  MixListView extends Marionette.CompositeView

        template: _.template(Template)
        className: "mix-listing audio-listing"
        itemView: MixItemView
        itemViewContainer: "#mix-list-container-ul"

        initialize: ->
            console.log "MixListView: Before render"
            @collection = new MixCollection()
            @collection.fetch(
                data: @options
                success: =>
                    console.log("MixListView: Collection fetched")
                    return
            )
            return

        onRender: ->
            $('#li-' + @options.type, @el).addClass('active')
            true

    MixListView

