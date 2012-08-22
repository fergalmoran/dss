window.MixListItemView = Backbone.View.extend({
    tagName:"li",
    events:{
        "click .play-button-small":"playMix",
        "click .like-button a":"likeMix",
        "click .favourite-button a":"favouriteMix",
        "click .share-button a":"shareLink"
    },
    initialize:function () {
        $(this.el).attr("id", "mixitem-" + this.model.get("id"));
        $(this.el).addClass("audio-listing-item");
        $(this.el).data("id", this.model.get("id"));
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        this.setLikeButton(this.model.get("id"), this.model.get('liked'));
        this.setFavouriteButton(this.model.get("id"), this.model.get('favourited'));
        return this;
    },
    setLikeButton:function (id, liked) {
        if (liked) {
            $('#like-' + id, this.el).html('<i class="icon-heart"></i> Unlike');
        } else
            $('#like-' + id, this.el).html('<i class="icon-heart"></i> Like');
    },
    setFavouriteButton:function (id, liked) {
        if (liked) {
            $('#favourite-' + id, this.el).html('<i class="icon-star-empty"></i> Unfavourite');
        } else
            $('#favourite-' + id, this.el).html('<i class="icon-star"></i> Favourite');
    },
    shareLink:function (e) {
        alert("Sharing");
    },
    likeMix:function (e) {
        var id = $(e.currentTarget).data("id");
        var mode = $(e.currentTarget).data("mode");
        var self = this;
        $.post(
            "/ajax/like/",
            { dataId:id, dataMode:mode },
            function (data) {
                var result = $.parseJSON(data);
                self.setLikeButton(id, result.value == 'Liked');
                if (result.value == 'Liked')
                    postFacebookLike(id);
            }
        );
    },
    favouriteMix:function (e) {
        var id = $(e.currentTarget).data("id");
        var mode = $(e.currentTarget).data("mode");
        var self = this;
        $.post(
            "/ajax/favourite/",
            { dataId:id, dataMode:mode },
            function (data) {
                var result = $.parseJSON(data);
                self.setFavouriteButton(id, result.value == 'Favourited');
                if (result.value == 'Favourited')
                    postFacebookFavourite(this.id);
            }
        );
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

window.MixCreateView = Backbone.View.extend({
    events:{
        "click #save-changes":"saveChanges",
        "change input":"changed"
    },
    initialize:function () {
        this.guid = generateGuid();
        this.render();
    },
    render:function () {
        $(this.el).html(this.template());
        $('#mix-upload', this.el).uploadifive({
            'uploadScript':'ajax/upload_mix_file_handler/',
            'formData'        : {
                'upload-hash' : this.guid
            },
            'onAddQueueItem':function (file) {
                $('#mix-details', this.el).show();
            },
            'onProgress':function (file, e) {
            }
        });
        //$('#mix-details', this.el).hide();
        $('.upload-hash', this.el).val(this.guid);
        return this;
    },
    saveChanges:function () {
        this.model.set('upload-hash', this.guid);
        this.model.save(
            null, {
                success:function () {
                    window.utils.showAlert("Success", "Successfully updated yourself", "alert-info", true);
                    window.history.back();
                },
                error:function () {
                    window.utils.showAlert("Error", "Something went wrong", "alert-info", false);
                }
            });
        return false;
    },
    changed:function (evt) {
        var changed = evt.currentTarget;
        var value = $("#" + changed.id).val();
        var obj = "{\"" + changed.id + "\":\"" + value + "\"}";
        var objInst = JSON.parse(obj);
        this.model.set(objInst);
    }
});