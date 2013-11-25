define ['marionette',
        'models/mix/mixItem',
        'models/comment/commentItem',
        'views/mix/mixItemView',
        'text!/tpl/MixDetailView',
        'vent'],
(Marionette,
 MixItem,
 CommentItem,
 MixItemView,
 Template,
 vent) ->
    class  MixDetailView extends Marionette.Layout

        template: _.template(Template)
        regions:{
            mix: "#mix"
            comments: "#comments"
        }
        ui:
            commentText: '#comment-text'
        events:
            "click #btn-add-comment": "addComment"


        addComment: ->
          comment = "123"

        onRender: ->
            view = new MixItemView({tagName: "div", className: "mix-listing audio-listing-single", model: @model})
            @mix.show(view)
            true

    MixDetailView
