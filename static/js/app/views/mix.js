window.MixListItemView = Backbone.View.extend({
    tagName:"li",
    events:{
        "click .play-button-small":"playMix",
        "click .like-button a":"likeMix",
        "click .share-button a":"shareLink"
    },
    initialize:function () {
        $(this.el).attr("id", "mixitem-" + this.model.get("id"));
        $(this.el).addClass("audio-listing-item");
        $(this.el).data("id", this.model.get("id"));
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    },
    shareLink:function (e) {
        alert("Sharing");
    },
    likeMix:function (e) {
        var id = $(e.currentTarget).data("id");
        var mode = $(e.currentTarget).data("mode");
        $.post(
            "/ajax/like/",
            { dataId:id, dataMode:mode },
            function (data) {
            }
        );
        var slug = '12345';
        var attachment = {
            'name':'Deep South Sounds',
            'description':'This is a test of the Deep South Sounds Broadcast System.  If this was real, you would be reading something useful.',
            'media':[{
                'type':'image',
                'src':'http://deepsouthsounds.com/images/facebook_image.png',
                'href':'http://www.deepsouthsounds.com/' + slug + '/'
            }]
        };
        FB.login(function(response) {
            /*FB.api('/me', function(response) {
                alert('Your name is ' + response.name);
            });*/
            FB.ui({
                method:'stream.publish',
                message:'I liked a sound on deep south sounds!',
                attachment:attachment
            });
        }, {scope: 'publish_stream'});
    },
    playMix:function () {
        var id = $(this.el).data("id");
        var mode = "play";

        //check if we're currently playing a sound
        var playingId = dssSoundHandler.getPlayingId();
        if (playingId != -1 && dssSoundHandler.isPlaying()) {
            var newMode = dssSoundHandler.togglePlaying(playingId);
            //only set the mode if we're toggling an existing track
            //otherwise default mode of "play" is what we want
            if (playingId == id)
                mode = newMode;
        }
        var button = $(this.el).find('#play-pause-button-small-' + id);
        $(button).blur();
        if (mode == "play") {
            dssSoundHandler.togglePlayVisual(id);
            $.getJSON(
                'ajax/mix_stream_url/' + id + '/',
                function (data) {
                    dssSoundHandler.playSound(id, data.stream_url);
                    _eventAggregator.trigger("track_changed", data);
                    _eventAggregator.trigger("track_playing");
                });
        } else if (mode == "resume") {
            _eventAggregator.trigger("track_playing");
        } else {
            _eventAggregator.trigger("track_paused");
        }
    }
});

window.MixListView = Backbone.View.extend({
    initialize:function () {
        this.render();
    },
    render:function () {
        var mixes = this.collection;
        var el = this.el;
        $(this.el).html(this.template()).append('<ul class="mix-listing audio-listing"></ul>');
        this.collection.each(function (item) {
            $('.mix-listing', el).append(new MixListItemView({model:item}).render().el);
        });
        var type = this.collection.type;
        $('#' + type, this.el).parent().addClass('active');
        return this;
    }
});

window.MixView = Backbone.View.extend({
    initialize:function () {
        this.render();
    },
    render:function () {
        $(this.el).html(this.template());
        var item = new MixListItemView({model:this.model}).render();
        $('.mix-listing', this.el).append(item.el);
        $('#mix-description', this.el).html(this.model.get("description"));
        return this;
    }
});