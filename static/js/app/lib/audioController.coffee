define ['app', 'marionette', 'vent', 'utils', 'soundmanager2', 'peneloplay'],
(App, Marionette, vent, utils, soundManager, peneloplay) ->
    class AudioController extends Marionette.Controller

        initialize: (options) ->
            console.log "AudioController: initialize"
            @listenTo(vent, 'mix:init', @mixInit)
            @listenTo(vent, 'mix:play', @mixPlay)
            @listenTo(vent, 'mix:pause', @mixPause)
            @listenTo(vent, 'mix:resume', @mixResume)
            @listenTo(vent, 'playing:destroy', @playingDestroy)
            @listenTo(vent, 'live:play', @livePlay)
            @listenTo(vent, 'live:pause', @livePause)

            soundManager.setup
                url: com.podnoms.settings.staticUrl + '/swf/sm/'
                onready: ->
                    console.log "Sound manager ready sir!"

                debugFlash: com.podnoms.smDebugMode
                preferFlash: true

                defaultOptions:
                    volume: com.podnoms.settings.volume

        setupPlayer: (el, url) ->
            peneloplay.setupPlayer el, url

        setupPlayerEl: (el) ->
            peneloplay.setupPlayer el
            peneloplay.setupUIWidgets()

        mixInit: (model, el) =>
            console.log "AudioController: mixInit"
            @id = model.get('id')
            @duration = model.get("duration")
            peneloplay.stopPlaying()
            $.getJSON "/ajax/mix_stream_url/" + @id + "/", (data) =>
                console.log("Setting up player: ", data.stream_url)
                @setupPlayer el, data.stream_url
                peneloplay.startPlaying
                    success: =>
                        vent.trigger("mix:play", model)
                        vent.trigger("live:stop")
                        utils.checkPlayCount()
                        return
                    error: =>
                        utils.showWarning "Ooops", "Error playing mix. If you have a flash blocker, please disable it for this site. Otherwise, do please try again."
                        return
                com.podnoms.storage.setItem "now_playing", @id
                return

        isPlayingId: (id) ->
            return id is @id

        getMixState: ->
            return peneloplay.getMixState()

        mixPlay: ->
            console.log("AudioController: mixPlay")
            peneloplay.resume();

        mixPause: ->
            console.log("AudioController: mixPause")
            peneloplay.pause();

        mixResume: ->
            console.log("AudioController: mixResume")
            peneloplay.resume();

        playingDestroy: ->
            peneloplay.stopPlaying()

        livePlay: ->
            console.log("AudioController: livePlay")
            vent.trigger('mix:stop')
            peneloplay.playLive
                success: ->
                    console.log("Live stream started")
                    vent.trigger('live:started')
        livePause: ->
            console.log("AudioController: livePause")
            peneloplay.stopLive
                success: ->
                    console.log("Live stream started")
                    vent.trigger('live:stopped')

    AudioController

