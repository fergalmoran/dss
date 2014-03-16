define ['jquery', 'utils', 'facebook'], ($, utils) ->
    postFacebookLike: (mixId) ->

        #first off, find if the current user has allowed facebook likes
        $.getJSON "social/like/" + mixId + "/", (data) ->
            com.podnoms.utils.showAlert "Posted your like to facebook, you can stop this in your settings page.", "Cheers feen"


    generateEmbedCode: (model) ->
        console.log("Generating embed code");
        utils.modal "/dlg/embed/" + model.get('slug')

    sharePageToTwitter: (model) ->

        #We get the URL of the link
        loc = $(this).attr("href")

        #We get the title of the link
        title = $(this).attr("title")

        #We trigger a new window with the Twitter dialog, in the middle of the page
        window.open "http://twitter.com/share?url=" + "http://" + window.location.host + "/" + model.get("item_url") + "&amp;text=" + model.get("title"), "twitterwindow", "height=450, width=550, top=" + ($(window).height() / 2 - 225) + ", left=" + $(window).width() / 2 + ", toolbar=0, location=0, menubar=0, directories=0, scrollbars=0"

    sharePageToFacebook: (model) ->
        FB.init({
            appId : '154504534677009',
            xfbml : true
        });
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

