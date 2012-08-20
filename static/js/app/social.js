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
                            window.utils.showAlert(response.error.message, 'Error occurred: ', "alert-error", true);
                        } else {
                            window.utils.showAlert("Posted your like to facebook, you can stop this in your settings page.", "Cheers feen", "alert-success", true);
                        }
                    }
                );
            }
        }
    );
}

postFacebookFavourite = function(mixId){

}