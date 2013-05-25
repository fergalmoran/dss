define ['marionette', 'app.lib/controller'],
(Marionette, Controller) ->
    class DssRouter extends Marionette.AppRouter
        controller: new Controller,
        appRoutes:
            "": "home",
            "/": "home",

            "mixes": "showMixList",
            "mixes/:type": "showMixList"
            "mix/:slug": "showMix"
            "mix/edit/:slug": "editMix",

            "user/:slug": "user"



