/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
postFacebookLike = function (mixId) {
    //first off, find if the current user has allowed facebook likes
    $.getJSON(
        'ajax/facebook_post_likes_allowed/',
        function (data) {
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
        }
    );
};

postFacebookFavourite = function(mixId){

};

sharePageToFacebook = function(model){
    var obj = {
        method: 'feed',
        link: 'http://' + window.location.host  + "/" + model.get('item_url'),
        picture: model.get('mix_image'),
        name: 'Check out this mix on Deep South Sounds',
        caption: model.get('title'),
        description: model.get('description')
    };
    function callback(response) {
        com.podnoms.utils.alert("Post ID: " + response['post_id']);
    }
    FB.ui(obj, callback);
};