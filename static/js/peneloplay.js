define(["jquery", "soundmanager2"], function ($, soundManager) {

    var ui = {
    };

    var bounds = {
    };

    var _player, _src, _el;

    function _secondsToHms(d) {
        if (d) {
            d = Number(d);
            var h = Math.floor(d / 3600);
            var m = Math.floor(d % 3600 / 60);
            var s = Math.floor(d % 3600 % 60);
            return ((h > 0 ? h + ":" : "") + (m > 0 ? (h > 0 && m < 10 ? "0" : "") + m + ":" : "00:") + (s < 10 ? "0" : "") + s);
        } else {
            return "00:00:00";
        }
    }

    Peneloplay = {
        _mouseDown: function (event) {
            if (_player) {
                _player.setPosition(
                    (Peneloplay._getCalculatedDuration() / 100) * ((event.pageX - ui.wrapper.offset().left) / bounds.waveformWidth) * 100);
            }
            $(event.currentTarget).mouseup($.proxy(this._mouseDown, this));
        },
        _mouseMove: function (event) {
            ui.seekHead.css('left', (event.offsetX + bounds.waveformLeft));//.fadeIn('fast');
        },
        _mouseLeave: function () {
            ui.seekHead.hide();
            ui.wrapper.unbind("mousedown");
            ui.wrapper.unbind("mousemove");
        },
        _mouseEnter: function () {
            ui.wrapper.mousedown($.proxy(this._mouseDown, this));
            ui.wrapper.mousemove($.proxy(this._mouseMove, this));

            ui.seekHead.show();
        },
        _hookupMouseEntryEvents: function () {
            if (ui.wrapper) {
                ui.wrapper.mouseenter($.proxy(this._mouseEnter, this));
                ui.wrapper.mouseleave($.proxy(this._mouseLeave, this));
            }
        },
        _teardownMouseEntryEvents: function () {
            if (ui.wrapper) {
                ui.wrapper.unbind("mouseenter");
                ui.wrapper.unbind("mouseleave");
            }
        },
        _getCalculatedDuration: function () {
            if (_player.instanceOptions.isMovieStar) {
                return (_player.duration);
            } else {
                return _player.durationEstimate;
            }
        },

        stopPlaying: function () {
            if (_player) {
                _player.stop();
                soundManager.destroySound(_player.sID);
                Peneloplay._teardownMouseEntryEvents();
                _player = undefined;
            }
        },
        setupPlayer: function (el, src) {

            if (src)
                _src = src;
            _el = el;
            //check all required elements are available
            ui.instance = el.find(".pnp-instance");
            ui.wrapper = el.find(".pnp-wrapper");
            ui.waveform = el.find(".pnp-waveform");
            ui.timeDuration = el.find(".pnp-time-display-label-duration");
            ui.timeElapsed = el.find(".pnp-time-display-label-elapsed");
            ui.downloadOverlay = el.find(".pnp-download-overlay");
            ui.playedOverlay = el.find(".pnp-played-overlay");
            ui.seekHead = el.find(".pnp-seekhead");

            bounds.waveformWidth = ui.waveform.width();
            bounds.waveformHeight = ui.waveform.height();
            bounds.waveformLeft = ui.waveform.position().left;
            Peneloplay.setupUIWidgets();
            return this;
        },
        setupUIWidgets: function () {
            ui.seekHead.animate({ top: ui.waveform.position().top, left: ui.waveform.position().left, height: ui.waveform.height() });

            ui.timeElapsed.show();
            ui.timeElapsed.animate({ top: ui.waveform.position().top, left: ui.waveform.position().left });
            ui.timeDuration.show();
            ui.timeDuration.animate({ top: ui.waveform.position().top, left: (ui.waveform.position().left + ui.waveform.width()) - ui.timeDuration.width() });

            ui.downloadOverlay.animate({top: ui.waveform.position().top, left: ui.waveform.position().left, height: ui.waveform.height()});
            ui.playedOverlay.show();
            ui.playedOverlay.animate({top: ui.waveform.position().top, left: ui.waveform.position().left, height: ui.waveform.height()});

            if (_player) {
                if (_player.paused) {
                    var percentageWidth = (bounds.waveformWidth / 100) * ((_player.position / Peneloplay._getCalculatedDuration()) * 100);
                    ui.playedOverlay.css('width', percentageWidth);
                }
            }
            Peneloplay._hookupMouseEntryEvents();
        },
        startPlaying: function () {
            console.log("Starting to play");
            Peneloplay.setupUIWidgets();
            //clear any existing sounds
            Peneloplay.stopPlaying();
            var args = arguments;
            _player = soundManager.createSound({
                id: 'pnp-current-sound',
                url: _src,
                whileloading: function () {
                    var percentageFinished = (_player.bytesLoaded / _player.bytesTotal) * 100;
                    var percentageWidth = (bounds.waveformWidth / 100) * percentageFinished;
                    ui.downloadOverlay.css('width', percentageWidth);
                },
                whileplaying: function () {
                    var percentageWidth = (bounds.waveformWidth / 100) * ((_player.position / Peneloplay._getCalculatedDuration()) * 100);
                    ui.playedOverlay.css('width', percentageWidth);
                    ui.timeElapsed.text(_secondsToHms(_player.position / 1000));
                }
            });
            _player.play({
                onplay: function () {
                    args[0].success();
                }
            });
            Peneloplay._hookupMouseEntryEvents();
        },
        pause: function () {
            if (_player.playState == 1)
                _player.pause();
        },
        resume: function () {
            if (_player.paused)
                _player.resume();
        },
        getMixState: function () {
            if (!_player || _player.playState === 0)
                return 0;
            else if (_player.paused)
                return 2;

            return 1;
        },
        playLive: function () {
            var args = arguments;
            Peneloplay.stopPlaying();
            _player = soundManager.createSound({
                id: 'com.podnoms.player-live',
                url: com.podnoms.settings.liveStreamRoot,
                volume: 50,
                stream: true,
                useMovieStar: true,
            });
            _player.play({
                onplay: function () {
                    args[0].success();
                }
            });
        },
        stopLive: function(){
            Peneloplay.stopPlaying();
            arguments[0].success();
        }
    };
    return Peneloplay;
});
