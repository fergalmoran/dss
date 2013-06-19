define ['jquery', 'bootstrap', 'toastr'], ($, bootstrap, toastr) ->
    modal: (url) ->
        if url
            if url.indexOf("#") is 0
                $(url).modal "open"
            else
                $.get(url,(data) ->
                    $(data).modal().on "hidden", ->
                        $(this).remove()
                        true
                ).success ->
                    $("input:text:visible:first").focus()
                    true
        true

    checkPlayCount: ->
        if document.cookie.indexOf("sessionId")
            $.getJSON "/ajax/session_play_count", (data) =>
                console.log "utils: got playcount"
                @modal "dlg/PlayCountLoginAlert"  if (data.play_count isnt 0) and (data.play_count % com.podnoms.settings.nag_count) is 0
        true

    showError: (title, message) =>
        toastr.error message, title

    showWarning: (title, message) =>
        toastr.warning message, title

    showAlert: (title, message) =>
        toastr.success message, title

    generateGuid: ->
      "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace /[xy]/g, (c) ->
        r = Math.random() * 16 | 0
        v = (if c is "x" then r else (r & 0x3 | 0x8))
        v.toString 16
