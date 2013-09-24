define ['marionette', 'vent', 'text!/tpl/NowPlayingView'],
(Marionette, vent, Template) ->

    class NowPlayingView extends Marionette.ItemView
        template: _.template(Template)
        className: "now-playing"

        events: {
            "click #now-playing-play": "doPlay",
            "click #now-playing-pause": "doPause"
        }

        initialize: ->
            console.log "NowPlayingView: initialize"
            @listenTo(vent, 'mix:play', @mixPlay)
            @listenTo(vent, 'mix:pause', @mixPause)
            $('#now-playing-pause', @el).hide()
            true

        onRender: ->
            @mixPlay()
            true

        mixPause: (model) ->
            console.log "NowPlayingView: mixPause"
            $('#now-playing-play', @el).show()
            $('#now-playing-pause', @el).hide()
            true

        mixPlay: (model) ->
            console.log "NowPlayingView: mixPlay"
            $('#now-playing-play', @el).hide()
            $('#now-playing-pause', @el).show()
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

