define ['marionette', 'models/mix/mixCollection', 'views/mix/mixItemView', 'text!/tpl/MixListView'],
(Marionette, MixCollection, MixItemView, Template) ->
    class  MixListView extends Marionette.CompositeView

        template: _.template(Template)
        className: "mix-listing audio-listing"
        itemView: MixItemView
        itemViewContainer: "#mix-list-container-ul"

        initialize: ->
            console.log "MixListView: initialize"
            @collection = new MixCollection()
            @collection.fetch(
                data: @options
                success: =>
                    console.log("MixListView: Collection fetched")
                    @tabChanged('latest')
                    true
            )
            return

        onRender: ->
            $('#li-' + @options.type, @el).addClass('active')
            true

        tabChanged: (type) ->
            console.log("MixListView: tab changed")
            $('#mix-tab a#' + type, @el).tab('show')
            true

    MixListView

