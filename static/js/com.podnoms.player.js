/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

soundManager.url = com.podnoms.settings.staticUrl + '/swf/sm/';
soundManager.bgColor = '#ffffff';
soundManager.consoleOnly = true;
soundManager.debugMode = com.podnoms.settings.smDebugMode;
soundManager.debugFlash = com.podnoms.settings.smDebugMode;
soundManager.flashVersion = 9;
soundManager.flashPollingInterval = null;
soundManager.html5PollingInterval = null;
soundManager.html5Test = /^(probably|maybe)$/i;
soundManager.flashLoadTimeout = 1000;
soundManager.idPrefix = 'sound';
soundManager.noSWFCache = false;
soundManager.preferFlash = false;
soundManager.useConsole = true;
soundManager.useFlashBlock = false;
soundManager.useHighPerformance = false;
soundManager.useHTML5Audio = true;
soundManager.waitForWindowLoad = false;
soundManager.wmode = null;

com.podnoms.player = {
    /*Members*/
    currentId: -1,
    currentPath: '',
    currentSound: null,
    boundingEl: null,
    timeDisplayLabel: null,
    waveFormEl: null,
    playHeadEl: null,
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
    _secondsToHms: function (d) {
        if (d) {
            d = Number(d);
            var h = Math.floor(d / 3600);
            var m = Math.floor(d % 3600 / 60);
            var s = Math.floor(d % 3600 % 60);
            return ((h > 0 ? h + ":" : "") + (m > 0 ? (h > 0 && m < 10 ? "0" : "") + m + ":" : "00:") + (s < 10 ? "0" : "") + s);
        } else {
            return "00:00:00";
        }
    },
    _getDurationEstimate: function (oSound) {
        if (oSound.instanceOptions.isMovieStar) {
            return (oSound.duration);
        } else {
            return oSound.durationEstimate;
        }
    },
    _whileLoading: function () {
        var percentageFinished = (this.currentSound.bytesLoaded / this.currentSound.bytesTotal) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.loadingEl.css('width', percentageWidth);
    },
    _whilePlaying: function () {
        if (!this.trackLoaded) {
            this.trackLoaded = true;
            this.loadingEl.css('width', 100);
        }

        //need to call this every time as the boundaries may have changed.
        this._calculateBounds();
        this.currentPosition = this.currentSound.position;
        var duration = this._getDurationEstimate(this.currentSound);
        var percentageFinished = (this.currentSound.position / duration) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.playHeadEl.css('width', percentageWidth);
        this.timeDisplayLabel.text(this._secondsToHms(this.currentSound.position / 1000));
    },
    _mouseDown: function (event) {
        if (this.currentSound != null) {
            this.currentSound.setPosition(
                (this._getDurationEstimate(this.currentSound) / 100) * ((event.pageX - this.waveFormLeft) / this.waveFormWidth) * 100);
        }
        $(event.currentTarget).mouseup($.proxy(this._mouseDown, this));
    },
    _mouseMove: function (event) {
        this.seekHeadEl.css('left', (event.pageX - this.waveFormLeft));//.fadeIn('fast');
    },
    _mouseLeave: function (event) {
        this.seekHeadEl.hide();
    },
    _mouseEnter: function (event) {
        this.seekHeadEl.show();
    },
    _destroyCurrent: function (success) {
        if (this.currentSound != null) {
            soundManager.destroySound(this.currentSound.sID);
        }
        this.trackLoaded = false;
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
        this.currentPath = options.url;
    },
    _calculateBounds: function () {
        if (this.waveFormEl.position()) {
            this.waveFormTop = this.waveFormEl.position().top;
            this.waveFormLeft = this.waveFormEl.offset().left;
            this.waveFormWidth = this.waveFormEl.width();
            this.playHeadEl.css('top', 0);
            this.loadingEl.css('top', 0);
            this.seekHeadEl.css('top', this.waveFormEl.position().top);
            /*this.waveFormEl.mousedown($.proxy(this._mouseDown, this));*/
            this.waveFormEl.mouseup($.proxy(this._mouseDown, this));
            this.waveFormEl.mousemove($.proxy(this._mouseMove, this));
            this.waveFormEl.mouseout($.proxy(this._mouseLeave, this));
            this.waveFormEl.mouseenter($.proxy(this._mouseEnter, this));
        } else {
            console.error("Error setting up player, waveFormEl is empty");
        }
    },
    /*Methods*/
    isPlaying: function () {
        if (this.currentSound != null)
            return this.currentSound.playState == 1;
    },
    isPlayingId: function (id) {
        return this.isPlaying() && this.currentSound.sID == "com.podnoms.player-" + id;
    },
    getStreamUrl: function () {
        return this.currentPath;
    },
    drawTimeline: function (el, boundingEl, duration) {
        /*
         Assume 10 markers
         */
        var markerDuration = duration / 10;
        var item = $(document.createElement("li"));
        for (var i = 0; i < 10; i++) {
            var sliceDuration = moment.duration(markerDuration * (i + 1), "seconds");
            var text = sliceDuration.hours() != 0 ?
                moment(sliceDuration).format("HH:mm") :
                moment(sliceDuration).format("mm:ss");
            el.append(item.clone().text(text).css('width', '10%'));
        }

    },
    setupPlayer: function (options) {
        this._parseOptions(options);
        this._calculateBounds();
        this._createTimeDisplayLabel();
    },
    _createTimeDisplayLabel: function () {
        this.timeDisplayLabel = $('<label>').text('00:00');
        this.timeDisplayLabel.css('left', -100);
        this.timeDisplayLabel.addClass('dss-time-display-label')
        this.waveFormEl.append(this.timeDisplayLabel);
        this.timeDisplayLabel.animate({ top: 0, left: this.playHeadEl.position().left });
    },
    startPlaying: function (options) {
        var that = this;
        var currId = this.currentId;
        this._destroyCurrent(function () {
            that.currentSound = soundManager.createSound({
                url: that.currentPath,
                id: "com.podnoms.player-" + currId.toString(),
                volume: com.podnoms.settings.volume,
                whileloading: function () {
                    that._whileLoading();
                },
                whileplaying: function () {
                    that._whilePlaying();
                }
            });
            if (that.currentSound) {
                that.play();
                if (options.success)
                    options.success();
                //create the floating time display label
                that._createTimeDisplayLabel();
            }
            else {
                if (options.error)
                    options.error();
                else
                    com.podnoms.utils.showError('Oooopsies', 'Error playing sound..');
            }
        });
    },
    stopPlaying: function () {
        this._destroyCurrent();
    },
    stopLive: function () {
        if (this.currentSound.instanceOptions.stream = true) {
            this.stopPlaying();
        }
    },
    playLive: function () {
        var that = this;
        var args = arguments;
        this._destroyCurrent(function () {
            that.currentSound = soundManager.createSound({
                id: 'com.podnoms.player-live',
                url: com.podnoms.settings.liveStreamRoot,
                volume: 50,
                stream: true,
                useMovieStar: true
            });
            if (that.currentSound) {
                that.currentSound.play();
                args[0].success();
            }
            else {
                com.podnoms.utils.showError('Oooopsies', 'Error playing sound..');
            }
        });
    },

    play: function () {
        this.currentSound.play();
    },
    pause: function () {
        this.currentSound.pause();
    },
    resume: function () {
        this.currentSound.resume();
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
