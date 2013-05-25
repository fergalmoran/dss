define ["marionette"],
(Marionette) ->
    class EditableView extends Marionette.ItemView
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

        _bakeForm: (el, lookups) ->

            #TODO extend lookups to be a list
            #TODO this way we can initialise more than one lookup per page
            model = @model
            labels = undefined
            mapped = undefined
            $(".typeahead", el).typeahead
                source: (query, process) ->
                    $.get "/ajax/lookup/" + lookups + "/",
                        query: query
                    , ((data) ->
                            labels = []
                            mapped = {}
                            $.each data, (i, item) ->
                                mapped[item[1]] = item
                                labels.push item[1]

                            process labels
                        ), "json"

                updater: (item) ->
                    @$element.val mapped[item][0]
                    model.set @$element.attr("id"), mapped[item][0]
                    item

            $(".datepicker", el).datepicker format: "dd/mm/yyyy"
            $(".timepicker", el).timepicker()
            $("textarea.tinymce", @el).tinymce
                script_url: "/static/js/libs/tiny_mce/tiny_mce.js"
                mode: "textareas"
                theme: "advanced"
                theme_advanced_toolbar_location: "top"
                theme_advanced_toolbar_align: "left"
                theme_advanced_buttons1: "fullscreen,media,tablecontrols,separator,link,unlink,anchor,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,image,cleanup,help,separator,code"
                theme_advanced_buttons2: ""
                theme_advanced_buttons3: ""
                auto_cleanup_word: true
                plugins: "media, table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,print,contextmenu,fullscreen,preview,searchreplace"
                plugin_insertdate_dateFormat: "%m/%d/%Y"
                plugin_insertdate_timeFormat: "%H:%M:%S"
                extended_valid_elements: "a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]"
                fullscreen_settings:
                    theme_advanced_path_location: "top"
                    theme_advanced_buttons1: "fullscreen,media, separator,preview,separator,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help"
                    theme_advanced_buttons2: "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor"
                    theme_advanced_buttons3: "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"


        _saveChanges: ->
            args = arguments
            if not @model.isValid()
                if @model.errors
                    for error of @model.errors
                        $("#group-" + error, @el).addClass "error"
                        $("#error-" + error, @el).text @model.errors[error]
            else
                @model.save null,
                    success: args[0].success
                    error: args[0].error


    EditableView