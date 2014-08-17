@Dss.module "Lib", (Lib, App, Backbone, Marionette, $    ) ->
    class Lib.Router extends Marionette.AppRouter
        controller: new Lib.Controller,
        appRoutes:
            "": "home",
            "/": "home",

            "mix/upload": "uploadMix",
            "mixes": "showMixList",
            "mixes/:type": "showMixListType"
            "mixes/genre/:type": "showMixListGenre"
            "mix/:slug": "showMix"
            "mix/edit/:slug": "editMix",

            "chat": "showChat",
            "random": "showRandomMix",
            "stream": "showStreamList",
            "schedule": "showSchedule",

            "login": "doLogin"
            "logout": "doLogout"

            "users": "showUserList"
            "user/:slug/favourites": "showUserFavourites"
            "user/:slug/likes": "showUserLikes"
            "user/:slug/followers": "showUserFollowers"
            "user/:slug/following": "showUserFollowing"
            "user/:slug/mixes": "showUserMixes"
            #"user/:slug/playlists": "showUserPlaylists"
            "user/:slug": "showUserProfile"
            "me": "editUser"

            "playlist/:slug": "showPlaylist"

        initialize: ->
            console.log "Router: initialize"
            @listenTo App.vent, "navigate:mix", (slug)->
                @navigate 'mix/' + slug, true

    Lib.Router