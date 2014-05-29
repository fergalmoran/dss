@utils = do ->
    getCookie: (name) ->
        cookieValue = null
        if document.cookie and document.cookie isnt ""
            cookies = document.cookie.split(";")
            i = 0

            while i < cookies.length
                cookie = jQuery.trim(cookies[i])

                # Does this cookie string begin with the name we want?
                if cookie.substring(0, name.length + 1) is (name + "=")
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
                i++
        cookieValue

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

    isAuth: ->
        com.podnoms.settings.currentUser != -1

    isMe: (id) ->
        id == com.podnoms.settings.currentUser

$(document).ready ->
    window.location.hash = ""  if window.location.hash is "#_=_"
    Backbone.history.navigate "/"  if window.location.hash is "upload#"
    unless Array::indexOf
        console.log "Shimming indexOf for IE8"
        Array::indexOf = (searchElement) -> #, fromIndex
            "use strict"
            throw new TypeError()  unless this?
            n = undefined
            k = undefined
            t = Object(this)
            len = t.length >>> 0
            return -1  if len is 0
            n = 0
            if arguments_.length > 1
                n = Number(arguments_[1])
                unless n is n # shortcut for verifying if it's NaN
                    n = 0
                else n = (n > 0 or -1) * Math.floor(Math.abs(n))  if n isnt 0 and n isnt Infinity and n isnt -Infinity
            return -1  if n >= len
            k = (if n >= 0 then n else Math.max(len - Math.abs(n), 0))
            while k < len
                return k  if k of t and t[k] is searchElement
                k++
            -1
    return

$(document).ajaxSend (event, xhr, settings) ->
    getCookie = (name) ->
        cookieValue = null
        if document.cookie and document.cookie isnt ""
            cookies = document.cookie.split(";")
            i = 0

            while i < cookies.length
                cookie = jQuery.trim(cookies[i])

                # Does this cookie string begin with the name we want?
                if cookie.substring(0, name.length + 1) is (name + "=")
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
                i++
        cookieValue
    sameOrigin = (url) ->

        # url could be relative or scheme relative or absolute
        host = document.location.host # host + port
        protocol = document.location.protocol
        sr_origin = "//" + host
        origin = protocol + sr_origin

        # Allow absolute or scheme relative URLs to same origin

        # or any other URL that isn't scheme relative or absolute i.e relative.
        (url is origin or url.slice(0, origin.length + 1) is origin + "/") or (url is sr_origin or url.slice(0,
                sr_origin.length + 1) is sr_origin + "/") or not (/^(\/\/|http:|https:).*/.test(url))
    safeMethod = (method) ->
        /^(GET|HEAD|OPTIONS|TRACE)$/.test method
    xhr.setRequestHeader "X-CSRFToken", getCookie("csrftoken")  if typeof (xhr.setRequestHeader) is typeof (Function)  if not safeMethod(settings.type) and sameOrigin(settings.url)
    return

$.ajaxSetup
    beforeSend: (xhr, settings) ->

        # Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader "X-CSRFToken", utils.getCookie("csrftoken")  unless /^http:.*/.test(settings.url) or /^https:.*/.test(settings.url)
        return

    statusCode:
        401: ->
            vent.trigger "app:login"
            window.location.replace "/"
            return

        403: ->
            vent.trigger "app:denied"
            window.location.replace "/"
            return

unless com.podnoms.settings.isDebug

    #console.log("Looking under the hood? Check us out on github https://github.com/fergalmoran/dss");
    console = {}
    console.log = (message) ->