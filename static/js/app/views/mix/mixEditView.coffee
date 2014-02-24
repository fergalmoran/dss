define ['app.lib/editableView',
        'vent', 'moment', 'utils', 'backbone.syphon', 'text!/tpl/MixEditView'
        'models/genre/genreCollection', 'lib/jdataview',
        'ace', 'dropzone', 'wizard', 'ajaxfileupload','jquery.fileupload', 'lib/ace/uncompressed/select2'],
(EditableView, vent, moment, utils, Syphon, Template, GenreCollection, jDataView) ->
    class MixEditView extends EditableView
        @func = null

        template: _.template(Template)
        events:
            "click #login": "login"
            "change input[name='...']": "imageChanged"
        ui:
            image: "#mix-image"
            progress: "#mix-upload-progress"
            uploadError: '#mix-upload-error'

        initialize: ->
            @guid = utils.generateGuid()
            @uploadState = -1
            @detailsEntered = false
            @patch = false

        onRender: ->
            console.log("MixEditView: onRender js")
            $('.progress', @el).hide()
            @sendImage = false

            if not @model.id
                $('input[name="upload-hash"]', @el).val(@guid)
            else
                $('#header-step1', @el).remove()
                $('#step1', @el).remove()

                $('#header-step2', @el).addClass("active")
                $('#step2', @el).addClass("active")

                $('.progress', @el).hide()

                @patch = true
                @uploadState = 2

            wizard = $("#fuelux-wizard", @el).ace_wizard().on("change",(e, info) =>
                if info.step is 1 and @uploadState is 0
                    console.log "MixEditView: No mix uploaded"
                    @ui.uploadError.text("Please add a mix")
                    @ui.uploadError.fadeIn()
                    false
                else if @uploadState > 0
                    true
                else
                    $('#step1').addClass("alert-danger")
                    false
            ).on("finished", (e) =>
                console.log("Finished")
                @saveChanges()
            )

            $("#mix-upload-form", @el).dropzone
                addRemoveLinks: true

                dictDefaultMessage: "<span class=\"bigger-150 bolder\"><i class=\"icon-caret-right red\"></i> Drop files</span> to upload \t\t\t\t<span class=\"smaller-80 grey\">(or click)</span> <br /> \t\t\t\t<i class=\"fa fa-cloud-upload fa-5x blue\"></i>"

                maxFilesize: 512

                sending: =>
                    $('.progress', @el).show()
                    @uploadState = 1

                uploadprogress: (e, progress, bytesSent) =>
                    $('.progress', @el).show()
                    percentage = Math.round(progress)
                    @ui.progress.css("width", percentage + "%").parent().attr "data-percent", percentage + "%"

                complete: (file)=>
                    if file.status != "error"
                        @uploadState = 2
                        @checkRedirect()

            $("#genres", @el).select2
                placeholder: "Start typing and choose from list or create your own."
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

                formatResult: (genre) ->
                    genre.description

                formatSelection: (genre) ->
                    "<div class='select2-user-result'>" + genre.description + "</div>"

                initSelection: (element, callback) =>
                    console.log("MixEditView: genres:initSelection")
                    result = []
                    genres = @model.get("genres")
                    unless genres is `undefined`
                        genres.each (data) ->
                            result.push
                                id: data.get("id")
                                description: data.get("description")
                    callback result

                """
                createSearchChoice: (term, data) ->
                    if $(data).filter(->
                        @description.localeCompare(term) is 0
                    ).length is 0
                        id: term
                        text: term
                """

            true

        saveChanges: =>
            console.log("MixEditView: saveChanges")
            @model.set Syphon.serialize($("#mix-details-form", @el)[0])
            flair = Syphon.serialize $("#mix-flair-form", @el)[0],
                exclude: ["...", ""]

            @model.set flair

            @model.set "upload-hash", @guid
            @model.set "upload-extension", $("#upload-extension", @el).val()

            @model.set("genres", new GenreCollection())
            $.each $("#genres", @el).select2("data"), (i, item) =>
                """
                if @model.get("genres") is undefined
                    @model.set("genres", new GenreCollection())
                """
                @model.get("genres").add({id: item.id, description: item.text});

            @model.unset "mix_image" unless @sendImage
            @model.unset "comments"

            @_saveChanges
                patch: @patch
                success: =>
                    if @sendImage
                        $.ajaxFileUpload
                            url: "/ajax/upload_mix_image/" + @model.get("id") + "/"
                            secureuri: false
                            fileElementId: "input[name='...']"
                            success: (data, status) =>
                                unless typeof (data.error) is "undefined"
                                    unless data.error is ""
                                        alert data.error
                                    else
                                        alert data.msg
                                else
                                    $("#mix-upload-wizard", @el).hide()
                                    @detailsEntered = true
                                    @checkRedirect()

                            error: (data, status, e) ->
                                utils.showError e
                    else
                        $("#mix-upload-wizard", @el).hide()
                        @detailsEntered = true
                        @checkRedirect()
                    true
                error: (model, response) ->
                    utils.showError "Error", "Something went wrong<br />Nerd stuff is: " + response

            false

        checkRedirect: ->
            if @detailsEntered and @uploadState is 2
                Backbone.history.navigate "/mix/" + @model.get("slug"),
                    trigger: true

        login: ->
            vent.trigger('app:login')

        imageChanged: (evt) ->
            @sendImage = true


        MixEditView
