if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};


soundManager.setup({
    url:'/static/bin/sm/',
    debugMode:false,
    wmode:'transparent',
    usePeakData:false, // [Flash 9 only]: show peak data
    useWaveformData:false, // [Flash 9 only]: enable sound spectrum (raw waveform data) - WARNING: CPU-INTENSIVE: may set CPUs on fire.
    useEQData:false, // [Flash 9 only]: enable sound EQ (frequency spectrum data) - WARNING: Also CPU-intensive.
    fillGraph:false, // [Flash 9 only]: draw full lines instead of only top (peak) spectrum points
    useThrottling:true    // try to rate-limit potentially-expensive calls (eg. dragging position around)
});

com.podnoms.player = {
    /*Members*/
    currentId:-1,
    currentPath:'',
    currentSound:null,
    waveFormEl:null,
    playHeadEl:null,
    loadingEl:null,
    seekHeadEl:null,
    waveFormRect:[-1, -1, -1, -1],
    trackLoaded:false,
    waveFormTop:-1,
    waveFormLeft:-1,
    waveFormWidth:-1,
    totalLength:-1,
    currentPosition:-1,
    /*Privates */
    _getDurationEstimate:function (oSound) {
        if (oSound.instanceOptions.isMovieStar) {
            return (oSound.duration);
        } else {
            return (!oSound._data.metadata || !oSound._data.metadata.data.givenDuration ? (oSound.durationEstimate || 0) : oSound._data.metadata.data.givenDuration);
        }
    },
    _whileLoading:function () {
        var percentageFinished = (this.currentSound.bytesLoaded / this.currentSound.bytesTotal) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.loadingEl.css('width', percentageWidth);
    },
    _whilePlaying:function () {
        if (!this.trackLoaded) {
            this.playButtonEl
                .removeClass('play-button-small-loading')
                .addClass('play-button-small-pause');
            this.trackLoaded = true;
        }
        this.currentPosition = this.currentSound.position;
        var duration = this.currentSound.durationEstimate;
        var percentageFinished = (this.currentSound.position / duration) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.playHeadEl.css('width', percentageWidth);
    },
    _mouseDown:function (event) {
        console.log("Got mousedown: " + event.pageX);
        if (this.currentSound != null) {
            this.currentSound.setPosition(
                (this.currentSound.duration / 100) * ((event.pageX - this.waveFormLeft) / this.waveFormWidth) * 100);
        }
        $(event.currentTarget).mouseup($.proxy(this._mouseDown, this));
    },
    _mouseMove:function (event) {
        this.seekHeadEl.show();
        this.seekHeadEl.css('left', (event.pageX) + 'px').fadeIn('fast');
    },
    _mouseLeave:function (event) {
        this.seekHeadEl.hide();
    },
    _destroyCurrent:function (success) {
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
        success();
    },
    _parseOptions:function (options) {
        this.currentId = options.id;
        this.waveFormEl = options.waveFormEl;
        this.seekHeadEl = options.seekHeadEl;
        this.playHeadEl = options.playHeadEl;
        this.loadingEl = options.loadingEl;
        this.playButtonEl = options.playButtonEl;
        this.currentPath = options.url;
    },
    _setupParams:function () {
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
    isPlaying:function () {
        if (this.currentSound != null)
            return this.currentSound.playState == 1;
    },
    isPlayingId:function (id) {
        return this.isPlaying() && this.currentSound.sID == "com.podnoms.player-" + id;
    },
    setupPlayer:function (options) {
        this._parseOptions(options);
        this._setupParams();
        if (this.isPlayingId(options.id)) {
            this.playButtonEl
                .removeClass('play-button-small-start')
                .removeClass('play-button-small-loading')
                .addClass('play-button-small-pause');
        }
    },
    startPlaying:function (options) {
        var ref = this;
        var currId = this.currentId;
        this._destroyCurrent(function () {
            ref.currentSound = soundManager.createSound({
                url:ref.currentPath,
                id:"com.podnoms.player-" + currId.toString(),
                volume:com.podnoms.settings.volume,
                whileloading:function () {
                    ref._whileLoading();
                },
                whileplaying:function () {
                    ref._whilePlaying();
                }
            });
            if (ref.currentSound) {
                ref.play();
                options.success();
            }
            else {
                com.podnoms.utils.showError('Oooopsies', 'Error playing sound..');
                options.failure();
            }
        });
    },
    playLive:function () {
        var ref = this;
        this._destroyCurrent(function () {
            ref.currentSound = soundManager.createSound({
                id:'com.podnoms.player-live',
                url:com.podnoms.settings.liveStreamRoot,
                volume:50,
                stream:true,
                useMovieStar:true
            });
            if (ref.currentSound) {
                ref.currentSound.play();
            }
            else {
                com.podnoms.utils.showError('Oooopsies', 'Error playing sound..');
            }
        });
    },

    play:function () {
        this.currentSound.play();
        this.playButtonEl
            .removeClass('play-button-small-start')
            .addClass('play-button-small-loading');
    },
    pause:function () {
        this.currentSound.pause();
        this.playButtonEl
            .removeClass('play-button-small-pause')
            .addClass('play-button-small-resume');
    },
    resume:function () {
        this.currentSound.resume();
        this.playButtonEl
            .removeClass('play-button-small-resume')
            .addClass('play-button-small-pause');
    },
    forward:function (increment) {

    },
    back:function (increment) {

    },
    setPosition:function (position) {

    },
    updateWaveform:function (position) {

    }
}