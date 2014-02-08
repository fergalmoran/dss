define ['app.lib/dssView', 'utils', 'ace-editable', 'typeahead'],
(DssView, utils) ->
    class EditableView extends DssView
        events:
            "change input": "changed"
            "change textarea": "changed"

        changeSelect: (evt) ->
            changed = evt.currentTarget
            if id
                value = $(evt.currentTarget).val()
                obj = "{\"" + changed.id + "\":\"" + value.replace(/\n/g, "<br />") + "\"}"
                objInst = JSON.parse(obj)
                @model.set objInst

        changed: (evt) ->

            #change handler for the form to update the model
            #with the new values
            return
            changed = evt.currentTarget

            #$("#" + changed.id)
            if changed.id
                value = undefined
                obj = undefined
                if $(changed).is(":checkbox")
                    value = $(changed).is(":checked")
                    obj = "{\"" + changed.id + "\":" + value + "}"
                else
                    value = $(changed).val()
                    obj = "{\"" + changed.id + "\":\"" + value.replace(/\n/g, "<br />") + "\"}"
                objInst = JSON.parse(obj)
                @model.set objInst

        _saveChanges: ->
            args = arguments
            if not @model.isValid()
                if @model.errors
                    for error of @model.errors
                        $("#group-" + error, @el).addClass "error"
                        $("#error-" + error, @el).text @model.errors[error]
            else
                @model.save null,
                    patch: args[0].patch
                    success: args[0].success
                    error: args[0].error

        setupImageEditable: (options) =>
            $.fn.editable.defaults.mode = 'inline';

            try #ie8 throws some harmless exception, so let's catch it

            #it seems that editable plugin calls appendChild, and as Image doesn't have it, it causes errors on IE at unpredicted points
            #so let's have a fake appendChild for it!
                if /msie\s*(8|7|6)/.test(navigator.userAgent.toLowerCase())
                    Image::appendChild = (el) ->
                        true

                options.el.editable
                    type: "image"
                    name: options.el.attr('id')
                    value: null
                    showbuttons: if options.showbuttons is undefined then true else options.showbuttons
                    image:
                        btn_choose: if options.chooseMessage then options.chooseMessage else "Change Avatar"
                        droppable: true
                        name: options.el.attr('id')
                        max_size: 2621440
                        on_error: (code) -> #on_error function will be called when the selected file has a problem
                            if code is 1 #file format error
                                utils.showError "File is not an image!", "Please choose a jpg|gif|png image!"
                            else if code is 2 #file size rror
                                utils.showError "File too big!", "Image size should not exceed 2.5Mb!"
                            else #other error


                    url: (params) =>
                        @uploadImage
                            el: options.el,
                            url: options.url,
                            success: (data)->
                                console.log("Image updated: " + data.url)
                                options.el.attr("src", data.url)
                                utils.showMessage("Avatar succesfully updated")

            catch e
                console.log e

        uploadImage: (options) ->
            $form = options.el.next().find(".editableform:eq(0)")
            file_input = $form.find("input[type=file]:eq(0)")

            #user iframe for older browsers that don't support file upload via FormData & Ajax
            unless "FormData" of window
                deferred = new $.Deferred
                iframe_id = "temporary-iframe-" + (new Date()).getTime() + "-" + (parseInt(Math.random() * 1000))
                $form.after "<iframe id=\"" + iframe_id + "\" name=\"" + iframe_id + "\" frameborder=\"0\" width=\"0\" height=\"0\" src=\"about:blank\" style=\"position:absolute;z-index:-1;\"></iframe>"
                $form.append "<input type=\"hidden\" name=\"temporary-iframe-id\" value=\"" + iframe_id + "\" />"
                $form.next().data "deferrer", deferred #save the deferred object to the iframe
                $form.attr
                    method: "POST"
                    enctype: "multipart/form-data"
                    target: iframe_id
                    action: options.url

                $form.get(0).submit()

                #if we don't receive the response after 60 seconds, declare it as failed!
                setTimeout (->
                    iframe = document.getElementById(iframe_id)
                    if iframe?
                        iframe.src = "about:blank"
                        $(iframe).remove()
                        deferred.reject
                            status: "fail"
                            message: "Timeout!"

                ), 60000
            else
                fd = null
                try
                    fd = new FormData($form.get(0))
                catch e

                #IE10 throws "SCRIPT5: Access is denied" exception,
                #so we need to add the key/value pairs one by one
                    fd = new FormData()
                    $.each $form.serializeArray(), (index, item) ->
                        fd.append item.name, item.value


                    #and then add files because files are not included in serializeArray()'s result
                    $form.find("input[type=file]").each ->
                        fd.append @getAttribute("name"), @files[0]  if @files.length > 0


                #if file has been drag&dropped , append it to FormData
                if file_input.data("ace_input_method") is "drop"
                    files = file_input.data("ace_input_files")
                    fd.append file_input.attr("name"), files[0]  if files and files.length > 0
                deferred = $.ajax(
                    url: options.url
                    type: "POST"
                    processData: false
                    contentType: false
                    dataType: "json"
                    data: fd
                    xhr: ->
                        req = $.ajaxSettings.xhr()
                        req

                    beforeSend: ->
                        success: ->
                )

            deferred.done((res) ->
                if res.status is "OK"
                    options.success(res)
                else
                    utils.showError res.message
            ).fail (res) ->
                utils.showError "Failure"

            deferred.promise()

    EditableView