window.MixListItemView = Backbone.View.extend({
    tagName:"li",
    events:{
        "click .play-button-small-start":"startMix",
        "click .play-button-small-resume":"resume",
        "click .play-button-small-pause":"pauseMix",
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
        var id = this.model.get("id");
        this.setLikeButton(id, this.model.get('liked'));
        this.setFavouriteButton(id, this.model.get('favourited'));

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
    pauseMix:function () {
        com.podnoms.player.pause();
        _eventAggregator.trigger("track_paused");
    },
    resume:function () {
        _eventAggregator.trigger("track_playing");
        com.podnoms.player.resume();
    },
    startMix:function () {
        var id = $(this.el).data("id");
        var mode = "play";
        var ref = this;
        $.getJSON(
            'ajax/mix_stream_url/' + id + '/',
            function (data) {
                com.podnoms.settings.setupPlayer(data, id);
                com.podnoms.player.startPlaying({
                    success:function () {
                        _eventAggregator.trigger("track_playing");
                        _eventAggregator.trigger("track_changed", data);
                    },
                    error:function () {
                        alert("Error playing mix. Do please try again.");
                    }
                });
                com.podnoms.storage.setItem('now_playing', id);
            }
        );
    }
});

window.MixListView = Backbone.View.extend({
    itemPlaying: null,
    initialize:function () {
        this.render();
    },
    render:function () {
        var mixes = this.collection;
        var el = this.el;
        var ref = this;
        $(this.el).html(this.template()).append('<ul class="mix-listing audio-listing"></ul>');
        this.collection.each(function (item) {
            $('.mix-listing', el).append(new MixListItemView({model:item}).render().el);
            if (com.podnoms.player.isPlayingId(item.get('id'))){
                console.log("Item "+ item.get('id') + " is playing...");
                ref.itemPlaying = item;
            }
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

window.MixCreateView = DSSEditableView.extend({
    events:{
        "click #save-changes":"saveChanges",
        "change #mix_image":"imageChanged",
        "change input":"changed",
        "change textarea":"changed"
    },
    checkRedirect:function () {
        if (this.state == 2) {
            app.navigate('/#/mix/' + this.model.get('id'));
        }
    },
    initialize:function () {
        this.guid = com.podnoms.utils.generateGuid();
        this.state = 0;
        this.render();
    },
    render:function () {
        this.sendImage = false;
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        var parent = this;
        if (this.model.id == undefined) {
            $('#mix-upload', this.el).uploadifive({
                'uploadScript':'ajax/upload_mix_file_handler/',
                'formData':{
                    'upload-hash':this.guid
                },
                'onAddQueueItem':function (file) {
                    $('#upload-extension', this.el).val(file.name.split('.').pop());
                    $('#mix-details', this.el).show();
                },
                'onProgress':function (file, e) {
                },
                'onUploadComplete':function (file, data) {
                    parent.state++;
                    parent.checkRedirect();
                }
            });
            $('.fileupload', this.el).fileupload({
                'uploadtype':'image'
            });
            $('#mix-details', this.el).hide();
            $('.upload-hash', this.el).val(this.guid);
        } else {
            $('#div-upload-mix', this.el).hide();
            this.state = 1;
        }
        $('#image-form-proxy', this.el).ajaxForm({
            beforeSubmit:function () {
                $('#results').html('Submitting...');
            },
            success:function (data) {
                var $out = $('#results');
                $out.html('Your results:');
                $out.append('<div><pre>' + data + '</pre></div>');
            }
        });
        return this;
    },
    saveChanges:function () {
        var model = this.model;
        var el = this.el;
        var parent = this;
        this.model.set('upload-hash', this.guid);
        this.model.set('upload-extension', $('#upload-extension', this.el).val());
        this.model.save(
            null, {
                success:function () {
                    if (parent.sendImage) {
                        $.ajaxFileUpload({
                            url:'ajax/upload_image/' + model.get('id') + '/',
                            secureuri:false,
                            fileElementId:'mix_image',
                            success:function (data, status) {
                                if (typeof(data.error) != 'undefined') {
                                    if (data.error != '') {
                                        alert(data.error);
                                    } else {
                                        alert(data.msg);
                                    }
                                } else {
                                    $('#mix-details', this.el).hide();
                                    parent.state++;
                                    parent.checkRedirect();
                                }
                            },
                            error:function (data, status, e) {
                                alert(e);
                            }
                        });
                    } else {
                        parent.state++;
                        parent.checkRedirect();
                    }
                },
                error:function () {
                    com.podnoms.utils.showAlert("Error", "Something went wrong", "alert-info", false);
                }
            });
        return false;
    },
    imageChanged:function (evt) {
        this.sendImage = true;
    }
});