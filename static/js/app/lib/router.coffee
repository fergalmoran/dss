define ['marionette', 'app.lib/controller'],
(Marionette, Controller) ->
    class DssRouter extends Marionette.AppRouter
        controller: new Controller,
        appRoutes:
            "": "home",
            "/": "home",

            "mix/upload": "uploadMix",
            "mixes": "showMixList",
            "mixes/:type": "showMixList"
            "mix/:slug": "showMix"
            "mix/edit/:slug": "editMix",

            "users": "showUserList"
            "user/:slug/favourites": "showUserFavourites"
            "user/:slug/likes": "showUserLikes"
            "user/:slug/followers": "showUserFollowers"
            "user/:slug/following": "showUserFollowing"
            "user/:slug": "showUserDetail"
            "me": "editUser"



