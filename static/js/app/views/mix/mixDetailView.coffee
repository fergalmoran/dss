define ['marionette', 'models/mix/mixItem', 'views/mix/mixItemView', 'text!/tpl/MixDetailView'],
(Marionette, MixItem, MixItemView, Template) ->
    class  MixDetailView extends Marionette.Layout

        template: _.template(Template)
        regions:{
            mix: "#mix"
            comments: "#comments"
        }

        onRender: ->
            view = new MixItemView({tagName: "div", className: "mix-listing audio-listing-single", model: @model})
            @mix.show(view)
            view.renderComments()
            true

    MixDetailView
