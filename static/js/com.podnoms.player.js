if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

soundManager.url = '/static/bin/sm/';
soundManager.flashVersion = 9;
soundManager.debugMode = false;
soundManager.useHTML5Audio = true;
soundManager.preferFlash = false;

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
        var percentageFinished = (this.currentPosition / this.currentSound.duration) * 100;
        var percentageWidth = (this.waveFormWidth / 100) * percentageFinished;
        this.playHeadEl.css('width', percentageWidth);
    },
    _mouseDown:function (event) {
        if (this.currentSound != null) {
            this.currentSound.setPosition(
                (this.currentSound.duration / 100) * ((event.pageX - this.waveFormLeft) / this.waveFormWidth) * 100);
        }
    },
    _mouseMove: function(event){
        this.seekHeadEl.show();
        this.seekHeadEl.css('left', (event.pageX) + 'px').fadeIn('fast');
    },
    _mouseLeave: function(event){
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
    _setupParams: function(){
        this.waveFormTop = this.waveFormEl.position().top;
        this.waveFormLeft = this.waveFormEl.offset().left;
        this.waveFormWidth = this.waveFormEl.width();
        this.playHeadEl.css('top', this.waveFormTop);
        this.loadingEl.css('top', this.waveFormTop);
        this.seekHeadEl.css('top', this.waveFormTop);
        this.waveFormEl.mousedown($.proxy(this._mouseDown, this));
        this.waveFormEl.mousemove($.proxy(this._mouseMove, this));
        this.waveFormEl.mouseout($.proxy(this._mouseLeave, this));
    },
    /*Methods*/
    setupPlayer:function (options) {
        var ref = this;
        this._destroyCurrent(function () {
            ref._parseOptions(options);
            ref._setupParams();
            ref.currentSound = soundManager.createSound({
                id:'com.podnoms.player.current',
                url:ref.currentPath,
                volume:com.podnoms.settings.volume,
                stream:true,
                whileloading:function () {
                    ref._whileLoading();
                },
                whileplaying:function () {
                    ref._whilePlaying();
                }
            });
            ref.play();
            options.success();
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