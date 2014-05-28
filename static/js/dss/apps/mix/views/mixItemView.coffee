@Dss.module "MixApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.MixItemView extends Marionette.ItemView
        template: "mixitemview"
        tagName: @tagName or "li"
        className: @className or ""

        events: {
            "click .play": "mixPlay",
            "click .pause": "mixPause",
            "click .resume": "mixResume",

            "click .mix-link": "mixLink",
            "click .delete-button a": "mixDelete",
            "click .like-button a": "mixLike",
            "click .favourite-button a": "mixFavourite",
            "click .share-button": "mixShare",
            "click .download-button a": "mixDownload"
            "click .login-download-button  a": "login"
        }

        ui: {
            playButton: ".mix-state-toggle",
            playButtonIcon: ".mix-state-toggle i",
            playerEl: ".pnp-instance"
        }

        initialize: =>
            @mixState = 0

            @listenTo(@model, 'change:favourited', @render)
            @listenTo(@model, 'change:liked', @render)
            @listenTo(@model, 'nested-change', @render)
            @listenTo(App.vent, 'mix:init', @onMixInit)
            @listenTo(App.vent, 'mix:stop', @onMixStop)
            @listenTo(App.vent, 'mix:resume', @onMixStateChanged)
            @listenTo(App.vent, 'mix:pause', @onMixStateChanged)

            true

        onRender: =>
            window.scrollTo 0, 0

        onDomRefresh: ->
            #check if we're currently playing
            #
            #marionette weirdness, apparently when rendered as part of a composite view
            #the el has not been added to the DOM at this stage, so we'll check for the bounds
            #and if zero, rely on the composite view to call into this in it's onDomRefresh

            if App.audioController.isPlayingId @model.id
                console.log "Re-wrapping player"
                App.audioController.setupPlayerEl $(@el)
                @ui.playButton.toggleClass("play", false).toggleClass("pause", false).toggleClass("resume", false)
                @mixState = App.audioController.getMixState()
                @_setupStateUI()
            #$(@el).on("resize", App.audioController.setupPlayerEl($(@el)));
            return

        onMixInit: ->
            @mixState = 1
            @_setupStateUI()

        onMixStop: ->
            @mixState = 0
            @ui.playButton.addClass("play").removeClass("resume").removeClass("pause")
            @ui.playButtonIcon.addClass("fa-play").removeClass("fa-pause")

        onMixStateChanged: ->
            if App.audioController.isPlayingId @model.id
                if @mixState is 0 #init
                    @mixState = 1
                else if @mixState is 1 #playing
                    @mixState = 2
                else if @mixState is 2 #paused
                    @mixState = 1
                @_setupStateUI()

        _setupStateUI: ->
            if App.audioController.isPlayingId @model.id
                @ui.playButton.removeClass("play").removeClass("resume").removeClass("pause")
                @ui.playButtonIcon.removeClass("fa-play").removeClass("fa-pause")
                if @mixState is 1 #playing
                    @ui.playButton.addClass("pause")
                    @ui.playButtonIcon.removeClass("fa-play").addClass("fa-pause")
                else if @mixState is 2 #paused
                    @ui.playButton.addClass("resume")
                    @ui.playButtonIcon.removeClass("fa-pause").addClass("fa-play")

        mixPlay: (button) ->
            App.vent.trigger('mix:init', @model, $(@el))

        mixPause: ->
            if App.audioController.isPlayingId @model.id
                App.vent.trigger('mix:pause', @model, $(@el))

        mixResume: ->
            if App.audioController.isPlayingId @model.id
                App.vent.trigger('mix:resume', @model, $(@el))

        mixFavourite: ->
            console.log("MixItemView: favouriteMix")
            App.vent.trigger("mix:favourite", @model)
            true

        mixDelete: ->
            console.log("MixItemView: mixDelete")
            utils.messageBox "/dlg/DeleteMixConfirm", =>
                @model.destroy()

        mixLike: ->
            console.log("MixItemView: likeMix")
            App.vent.trigger("mix:like", @model)
            true

        mixShare: (e) ->
            console.log("MixItemView: shareMix")
            mode = $(e.currentTarget).data("mode");
            console.log("MixItemView: "+ mode)
            App.vent.trigger("mix:share", mode, @model)
            true

        mixDownload: ->
            console.log("MixItemView: mixDownload")
            utils.downloadURL("/audio/download/" + @model.get('id'))
            true

        login: ->
          console.log("MixItemView: login")
          vent.trigger('app:login')
          true

    Views.MixItemView