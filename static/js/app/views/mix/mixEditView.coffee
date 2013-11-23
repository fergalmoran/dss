define ['app.lib/editableView', 'moment', 'utils', 'backbone.syphon', 'text!/tpl/MixEditView'
        'jquery.fileupload', 'jquery.fileupload-process', 'jquery.fileupload-audio', 'jquery.fileupload-ui',
            'jquery.iframe-transport', 'jquery.ui.widget', 'lib/bootstrap-fileupload',
        'lib/select2', 'lib/ajaxfileupload', 'ace', 'lib/bootstrap-tag.min'],
(EditableView, moment, utils, Syphon, Template) ->
    class MixEditView extends EditableView
        template: _.template(Template)
        events:
            "click #save-changes": "saveChanges"
            "change #mix_image": "imageChanged"
        ui:
            image: "#mix-image"

        @working = false
        @patch = false
        checkRedirect: ->
            if @state is 2
                Backbone.history.navigate "/mix/" + @model.get("slug"),
                    trigger: true

        initialize: ->
            @guid = utils.generateGuid()
            @state = 0

        onDomRefresh: ->
            $("#fileupload", @el).fileupload
                downloadTemplateId: undefined
                url: "/_upload/"
                start: ->
                    $("#mix-details", @el).show()
                done: =>
                    @state++;
                    $("#div-upload-mix", @el).hide()
                    @checkRedirect()

            @setupImageEditable
                el: @ui.image
                showbuttons: false
                chooseMessage: "Choose mix image"

            $("#mix-imageupload", @el).jas_fileupload uploadtype: "image"
            true

        onRender: ->
            console.log("MixEditView: onRender")
            @sendImage = false
            parent = this
            if not @model.id
                $("#upload-hash", @el).val @guid
            else
                $("#div-upload-mix", @el).hide()
                @patch = true
                @state = 1

            $("#genres", @el).select2
                placeholder: "Start typing and choose or press enter"
                minimumInputLength: 1
                multiple: true
                ajax: # instead of writing the function to execute the request we use Select2's convenient helper
                    url: "/ajax/lookup/genre/"
                    dataType: "json"
                    data: (term, page) ->
                        q: term

                    results: (data, page) -> # parse the results into the format expected by Select2.
                        # since we are using custom formatting functions we do not need to alter remote JSON data
                        results: data

                initSelection: (element, callback) ->
                    console.log("MixEditView: genres:initSelection")
                    result = []
                    genres = parent.model.get("genre-list")
                    unless genres is `undefined`
                        $.each genres, (data) ->
                            result.push
                                id: @id
                                text: @text


                    callback result

                createSearchChoice: (term, data) ->
                    if $(data).filter(->
                        @text.localeCompare(term) is 0
                    ).length is 0
                        id: term
                        text: term

            this

        saveChanges: =>
            console.log("MixEditView: saveChanges")
            data = Syphon.serialize($("#mix-details-form", @el)[0])
            @model.set data
            @model.set "upload-hash", @guid
            @model.set "upload-extension", $("#upload-extension", @el).val()
            @model.set "genre-list", $("#genres", @el).select2("data")
            @model.unset "mix_image" unless @sendImage
            @model.unset "comments"

            @_saveChanges
                patch: @patch
                success: =>
                    if @sendImage
                        $.ajaxFileUpload
                            url: "/ajax/upload_mix_image/" + @model.get("id") + "/"
                            secureuri: false
                            fileElementId: "mix_image"
                            success: (data, status) =>
                                unless typeof (data.error) is "undefined"
                                    unless data.error is ""
                                        alert data.error
                                    else
                                        alert data.msg
                                else
                                    $("#mix-details", @el).hide()
                                    @state++
                                    @checkRedirect()

                            error: (data, status, e) ->
                                utils.showError e
                    else
                        $("#mix-details", @el).hide()
                        @state++
                        @checkRedirect()
                    true
                error: (model, response) ->
                    utils.showError "Error", "Something went wrong<br />Nerd stuff is: " + response

            false

        imageChanged: (evt) ->
            @sendImage = true
            true

        MixEditView