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
                    $(data).proceed().on "hidden", ->
                        alert("Go on so")
                        true
                ).success ->
                    $("input:text:visible:first").focus()
                    true
        true

    secondsToHms: (d)  ->
        if d
            d = Number(d)
            h = Math.floor(d / 3600)
            m = Math.floor(d % 3600 / 60)
            s = Math.floor(d % 3600 % 60)
            ((if h > 0 then h + ":" else "")) + ((if m > 0 then ((if h > 0 and m < 10 then "0" else "")) + m + ":" else "00:")) + ((if s < 10 then "0" else "")) + s
        else
            "00:00:00"

    messageBox: (url, success) ->
        if url
            if url.indexOf("#") is 0
                $(url).modal "open"
            else
                $.get(url,(data) ->
                    $(data).modal('show').on("shown.bs.modal", (e) ->
                        $(this).find("#yes-no-positive").click ->
                            success()
                    )
                )

        true

    checkPlayCount: ->
        if document.cookie.indexOf("sessionId")
            $.getJSON "/ajax/session_play_count", (data) =>
                console.log "utils: got playcount"
                if data.play_count isnt "0" and ((data.play_count % com.podnoms.settings.nag_count) == 0)
                    @modal "/dlg/PlayCountLoginAlert"
        true

    toastOptions: ->
        toastr.options =
          closeButton: true
          debug: false
          positionClass: "toast-bottom-left"
          onclick: null
          showDuration: "300"
          hideDuration: "1000"
          timeOut: "5000"
          extendedTimeOut: "1000"
          showEasing: "swing"
          hideEasing: "linear"
          showMethod: "fadeIn"
          hideMethod: "fadeOut"

    showError: (title, message) ->
        @toastOptions()
        toastr.error message, title

    showWarning: (title, message) ->
        @toastOptions()
        toastr.warning message, title

    showMessage: (title, message) ->
        @toastOptions()
        toastr.success message, title

    showAlert: (title, message) ->
        @showMessage title, message

    generateGuid: ->
        "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace /[xy]/g, (c) ->
            r = Math.random() * 16 | 0
            v = (if c is "x" then r else (r & 0x3 | 0x8))
            v.toString 16

    downloadURL: (url) ->
        iframe = document.getElementById("hiddenDownloader")
        if iframe is null
            iframe = document.createElement("iframe")
            iframe.id = "hiddenDownloader"
            iframe.style.visibility = "hidden"
            document.body.appendChild iframe
        iframe.src = url
        true

    isMe: (id) ->
        id == com.podnoms.settings.currentUser
