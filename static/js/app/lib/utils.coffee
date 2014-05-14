define ['jquery', 'lib/jquery.filedownload', 'bootstrap', 'toastr'],
  ($, filedownload, bootstrap, toastr) ->
    modal: (url) ->
        return if $('#modal-header').length
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
            $.getJSON "/ajax/session_play_count/", (data) =>
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
        """
        $.getJSON url, (data) =>
            $.fileDownload(data.url)
            successCallback: (url) ->
                alert "You just got a file download dialog or ribbon for this URL :" + url
                return

            failCallback: (html, url) ->
                alert "Your file download just failed for this URL:" + url + "\r\n" + "Here was the resulting error HTML: \r\n" + html
                return
        """
        iframe = document.getElementById("if_dl_misecure")
        if iframe is null
            iframe = document.createElement("iframe")
            iframe.id = "if_dl_misecure"
            iframe.style.visibility = "hidden"
            document.body.appendChild iframe
        iframe.src = url
        true
    isMe: (id) ->
        id == com.podnoms.settings.currentUser
