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
    pauseMix:function () {
        com.podnoms.player.pause();
    },
    resume:function () {
        com.podnoms.player.resume();
    },
    startMix:function () {
        var id = $(this.el).data("id");
        var mode = "play";
        $.getJSON(
            'ajax/mix_stream_url/' + id + '/',
            function (data) {
                com.podnoms.player.setupPlayer({
                    waveFormEl:$('#waveform-' + id),
                    playHeadEl:$('#playhead-player-' + id),
                    loadingEl:$('#progress-player-' + id),
                    seekHeadEl:$('#player-seekhead'),
                    playButtonEl:$('#play-pause-button-small-' + id),
                    url:data.stream_url,
                    success:function () {
                        _eventAggregator.trigger("track_playing");
                    },
                    error:function () {

                    }
                });
            }
        );
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
        "change input":"changed",
        "change textarea":"changed",
        "change #mix_image":"imageChanged"
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
                    }else{
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
    changed:function (evt) {
        var changed = evt.currentTarget;
        var value = $("#" + changed.id).val();
        var obj = "{\"" + changed.id + "\":\"" + value + "\"}";
        var objInst = JSON.parse(obj);
        this.model.set(objInst);
    },
    imageChanged:function (evt) {
        this.sendImage = true;
    }
});