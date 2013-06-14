define ['app', 'marionette', 'vent'],
(App, Marionette, vent) ->
    class AudioController extends Marionette.Controller

        initialize: (options) ->
            console.log "AudioController: initialize"
            @listenTo(vent, 'mix:init', @mixInit)
            @listenTo(vent, 'mix:pause', @mixPause)
            @listenTo(vent, 'mix:play', @mixPlay)

        mixInit: (model) =>
            console.log "AudioController: mixInit"
            id = model.get('id')
            $.getJSON "/ajax/mix_stream_url/" + id + "/", (data) =>
                com.podnoms.settings.setupPlayerWrapper(id, data.stream_url)
                com.podnoms.player.startPlaying
                    success: =>
                        vent.trigger("mix:play", model)
                        com.podnoms.utils.checkPlayCount()
                        return
                    error: =>
                        com.podnoms.utils.showWarning "Ooops", "Error playing mix. If you have a flash blocker, please disable it for this site. Otherwise, do please try again."
                        return
                com.podnoms.storage.setItem "now_playing", id
                return

        mixPlay: (model) ->
            console.log("AudioController: mixPlay")
            com.podnoms.player.resume();

        mixPause: (model) ->
            console.log("AudioController: mixPause")
            com.podnoms.player.pause();
    AudioController

