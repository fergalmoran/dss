@peneloPlay = do ->
    _secondsToHms = (d) ->
        if d
            d = Number(d)
            h = Math.floor(d / 3600)
            m = Math.floor(d % 3600 / 60)
            s = Math.floor(d % 3600 % 60)
            ((if h > 0 then h + ":" else "")) + ((if m > 0 then ((if h > 0 and m < 10 then "0" else "")) + m + ":" else "00:")) + ((if s < 10 then "0" else "")) + s
        else
            "00:00:00"
    ui = {}
    bounds = {}
    _player = undefined
    _src = undefined
    _mouseDown: (event) ->
        _player.setPosition (@_getCalculatedDuration() / 100) * ((event.pageX - ui.wrapper.offset().left) / bounds.waveformWidth) * 100  if _player
        $(event.currentTarget).mouseup $.proxy(@_mouseDown, this)
        return

    _mouseMove: (event) ->
        ui.seekHead.css "left", (event.offsetX + bounds.waveformLeft) #.fadeIn('fast');
        return

    _mouseLeave: ->
        ui.seekHead.hide()
        ui.wrapper.unbind "mousedown"
        ui.wrapper.unbind "mousemove"
        return

    _mouseEnter: ->
        ui.wrapper.mousedown $.proxy(@_mouseDown, this)
        ui.wrapper.mousemove $.proxy(@_mouseMove, this)
        ui.seekHead.show()
        return

    _hookupMouseEntryEvents: ->
        if ui.wrapper
            ui.wrapper.mouseenter $.proxy(@_mouseEnter, this)
            ui.wrapper.mouseleave $.proxy(@_mouseLeave, this)
        return

    _teardownMouseEntryEvents: ->
        if ui.wrapper
            ui.wrapper.unbind "mouseenter"
            ui.wrapper.unbind "mouseleave"
        return

    _getCalculatedDuration: ->
        if _player.instanceOptions.isMovieStar
            _player.duration
        else
            _player.durationEstimate

    stopPlaying: ->
        if _player
            _player.stop()
            soundManager.destroySound _player.sID
            @_teardownMouseEntryEvents()
            _player = `undefined`
        return

    setupPlayer: (el, src) ->
        _src = src  if src
        @_el = el

        #check all required elements are available
        ui.instance = el.find(".pnp-instance")
        ui.wrapper = el.find(".pnp-wrapper")
        ui.waveform = el.find(".pnp-waveform")
        ui.timeDuration = el.find(".pnp-time-display-label-duration")
        ui.timeElapsed = el.find(".pnp-time-display-label-elapsed")
        ui.downloadOverlay = el.find(".pnp-download-overlay")
        ui.playedOverlay = el.find(".pnp-played-overlay")
        ui.seekHead = el.find(".pnp-seekhead")
        bounds.waveformWidth = ui.waveform.width()
        bounds.waveformHeight = ui.waveform.height()
        bounds.waveformLeft = ui.waveform.position().left
        @setupUIWidgets()
        this

    setupUIWidgets: ->
        ui.seekHead.animate
            top: ui.waveform.position().top
            left: ui.waveform.position().left
            height: ui.waveform.height()

        ui.timeElapsed.show()
        ui.timeElapsed.animate
            top: ui.waveform.position().top
            left: ui.waveform.position().left

        ui.timeDuration.show()
        ui.timeDuration.animate
            top: ui.waveform.position().top
            left: (ui.waveform.position().left + ui.waveform.width()) - ui.timeDuration.width()

        if false #soundManager.html5.mp3
            ui.downloadOverlay.hide()
        else
            ui.downloadOverlay.animate
                top: ui.waveform.position().top
                left: ui.waveform.position().left
                height: ui.waveform.height()


        ui.playedOverlay.show()
        ui.playedOverlay.animate
            top: ui.waveform.position().top
            left: ui.waveform.position().left
            height: ui.waveform.height()

        if _player
            if _player.paused
                percentageWidth = (bounds.waveformWidth / 100) * ((_player.position / @_getCalculatedDuration()) * 100)
                ui.playedOverlay.css "width", percentageWidth
        @_hookupMouseEntryEvents()
        return

    startPlaying: (args)->
        console.log "Starting to play"
        @setupUIWidgets()

        #clear any existing sounds
        @stopPlaying()
        _player = soundManager.createSound
            id: "pnp-current-sound"
            url: _src

            #Might not need the progress overlay if firefucks get their act together
            whileloading: =>
                percentageFinished = (_player.bytesLoaded / _player.bytesTotal) * 100
                percentageWidth = (bounds.waveformWidth / 100) * percentageFinished
                ui.downloadOverlay.css "width", percentageWidth
                return

            whileplaying: =>
                percentageWidth = (bounds.waveformWidth / 100) * ((_player.position / @_getCalculatedDuration()) * 100)
                ui.playedOverlay.css "width", percentageWidth
                ui.timeElapsed.text _secondsToHms(_player.position / 1000)
                return

        _player.play onplay: ->
            args.success()
            return

        @_hookupMouseEntryEvents()
        return

    pause: ->
        _player.pause()  if _player.playState is 1
        return

    resume: ->
        _player.resume()  if _player.paused
        return

    getMixState: ->
        if not _player or _player.playState is 0
            return 0
        else return 2  if _player.paused
        1

    playLive: (args)->
        @stopPlaying()
        _player = soundManager.createSound(
            id: "com.podnoms.player-live"
            url: com.podnoms.settings.liveStreamRoot
            volume: 50
            stream: true
            useMovieStar: true
        )
        _player.play onplay: ->
            args.success()
            return

        return

    stopLive: (args)->
        @stopPlaying()
        args.success()
        return
