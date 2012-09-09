function DssSoundHandler() {
    var _currentSound = null;
    var _currentId = -1;
    this.stop_sound = function () {
        if (_currentSound) {
            this.togglePlaying(this.getPlayingId());
            _currentSound.stop();
            _currentId = -1;
        }
    };
    this.getPlayingId = function () {
        return _currentId;
    };
    this.isPlaying = function () {
        if (_currentSound != null)
            return _currentSound.playState == 1;
    };

    this.togglePlaying = function (id) {
        this.togglePlayState(id);
        return this.togglePlayVisual(id);
    };

    this.togglePlayVisual = function (id) {
        var button = $('#play-pause-button-small-' + id);
        var mode = button.data("mode");
        if (mode == "play" || mode == "resume") {
            button.data('mode', 'pause');
            button.removeClass('play-button-small-playing');
            button.addClass('play-button-small-paused');
        } else {
            button.data('mode', 'resume');
            button.removeClass('play-button-small-paused');
            button.addClass('play-button-small-playing');
        }
        return mode;
    };
    this.togglePlayState = function (id) {
        var button = $('#play-pause-button-small-' + id);
        var mode = button.data("mode");
        if (mode == 'pause')
            this.pauseSound();
        else if (mode == 'resume')
            this.resumeSound();
    };
    this.playSound = (function (itemId, stream_url) {

        _currentId = itemId;
        var waveformTop = $('#waveform-' + _currentId).position().top;
        var waveformWidth = $('#waveform-' + _currentId).width();

        $('#player-seekhead').css('top', waveformTop);
        if (_currentSound) _currentSound.stop();
        soundManager.destroySound('current_sound');
        _currentSound = soundManager.createSound({
            id:'current_sound',
            url:stream_url,
            volume:50,
            stream:true,
            whileloading:function () {
                var percentageFinished = (_currentSound.bytesLoaded / _currentSound.bytesTotal) * 100;
                var percentageWidth = (waveformWidth / 100) * percentageFinished;
                $('#progress-player-' + _currentId).css('width', percentageWidth);
            },
            whileplaying:function () {
                /* Should move to an aggregator viewChanged callback */
                if (_currentId == -1){
                    _currentId = itemId;
                    this._setupEvents(itemId, _currentSound);
                }
                waveformTop = $('#waveform-' + _currentId).position().top;
                waveformWidth = $('#waveform-' + _currentId).width();
                $('#playhead-player-' + _currentId).css('top', waveformTop);
                $('#progress-player-' + _currentId).css('top', waveformTop);
                $('#player-seekhead').css('top', waveformTop);

                var currentPosition = _currentSound.position;
                var totalLength = _currentSound.duration;
                var percentageFinished = (currentPosition / totalLength) * 100;
                var percentageWidth = (waveformWidth / 100) * percentageFinished;
                $('#playhead-player-' + _currentId).css('width', percentageWidth);
            }
        });
        _currentSound.loaded = false;
        _currentSound.readyState = 0;
        dssSoundHandler._setupEvents(_currentId, _currentSound);
        _currentSound.play();
    });
    this.playLive = function () {
        this.stop_sound();
        _currentSound = soundManager.createSound({
            id:'current_sound',
            url:com.podnoms.settings.liveStreamRoot,
            volume:50,
            stream:true,
            useMovieStar:true
        });
        _currentSound.play();
    };
    this.pauseSound = function () {
        this.togglePlaying();
        if (_currentSound) {
            _currentSound.pause();
        }
    };
    this.resumeSound = function () {
        this.togglePlaying();
        if (_currentSound)
            _currentSound.resume();
    };
    this.getPosition = function () {
        if (_currentSound)
            return _currentSound.position;
    };
    this._setupEvents = function (itemId, sound) {
        $('#waveform-' + itemId).mousemove(function (event) {
            $('#player-seekhead').show();
            $('#player-seekhead').css('left', (event.pageX) + 'px').fadeIn('fast');
        });
        $('#waveform-' + itemId).mousedown(function (event) {
            var width = $('#waveform-image-' + itemId).width();
            if (sound != null) {
                var fullLength = sound.duration;
                var left = $('#waveform-image-' + itemId).offset().left;
                var clickPerc = ((event.pageX - left) / width) * 100;
                sound.setPosition((fullLength / 100) * clickPerc);
            }
        });
        $('#waveform-' + itemId).mouseleave(function (event) {
            $('#player-seekhead').hide();
        });
    };
}
dssSoundHandler = new DssSoundHandler();
window.dssSoundHandler = dssSoundHandler;
