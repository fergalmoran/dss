define ['marionette', 'vent', 'text!/tpl/NowPlayingView'],
(Marionette, vent, Template) ->

    class NowPlayingView extends Marionette.ItemView
        template: _.template(Template)
        className: "now-playing"

        events: {
            "click .now-playing-play": "doPlay",
            "click .now-playing-pause": "doPause"
        }

        initialize: ->
            console.log "NowPlayingView: initialize"
            @listenTo(vent, 'mix:play', @mixPlay)
            @listenTo(vent, 'mix:pause', @mixPause)
            true

        onRender: ->
            @mixPlay()
            true

        mixPause: (model) ->
            console.log "NowPlayingView: mixPause"
            $('#now-playing-playing-toggle', @el)
                .toggleClass('now-playing-play', true)
                .toggleClass('now-playing-pause', false)
            true

        mixPlay: (model) ->
            console.log "NowPlayingView: mixPlay"
            $('#now-playing-playing-toggle', @el)
                .toggleClass('now-playing-play', false)
                .toggleClass('now-playing-pause', true)
            true

        doPlay: ->
            console.log "NowPlayingView: doPlay"
            vent.trigger('mix:play', @model)
            true

        doPause: ->
            console.log "NowPlayingView: doPause"
            vent.trigger('mix:pause', @model)
            true

    NowPlayingView

