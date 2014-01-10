define ['marionette',
        'utils',
        'models/mix/mixItem',
        'models/comment/commentItem',
        'models/comment/commentCollection',
        'views/comment/commentListView',
        'views/mix/mixItemView',
        'text!/tpl/MixDetailView',
        'vent'],
(Marionette, utils, MixItem, CommentItem, CommentsCollection, CommentsListView, MixItemView, Template, vent) ->
    class  MixDetailView extends Marionette.Layout

        template: _.template(Template)
        regions:
            mix: "#mix"
            comments: "#comments"
        ui:
            commentText: '#comment-text'
        events:
            "click #btn-add-comment": "addComment"
            "keypress #comment-text": "checkCommentKeypress"

        initialize: ->
            @model.on('nested-change', @modelChanged)

        onRender: ->
            view = new MixItemView({tagName: "div", className: "mix-listing audio-listing-single", model: @model})
            @mix.show view
            @renderComments()

        renderComments: ->
            console.log "MixDetailView: Rendering comments"
            comments = new CommentsCollection()
            comments.url = @model.get("resource_uri") + "/comments/"
            comments.mix_id = @model.id
            comments.mix = @model
            comments.fetch success: (data) ->
                content = new CommentsListView(collection: comments).render()
                $("#comments", @el).html content.el
                true
            true

        modelChanged: =>
            console.log("MixDetailView: modelChanged")
            @render()
            true

        checkCommentKeypress: (e) ->
            if e.which is 13
                @addComment()

        addComment: ->
            activeTab = $("ul#mix-tab li.active", @el)
            comment = @ui.commentText.val()
            @model.addComment comment, (=>
                @ui.commentText.val ""
                utils.showMessage "Comment saved.."
                activeTab.tab().show()
            ), (error) =>
                utils.showError "Woops \n" + error
                $('#comment-input').addClass('has-error')
                $('#comment-text').focus()

            MixDetailView
