@Dss = do(Backbone, Marionette) ->

    App = new Marionette.Application


    App.addRegions
        headerRegion: "#header"
        contentRegion: "#content"
        footerRegion: "#footer"
        sidebarRegion: "#sidebar"

    App.addInitializer ->
        @audioController = new App.Lib.AudioController()
        App.Router = new App.Lib.Router()

    App.addInitializer ->
        @headerRegion.show(new App.HeaderApp.Views.Header())

    App.addInitializer ->
        $(document).on("click", "a[href]:not([data-bypass])", (evt) ->
            href = { prop: $(this).prop("href"), attr: $(this).attr("href") }
            root = location.protocol + "//" + location.host + (App.root || '/')
            if (href.prop.slice(0, root.length) == root)
                evt.preventDefault()
                App.Router.navigate(href.attr, true)
                true
        )
        true

    App.addInitializer ->
        @listenTo @vent, "app:login", ->
            console.log "App(vent): app:login"
            utils.modal "/dlg/LoginView"
            true

        @listenTo @vent, "app:donate", ->
            console.log("App: donate")
            utils.modal "/dlg/Donate"
            true

        @listenTo @vent, "mix:favourite", (model) ->
            console.log "App(vent): mix:favourite"
            model.save 'favourited', !model.get('favourited'), patch: true
            true

        @listenTo @vent, "mix:like", (model, id, success, favourite) ->
            console.log "App(vent): mix:like"
            model.save 'liked', !model.get('liked'), patch: true
            true

        @listenTo @vent, "mix:delete", (model) ->
            console.log "App(vent): mix:like"
            utils.messageBox "/dlg/DeleteMixConfirm"
              yes: ->
                console.log("Controller: mixDeleteYES!!")
                mix.destroy()
                Backbone.history.navigate "/", trigger: true
              no: ->
                console.log("Controller: mixDeleteNO!!")

        @listenTo @vent, "user:follow", (model)->
            console.log "App(vent): user:follow"
            user = new UserItem({id: com.podnoms.settings.currentUser })
            target = com.podnoms.settings.urlRoot + "user/" + model.get("id") + "/"
            user.fetch(
                success: =>
                    if not model.get("is_following")
                        newFollowers = user.get("following").concat([target])
                        user.save(
                            "following": newFollowers
                            "is_following": true
                            ,
                            patch: true
                        )
                        model.set("is_following", true)
                    else
                        f = user.get("following")
                        f.splice(f.indexOf(target), 1)
                        user.save(
                            "following": f
                            "is_following": false
                            ,
                            patch: true
                        )
                        model.set("is_following", false)

                    return
            )

            true

        @listenTo @vent, "mix:share", (mode, model) ->
            console.log "App(vent): mix:share (" + mode + ")"
            if (mode == "facebook")
                social.sharePageToFacebook(model)
            else if (mode == "twitter")
                social.sharePageToTwitter(model)
            else if (mode == "embed")
                social.generateEmbedCode(model)

            true

    App.on "initialize:after", ->
        if Backbone.history
            Backbone.history.start()

    App