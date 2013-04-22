/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

soundManager.setup({
    url: '/static/bin/sm/',
    debugMode: true,
    wmode: 'transparent'
});

soundManager.usePeakData = false;
soundManager.useWaveformData = false;
soundManager.useEQData = false;
soundManager.fillGraph = false;
soundManager.useThrottling = true;
soundManager.flashVersion = 9;
soundManager.useFlashBlock = false;
soundManager.useHTML5Audio = true;

com.podnoms.player = {
    /*Members*/
    currentId: -1,
    currentPath: '',
    currentSound: null,
    boundingEl: null,
    timeDisplayLabel: null,
    waveFormEl: null,
    playHeadEl: null,
    timeLineEl: null,
    loadingEl: null,
    seekHeadEl: null,
    waveFormRect: [-1, -1, -1, -1],
    trackLoaded: false,
    waveFormTop: -1,
    waveFormLeft: -1,
    waveFormWidth: -1,
    totalLength: -1,
    currentPosition: -1,
    soundDuration: 0,

    /*Privates */
    _getDurationEstimate: function (oSound) {
        if (oSound.instanceOptions.isMovieStar) {
            return (oSound.duration);
        } else {
            return this.soundDuration;
        }
    },
    _whileLoading: function () {
        var percentageFinished = (this.currentSound.bytesLoaded / this.currentSound.bytesTotal) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.loadingEl.css('width', percentageWidth);
    },
    _whilePlaying: function () {
        if (!this.trackLoaded) {
            this.playButtonEl
                .removeClass('play-button-small-loading')
                .addClass('play-button-small-pause');
            this.trackLoaded = true;r r sharing
        }
        this.currentPosition = this.currentSound.position;
        var duration = this._getDurationEstimate(this.currentSound);
        var percentageFinished = (this.currentSound.position / duration) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.playHeadEl.css('width', percentageWidth);
        var elapsed = moment.duration(this.currentSound.position, "milliseconds");
        var text = elapsed.hours() != 0 ?
            moment(elapsed).format("HH:mm") :
            moment(elapsed).format("mm:ss");
        this.timeDisplayLabel.text(text);
        el.append(item.clone().text(text).css('width', '10%'));
    },
    _mouseDown: function (event) {
        if (this.currentSound != null) {
            this.currentSound.setPosition(
                (this.currentSound.duration / 100) * ((event.pageX - this.waveFormLeft) / this.waveFormWidth) * 100);
        }
        $(event.currentTarget).mouseup($.proxy(this._mouseDown, this));
    },
    _mouseMove: function (event) {
        this.seekHeadEl.show();
        this.seekHeadEl.css('left', (event.pageX) + 'px').fadeIn('fast');
    },
    _mouseLeave: function (event) {
        this.seekHeadEl.hide();
    },
    _destroyCurrent: function (success) {
        if (this.currentSound != null) {
            soundManager.destroySound(this.currentSound.sID);
        }
        this.trackLoaded = false;
        if (this.playButtonEl != undefined)
            this.playButtonEl
                .removeClass('play-button-small-pause')
                .removeClass('play-button-small-loading')
                .addClass('play-button-smallstart');

        this.currentId = null;
        if (success != undefined)
            success();
    },
    _parseOptions: function (options) {
        this.currentId = options.id;
        this.boundingEl = options.boundingEl;
        this.waveFormEl = options.waveFormEl;
        this.seekHeadEl = options.seekHeadEl;
        this.playHeadEl = options.playHeadEl;
        this.loadingEl = options.loadingEl;
        this.timeLineEl = options.timeLineEl;
        this.playButtonEl = options.playButtonEl;
        this.currentPath = options.url;
    },
    _setupParams: function () {
        this.waveFormTop = this.waveFormEl.position().top;
        this.waveFormLeft = this.waveFormEl.offset().left;
        this.waveFormWidth = this.waveFormEl.width();
        this.playHeadEl.css('top', this.waveFormTop);
        this.loadingEl.css('top', this.waveFormTop);
        this.seekHeadEl.css('top', this.waveFormTop);
        /*this.waveFormEl.mousedown($.proxy(this._mouseDown, this));*/
        this.waveFormEl.mouseup($.proxy(this._mouseDown, this));
        this.waveFormEl.mousemove($.proxy(this._mouseMove, this));
        this.waveFormEl.mouseout($.proxy(this._mouseLeave, this));
    },
    /*Methods*/
    isPlaying: function () {
        if (this.currentSound != null)
            return this.currentSound.playState == 1;
    },
    isPlayingId: function (id) {
        return this.isPlaying() && this.currentSound.sID == "com.podnoms.player-" + id;
    },
    drawTimeline: function (el, duration) {
        /*
         Assume 10 markers
         */
        var markerDuration = duration / 10;
        var item = $(document.createElement("li"));
        this.soundDuration = duration * 1000; //convert to milliseconds
        for (var i = 0; i < 10; i++) {
            var duration = moment.duration(markerDuration * (i + 1), "seconds");
            var text = duration.hours() != 0 ?
                moment(duration).format("HH:mm") :
                moment(duration).format("mm:ss");
            el.append(item.clone().text(text).css('width', '10%'));
        }
    },
    setupPlayer: function (options) {
        this._parseOptions(options);
        this._setupParams();
        if (this.isPlayingId(options.id)) {
            this.playButtonEl
                .removeClass('play-button-small-start')
                .removeClass('play-button-small-loading')
                .addClass('play-button-small-pause');
        }

    },
    startPlaying: function (options) {
        var ref = this;
        var currId = this.currentId;
        this._destroyCurrent(function () {
            ref.currentSound = soundManager.createSound({
                url: ref.currentPath,
                id: "com.podnoms.player-" + currId.toString(),
                volume: com.podnoms.settings.volume,
                whileloading: function () {
                    ref._whileLoading();
                },
                whileplaying: function () {
                    ref._whilePlaying();
                }
            });
            if (ref.currentSound) {
                ref.play();
                if (options.success)
                    options.success();
            }
            else {
                com.podnoms.utils.showError('Oooopsies', 'Error playing sound..');
                if (options.error)
                    options.error();
            }
        });
        //create the floating time display label
        this.timeDisplayLabel = $('<label>').text('00:00');
        this.timeDisplayLabel.css('left', -100);
        this.timeDisplayLabel.addClass('dss-time-display-label')
        this.boundingEl.append(this.timeDisplayLabel);
        this.timeDisplayLabel.animate({ top: this.playHeadEl.position().top, left: this.playHeadEl.position().left });
    },
    stopPlaying: function () {
        this._destroyCurrent();
    },
    playLive: function () {
        var ref = this;
        var args = arguments;
        this._destroyCurrent(function () {
            ref.currentSound = soundManager.createSound({
                id: 'com.podnoms.player-live',
                url: com.podnoms.settings.liveStreamRoot,
                volume: 50,
                stream: true,
                useMovieStar: true
            });
            if (ref.currentSound) {
                ref.currentSound.play();
                args[0].success();
            }
            else {
                com.podnoms.utils.showError('Oooopsies', 'Error playing sound..');
            }
        });
    },

    play: function () {
        this.currentSound.play();
        this.playButtonEl
            .removeClass('play-button-small-start')
            .addClass('play-button-small-loading');
    },
    pause: function () {
        this.currentSound.pause();
        this.playButtonEl
            .removeClass('play-button-small-pause')
            .addClass('play-button-small-resume');
    },
    resume: function () {
        this.currentSound.resume();
        this.playButtonEl
            .removeClass('play-button-small-resume')
            .addClass('play-button-small-pause');
    },
    forward: function (increment) {

    },
    back: function (increment) {

    },
    setPosition: function (position) {

    },
    updateWaveform: function (position) {

    }
}
;

com.podnoms.player.timeline = {
    setupTimeline: function (options) {

    }
};