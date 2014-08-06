@Dss.module "MixApp.Views", (Views, App, Backbone, Marionette, $) ->
    class Views.MixDetailView extends Marionette.LayoutView
        template: "mixdetailview"
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
            @view = new Views.MixItemView({tagName: "div", className: "mix-listing audio-listing-single", model: @model})
            @mix.show @view
            @renderComments()
            window.scrollTo 0, 0

        onDomRefresh: ->
            @view.onDomRefresh()

        renderComments: ->
            console.log "MixDetailView: Rendering comments"
            comments = new App.CommentsApp.Models.CommentCollection()
            comments.url = @model.get("resource_uri") + "/comments/"
            comments.mix_id = @model.id
            comments.mix = @model
            comments.fetch success: (data) ->
                content = new App.CommentsApp.Views.CommentListView(collection: comments).render()
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

    Views.MixDetailView
