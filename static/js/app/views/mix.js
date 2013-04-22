/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
window.MixListItemView = Backbone.View.extend({
    tagName: "li",
    events: {
        "click .play-button-small-start": "startMix",
        "click .play-button-small-resume": "resume",
        "click .play-button-small-pause": "pauseMix",
        "click .mix-link": "mixLink",
        "click .like-button a": "likeMix",
        "click .favourite-button a": "favouriteMix",
        "click .share-button": "shareLink",
        "click .download-button a": "downloadMix"
        //"mouseover .mix-profile-insert": "mouseOverProfile"
    },
    initialize: function () {
        $(this.el).attr("id", "mixitem-" + this.model.get("id"));
        $(this.el).addClass("audio-listing-item");
        $(this.el).data("id", this.model.get("id"));

    },
    render: function () {
        $(this.el).html(this.template({"item": this.model.toJSON()}));
        var id = this.model.get("id");
        var parent = this;
        this.setLikeButton(id, this.model.get('liked'));
        this.setFavouriteButton(id, this.model.get('favourited'));
        $.each(this.model.get("genre-list"), function (data) {
            $('#genre-list', parent.el).append(
                '<a href="/mixes/' + this.slug + '" class="dss-tag-button">' + this.text + '</a>');
        });

        com.podnoms.player.drawTimeline(
            $('#player-timeline-' + id, this.el),
            this.model.get('duration'));
        return this;
    },
    mouseOverProfile: function () {
        var e = $(this.el);
        $.get(e.data('poload'), function (d) {
            e.popover({content: d}).popover('show');
        });
    },
    setLikeButton: function (id, liked) {
        if (liked) {
            $('#like-' + id, this.el).html('<i class="icon-heart"></i> Unlike');
            $('#like-' + id, this.el).data('loading-text', 'Unliking');
        } else {
            $('#like-' + id, this.el).html('<i class="icon-heart"></i> Like');
            $('#like-' + id, this.el).data('loading-text', 'Liking');
        }
    },
    setFavouriteButton: function (id, liked) {
        if (liked) {
            $('#favourite-' + id, this.el).html('<i class="icon-star-empty"></i> Unfavourite');
        } else
            $('#favourite-' + id, this.el).html('<i class="icon-star"></i> Favourite');
    },
    shareLink: function (e) {
        var id = $(e.currentTarget).data("id");
        var mode = $(e.currentTarget).data("mode");
        if (mode == "facebook")
            sharePageToFacebook(this.model);
        else if (mode == "twitter")
            sharePageToTwitter(this.model);
    },
    downloadMix: function (e) {
        var id = $(e.currentTarget).data("id");
        var mode = $(e.currentTarget).data("mode");
        com.podnoms.utils.downloadURL("/audio/download/" + id);
        return false;
    },
    mixLink: function (e) {
    },
    likeMix: function (e) {
        var parent = this;
        var button = $(e.currentTarget);
        var id = button.data("id");
        var mode = button.data("mode");
        var self = this;
        button.button('loading');
        $.post(
            "/ajax/like/",
            { dataId: id, dataMode: mode },
            function (data) {
                button.button('reset');
                var result = JSON.parse(data);
                if (result.value == "Liked") {
                    parent.setLikeButton(id, true);
                    com.podnoms.utils.showAlert("Success", "Thanks for liking!!", "alert-success", true);
                } else if (result.value == "Unliked") {
                    parent.setLikeButton(id, false);
                    com.podnoms.utils.showAlert("Success", "Mix unliked!!", "alert-success", true);
                }
            }
        );
    },
    favouriteMix: function (e) {
        var id = $(e.currentTarget).data("id");
        var mode = $(e.currentTarget).data("mode");
        var self = this;
        $.post(
            "/ajax/favourite/",
            { dataId: id, dataMode: mode },
            function (data) {
                var result = $.parseJSON(data);
                self.setFavouriteButton(id, result.value == 'Favourited');
                if (result.value == 'Favourited')
                    postFacebookFavourite(this.id);
            }
        );
    },
    pauseMix: function () {
        com.podnoms.player.pause();
        _eventAggregator.trigger("track_paused");
    },
    resume: function () {
        _eventAggregator.trigger("track_playing");
        com.podnoms.player.resume();
    },
    startMix: function () {
        var id = $(this.el).data("id");
        var mode = "play";
        var ref = this;
        $.getJSON(
            '/ajax/mix_stream_url/' + id + '/',
            function (data) {
                com.podnoms.settings.setupPlayer(data, id);
                com.podnoms.player.startPlaying({
                    success: function () {
                        _eventAggregator.trigger("track_playing");
                        _eventAggregator.trigger("track_changed", data);
                        com.podnoms.utils.checkPlayCount();
                    },
                    error: function () {
                        alert("Error playing mix. If you have a flash blocker, please disable it for this site. Othewise, do please try again.");
                    }
                });
                com.podnoms.storage.setItem('now_playing', id);
            }
        );
    }
})
;

window.MixListView = Backbone.View.extend({
    itemPlaying: null,
    initialize: function () {
        _.bindAll(this, "render");
        this.render();
        /*this.infiniScroll = new Backbone.InfiniScroll(this.collection);*/
    },
    render: function () {
        var mixes = this.collection;
        var el = this.el;
        var ref = this;
        $(this.el).html(this.template()).append('<ul class="mix-listing audio-listing"></ul>');
        this.collection.each(function (item) {
            $('.mix-listing', el).append(new MixListItemView({model: item}).render().el);
            if (com.podnoms.player.isPlayingId(item.get('id'))) {
                ref.itemPlaying = item;
            }
        });
        var type = this.collection.type;
        $('#' + type, this.el).parent().addClass('active');

        $('a[data-toggle=popover]', el)
            .popover({'trigger': 'manual'})
            .click(function (e) {
                e.preventDefault()
            });
        return this;
    }
});

window.MixView = Backbone.View.extend({
    initialize: function () {
        this.render();
    },
    render: function () {
        var el = this.el;
        $(this.el).html(this.template());
        var item = new MixListItemView({model: this.model}).render();
        $('.mix-listing', this.el).append(item.el);
        $('#mix-description', this.el).html(this.model.get("description"));

        /*
         var comments = this.model.get("comments");
         var content = new CommentListView({collection:comments}).render();
         $('#mix-comments', el).html(content.el);
         */

        var comments = new CommentCollection();
        comments.url = com.podnoms.settings.urlRoot + this.model.get("item_url") + "/comments/";
        comments.mix_id = this.model.id;
        comments.mix = this.model.get("resource_uri");
        comments.fetch({success: function (data) {
            var content = new CommentListView({collection: comments}).render();
            $('#mix-comments', el).html(content.el);

        }});
        $('#mix-tab a:first', el).tab('show');
        return this;
    }
});

window.MixCreateView = DSSEditableView.extend({
    events: {
        "click #save-changes": "saveChanges",
        "change #mix_image": "imageChanged",
        "change input": "changed",
        "change textarea": "changed"
    },
    checkRedirect: function () {
        if (this.state == 2) {
            Backbone.history.navigate('/mix/' + this.model.get('id'), {trigger: true});
        }
    },
    initialize: function () {
        this.guid = com.podnoms.utils.generateGuid();
        this.state = 0;
        this.render();
    },
    render: function () {
        this.sendImage = false;
        $(this.el).html(this.template({"item": this.model.toJSON()}));
        var parent = this;
        if (this.model.id == undefined) {
            $('#mix-upload', this.el).uploadifive({
                'uploadScript': '/ajax/upload_mix_file_handler/',
                buttonText: "Select audio file (mp3 for now please)",
                'formData': {
                    'upload-hash': this.guid,
                    'sessionid': $.cookie('sessionid')
                },
                'onUploadFile': function (file) {
                    $(window).on('beforeunload', function () {
                        alert('Go on outta that..');
                    });
                },
                'onAddQueueItem': function (file) {
                    $('#upload-extension', this.el).val(file.name.split('.').pop());
                    $('#mix-details', this.el).show();
                },
                'onProgress': function (file, e) {
                },
                'onUploadComplete': function (file, data) {
                    parent.state++;
                    parent.checkRedirect();
                }
            });
            $('.fileupload', this.el).fileupload({
                'uploadtype': 'image'
            });
            $('#mix-details', this.el).hide();
            $('.upload-hash', this.el).val(this.guid);
        } else {
            $('#div-upload-mix', this.el).hide();
            this.state = 1;
        }
        $('#image-form-proxy', this.el).ajaxForm({
            beforeSubmit: function () {
                $('#results').html('Submitting...');
            },
            success: function (data) {
                var $out = $('#results');
                $out.html('Your results:');
                $out.append('<div><pre>' + data + '</pre></div>');
            }
        });
        $("#genres", this.el).select2({
            placeholder: "Start typing and choose or press enter",
            minimumInputLength: 1,
            multiple: true,
            ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
                url: "/ajax/lookup/genre/",
                dataType: 'json',
                data: function (term, page) {
                    return {
                        q: term
                    };
                },
                results: function (data, page) { // parse the results into the format expected by Select2.
                    // since we are using custom formatting functions we do not need to alter remote JSON data
                    return {results: data};
                }
            }, initSelection: function (element, callback) {
                var result = [];
                var genres = parent.model.get('genre-list');
                if (genres != undefined) {
                    $.each(genres, function (data) {
                        result.push({id: this.id, text: this.text});
                    });
                }
                callback(result);
            },
            createSearchChoice: function (term, data) {
                if ($(data).filter(function () {
                    return this.text.localeCompare(term) === 0;
                }).length === 0) {
                    return {id: term, text: term};
                }
            }
        });
        return this;
    },
    saveChanges: function () {
        var model = this.model;
        var el = this.el;
        var parent = this;
        this.model.set('upload-hash', this.guid);
        this.model.set('upload-extension', $('#upload-extension', this.el).val());
        this.model.set('genre-list', $('#genres', this.el).select2('data'));

        if (!parent.sendImage)
            this.model.set('mix_image', 'DONOTSEND');

        this._saveChanges({
            success: function () {
                if (parent.sendImage) {
                    $.ajaxFileUpload({
                        url: '/ajax/upload_image/' + model.get('id') + '/',
                        secureuri: false,
                        fileElementId: 'mix_image',
                        success: function (data, status) {
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
                        error: function (data, status, e) {
                            alert(e);
                        }
                    });
                } else {
                    $('#mix-details', this.el).hide();
                    parent.state++;
                    parent.checkRedirect();
                }
            },
            error: function (model, response) {
                com.podnoms.utils.showAlert("Error", "Something went wrong<br />Nerd stuff is: " + response, "alert-info", false);
            }
        });
        return false;
    },
    imageChanged: function (evt) {
        this.sendImage = true;
    }
});
