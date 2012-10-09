/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
postFacebookLike = function (mixId) {
    //first off, find if the current user has allowed facebook likes
    $.getJSON(
        'social/like/' + mixId + '/',
        function (data) {
            com.podnoms.utils.showAlert("Posted your like to facebook, you can stop this in your settings page.", "Cheers feen", "alert-success", true);
            /*
            if (data.value) {
                FB.api(
                    '/me/deepsouthsounds:like',
                    'post',
                    { mix:'http://' + window.location.host + '/social/redirect/mix/' + mixId},
                    function (response) {
                        if (!response || response.error) {
                            com.podnoms.utils.showAlert(response.error.message, 'Error occurred: ', "alert-error", true);
                        } else {
                            com.podnoms.utils.showAlert("Posted your like to facebook, you can stop this in your settings page.", "Cheers feen", "alert-success", true);
                        }
                    }
                );
            }
            */
        }
    );
};

postFacebookFavourite = function (mixId) {

};

sharePageToTwitter = function (model) {
//We get the URL of the link
    var loc = $(this).attr('href');

//We get the title of the link
    var title = $(this).attr('title');

//We trigger a new window with the Twitter dialog, in the middle of the page
    window.open(
        'http://twitter.com/share?url=' + 'http://' + window.location.host + "/" + model.get('item_url') +
        '&amp;text=' + model.get('title'),
        'twitterwindow',
        'height=450, width=550, top=' + ($(window).height() / 2 - 225) +
        ', left=' + $(window).width() / 2 +
        ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');
};
sharePageToFacebook = function (model) {
    var obj = {
        method:'feed',
        link:'http://' + window.location.host + "/" + model.get('item_url'),
        picture:model.get('mix_image'),
        name:'Check out this mix on Deep South Sounds',
        caption:model.get('title'),
        description:model.get('description')
    };

    function callback(response) {
        com.podnoms.utils.alert("Post ID: " + response['post_id']);
    }

    FB.ui(obj, callback);
};