@social = do ->
    postFacebookLike: (mixId) ->

        #first off, find if the current user has allowed facebook likes
        $.getJSON "social/like/" + mixId + "/", (data) ->
            utils.showAlert "Posted your like to facebook, you can stop this in your settings page.", "Cheers feen"


    generateEmbedCode: (model) ->
        console.log("Generating embed code");
        utils.modal "/dlg/embed/" + model.get('slug')

    sharePageToTwitter: (model) ->
        title = $(this).attr("title")
        url = "http://" + window.location.host + model.get("item_url")
        text = model.get("title")
        window.open "http://twitter.com/share?url=#{url}&amp;text={#text}", "twitterwindow", "height=450, width=550, top=" + ($(window).height() / 2 - 225) + ", left=" + $(window).width() / 2 + ", toolbar=0, location=0, menubar=0, directories=0, scrollbars=0"

    sharePlaylistToTwitter: (model) ->
        url = "http://" + window.location.host + model.get("item_url")
        text = model.get("name")
        window.open "http://twitter.com/share?url=#{url}&amp;text={#text}", "twitterwindow", "height=450, width=550, top=" + ($(window).height() / 2 - 225) + ", left=" + $(window).width() / 2 + ", toolbar=0, location=0, menubar=0, directories=0, scrollbars=0"

    _initFacebook: ->
        FB.init({
            appId : '154504534677009',
            xfbml : true
        });

    sharePageToFacebook: (model) ->
        @_initFacebook()

        FB.getLoginStatus (oResponse) ->
            if oResponse.status is "connected"
                FB.ui
                    method: "feed"
                    name: "Check out this mix on Deep South Sounds"
                    display: "iframe"
                    link: "http://" + window.location.host + "/" + model.get("item_url")
                    picture: model.get("mix_image")
                    caption: model.get("title")
                    description: model.get("description")
                , (response) ->
                    if response and response.post_id
                        utils.showAlert "Success", "Post shared to facebook"
            else
                utils.showError "Error", "Failure sharing post"

    sharePlaylistToFacebook: (model) ->
        @_initFacebook()
        FB.getLoginStatus (oResponse) ->
            if oResponse.status is "connected"
                FB.ui
                    method: "feed"
                    name: "Check out this playlist on Deep South Sounds"
                    display: "iframe"
                    link: "http://" + window.location.host + "/" + model.get("item_url")
                    picture: model.get("playlist_image")
                    caption: model.get("name")
                    description: model.get("name")
                , (response) ->
                    if response and response.post_id
                        utils.showAlert "Success", "Post shared to facebook"
            else
                utils.showError "Error", "Failure sharing post"
