define ['marionette', 'vent', 'app.lib/controller'],
(Marionette, vent, Controller) ->
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

            "chat": "showChat",

            "users": "showUserList"
            "user/:slug/favourites": "showUserFavourites"
            "user/:slug/likes": "showUserLikes"
            "user/:slug/followers": "showUserFollowers"
            "user/:slug/following": "showUserFollowing"
            "user/:slug/mixes": "showUserMixes"
            "user/:slug": "showUserProfile"
            "me": "editUser"

        initialize: ->
            console.log "Router: initialize"
            @listenTo vent, "navigate:mix", (slug)->
                @navigate 'mix/' + slug, true
