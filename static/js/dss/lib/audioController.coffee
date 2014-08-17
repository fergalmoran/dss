@Dss.module "Lib", (Lib, App, Backbone, Marionette, $    ) ->
    class Lib.AudioController extends Marionette.Controller

        AudioStates =
            unmuted: 0
            muted: 1
        @AUDIO_STATES = AudioStates

        initialize: (options) ->
            console.log "AudioController: initialize"
            @listenTo(App.vent, 'mix:init', @mixInit)
            @listenTo(App.vent, 'mix:play', @mixPlay)
            @listenTo(App.vent, 'mix:pause', @mixPause)
            @listenTo(App.vent, 'mix:resume', @mixResume)
            @listenTo(App.vent, 'audio:mute', @audioMute)
            @listenTo(App.vent, 'playing:destroy', @playingDestroy)
            @listenTo(App.vent, 'live:play', @livePlay)
            @listenTo(App.vent, 'live:pause', @livePause)

            @audioState = AudioStates.unmuted

            soundManager.setup
                url: com.podnoms.settings.staticUrl + '/swf/sm/'
                onready: ->
                    App.vent.trigger('peneloPlay:ready')
                    console.log "Sound manager ready!"

                debugFlash: com.podnoms.smDebugMode
                debugMode: com.podnoms.smDebugMode
                useHTML5Audio: true
                preferFlash: false

                defaultOptions:
                    volume: com.podnoms.settings.volume

        setupPlayer: (el, url) ->
            peneloPlay.setupPlayer el, url
            if @audioState is AudioStates.muted
                peneloPlay.mute()

        setupPlayerEl: (el) ->
            peneloPlay.setupPlayer el
            peneloPlay.setupUIWidgets()

        mixInit: (model, el) =>
            console.log "AudioController: mixInit"
            @id = model.get('id')
            @duration = model.get("duration")
            peneloPlay.stopPlaying()
            $.getJSON "/ajax/mix_stream_url/" + @id + "/", (data) =>
                console.log("Setting up player: ", data.stream_url)
                @setupPlayer el, data.stream_url
                peneloPlay.startPlaying
                    success: =>
                        App.vent.trigger("mix:play", model)
                        App.vent.trigger("live:stop")
                        utils.checkPlayCount()
                        return
                    error: =>
                        utils.showWarning "Ooops", "Error playing mix. If you have a flash blocker, please disable it for this site. Otherwise, do please try again."
                        return
                return

        isPlayingId: (id) ->
            return id is @id

        getMixState: ->
            return peneloPlay.getMixState()

        audioMute: ->
            if @audioState is AudioStates.unmuted
                @audioState = AudioStates.muted
                peneloPlay.mute()
            else
                @audioState = AudioStates.unmuted
                peneloPlay.unmute()

        mixPlay: ->
            console.log("AudioController: mixPlay")
            peneloPlay.resume();

        mixPause: ->
            console.log("AudioController: mixPause")
            peneloPlay.pause();

        mixResume: ->
            console.log("AudioController: mixResume")
            peneloPlay.resume();

        playingDestroy: ->
            peneloPlay.stopPlaying()

        livePlay: ->
            console.log("AudioController: livePlay")
            App.vent.trigger('mix:stop')
            peneloPlay.playLive
                success: ->
                    console.log("Live stream started")
                    App.vent.trigger('live:started')
        livePause: ->
            console.log("AudioController: livePause")
            peneloPlay.stopLive
                success: ->
                    console.log("Live stream started")
                    App.vent.trigger('live:stopped')

    Lib.AudioController