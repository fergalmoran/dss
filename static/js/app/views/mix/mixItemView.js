// Generated by CoffeeScript 1.3.3
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['moment', 'app', 'vent', 'marionette', 'utils', 'models/comment/commentCollection', 'views/comment/commentListView', 'text!/tpl/MixListItemView'], function(moment, App, vent, Marionette, utils, CommentsCollection, CommentsListView, Template) {
    var MixItemView;
    MixItemView = (function(_super) {

      __extends(MixItemView, _super);

      function MixItemView() {
        this.doStart = __bind(this.doStart, this);

        this.renderComments = __bind(this.renderComments, this);

        this.renderGenres = __bind(this.renderGenres, this);

        this.onRender = __bind(this.onRender, this);

        this.initialize = __bind(this.initialize, this);
        return MixItemView.__super__.constructor.apply(this, arguments);
      }

      MixItemView.prototype.template = _.template(Template);

      MixItemView.prototype.tagName = MixItemView.tagName || "li";

      MixItemView.prototype.className = MixItemView.className || "";

      MixItemView.prototype.events = {
        "click .play-button-small-start": "doStart",
        "click .play-button-small-resume": "doResume",
        "click .play-button-small-pause": "doPause",
        "click .mix-link": "mixLink",
        "click .like-button a": "mixLike",
        "click .favourite-button a": "mixFavourite",
        "click .share-button": "mixShare",
        "click .download-button a": "mixDownload"
      };

      MixItemView.prototype.ui = {
        playButton: ".play-button-small"
      };

      MixItemView.prototype.initialize = function() {
        this.listenTo(this.model, 'change:favourited', this.render);
        this.listenTo(this.model, 'change:liked', this.render);
        this.listenTo(vent, 'mix:play', this.mixPlay);
        this.listenTo(vent, 'mix:pause', this.mixPause);
        return true;
      };

      MixItemView.prototype.onRender = function() {
        var id;
        id = this.model.get('id');
        if (this.model.get('duration')) {
          $('#player-duration-' + id, this.el).text(this.model.secondsToHms('duration'));
        }
        this.renderGenres();
        this.renderComments();
      };

      MixItemView.prototype.onShow = function() {
        if (com.podnoms.player.isPlayingId(this.model.id)) {
          com.podnoms.settings.setupPlayerWrapper(this.model.get('id'), com.podnoms.player.getStreamUrl(), this.el);
          this.mixPlay(this.model);
        }
        return true;
      };

      MixItemView.prototype.renderGenres = function() {
        var el;
        el = this.el;
        $.each(this.model.get("genre-list"), function(data) {
          $("#genre-list", el).append('<a href="/mixes/' + this.slug + '" class="label label-info arrowed-right arrowed-in">' + this.text + '</a>');
          return true;
        });
        return true;
      };

      MixItemView.prototype.renderComments = function() {
        var comments;
        comments = new CommentsCollection();
        comments.url = this.model.get("resource_uri") + "comments/";
        comments.mix_id = this.model.id;
        comments.mix = this.model;
        comments.fetch({
          success: function(data) {
            var content;
            content = new CommentsListView({
              collection: comments
            }).render();
            $("#comments", this.el).html(content.el);
            return true;
          }
        });
        return true;
      };

      MixItemView.prototype.doStart = function() {
        console.log("MixItemView: mixStart");
        this.ui.playButton.toggleClass('play-button-small-start', false).toggleClass('play-button-small-resume', false).toggleClass('play-button-small-pause', true);
        vent.trigger('mix:init', this.model);
      };

      MixItemView.prototype.doPause = function() {
        console.log("MixItemView: mixPause");
        vent.trigger("mix:pause", this.model);
        return true;
      };

      MixItemView.prototype.doResume = function() {
        console.log("MixItemView: mixResume");
        vent.trigger("mix:play", this.model);
        return true;
      };

      MixItemView.prototype.mixPlay = function(model) {
        if (this.model.get('id') === model.get('id')) {
          this.ui.playButton.toggleClass('play-button-small-start', false).toggleClass('play-button-small-resume', false).toggleClass('play-button-small-pause', true);
        }
      };

      MixItemView.prototype.mixPause = function(model) {
        if (this.model.get('id') === model.get('id')) {
          this.ui.playButton.toggleClass('play-button-small-start', false).toggleClass('play-button-small-resume', true).toggleClass('play-button-small-pause', false);
        }
      };

      MixItemView.prototype.mixStop = function(model) {
        if (this.model.get('id') === model.get('id')) {
          this.ui.playButton.toggleClass('play-button-small-start', true).toggleClass('play-button-small-resume', false).toggleClass('play-button-small-pause', false);
        }
      };

      MixItemView.prototype.mixFavourite = function() {
        var app;
        console.log("MixItemView: favouriteMix");
        app = require('app');
        vent.trigger("mix:favourite", this.model);
        return true;
      };

      MixItemView.prototype.mixLike = function() {
        console.log("MixItemView: likeMix");
        vent.trigger("mix:like", this.model);
        return true;
      };

      MixItemView.prototype.mixShare = function(e) {
        var mode;
        console.log("MixItemView: shareMix");
        mode = $(e.currentTarget).data("mode");
        console.log("MixItemView: " + mode);
        vent.trigger("mix:share", mode, this.model);
        return true;
      };

      MixItemView.prototype.mixDownload = function() {
        console.log("MixItemView: mixDownload");
        utils.downloadURL("/audio/download/" + this.model.get('id'));
        return true;
      };

      return MixItemView;

    })(Marionette.ItemView);
    return MixItemView;
  });

}).call(this);
