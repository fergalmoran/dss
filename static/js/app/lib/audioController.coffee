define ['app', 'marionette', 'vent', 'utils'],
(App, Marionette, vent, utils) ->
    class AudioController extends Marionette.Controller

        initialize: (options) ->
            console.log "AudioController: initialize"
            @listenTo(vent, 'mix:init', @mixInit)
            @listenTo(vent, 'mix:pause', @mixPause)
            @listenTo(vent, 'mix:play', @mixPlay)
            @listenTo(vent, 'live:play', @livePlay)
            @listenTo(vent, 'live:pause', @livePause)

        mixInit: (model) =>
            console.log "AudioController: mixInit"
            id = model.get('id')
            com.podnoms.player.stopPlaying()
            $.getJSON "/ajax/mix_stream_url/" + id + "/", (data) =>
                com.podnoms.settings.setupPlayerWrapper(id, data.stream_url)
                com.podnoms.player.startPlaying
                    success: =>
                        vent.trigger("mix:play", model)
                        utils.checkPlayCount()
                        return
                    error: =>
                        utils.showWarning "Ooops", "Error playing mix. If you have a flash blocker, please disable it for this site. Otherwise, do please try again."
                        return
                com.podnoms.storage.setItem "now_playing", id
                return

        mixPlay: (model) ->
            console.log("AudioController: mixPlay")
            com.podnoms.player.resume();

        mixPause: (model) ->
            console.log("AudioController: mixPause")
            com.podnoms.player.pause();

        livePlay: ->
            console.log("AudioController: livePlay")
            com.podnoms.player.playLive
                success: ->
                    console.log("Live stream started")
                    vent.trigger('live:started')
        livePause:->
            console.log("AudioController: livePause")
            com.podnoms.player.stopLive()

    AudioController

