define['jquery', 'bootstrap']
($, bootstrap) ->
    class Utils

        modal: (url) ->
            if url.indexOf("#") is 0
                $(url).modal "open"
            else
                $.get(url,(data) ->
                    $("<div class=\"modal hide fade\">" + data + "</div>").modal().on "hidden", ->
                        $(this).remove()

                ).success ->
                    $("input:text:visible:first").focus()
            true
        checkPlayCount: ->
            if document.cookie.indexOf("sessionId")
                $.getJSON "/ajax/session_play_count", (data) ->
                    com.podnoms.utils.modal "tpl/PlayCountLoginAlert"  if (data.play_count isnt 0) and (data.play_count % 1) is 0
            true

        Utils

