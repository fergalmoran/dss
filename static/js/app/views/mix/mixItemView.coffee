define ['moment', 'app', 'vent', 'marionette', 'utils', 'models/comment/commentCollection', 'views/comment/commentListView', 'text!/tpl/MixListItemView'],
(moment, App, vent, Marionette, utils, CommentsCollection, CommentsListView, Template) ->
    class MixItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: @tagName or "li"
        className: @className or ""

        events: {
            "click .play-button-small-start": "doStart",
            "click .play-button-small-resume": "doResume",
            "click .play-button-small-pause": "doPause",
            "click .mix-link": "mixLink",
            "click .like-button a": "mixLike",
            "click .favourite-button a": "mixFavourite",
            "click .share-button": "mixShare",
            "click .download-button a": "mixDownload"
        }

        ui: {
            playButton: ".play-button-small"
        }

        initialize: =>
            @listenTo(@model, 'change:favourited', @render)
            @listenTo(@model, 'change:liked', @render)
            @listenTo(vent, 'mix:play', @mixPlay)
            @listenTo(vent, 'mix:pause', @mixPause)
            true

        onRender: =>
            id = @model.get('id')
            if @model.get('duration')
                totalDuration = moment.duration(this.model.get('duration'), "seconds")
                totalDurationText = if totalDuration.hours() != 0 then moment(totalDuration).format("HH:mm:ss") else moment(totalDuration).format("mm:ss");
                $('#player-duration-' + id, this.el).text(totalDurationText)


            @renderGenres()
            return

        onShow: ->
            #check if we're currently playing
            if com.podnoms.player.isPlayingId @model.id
                com.podnoms.settings.setupPlayerWrapper @model.get('id'), com.podnoms.player.getStreamUrl(), @el
                @mixPlay(@model)
            true

        renderGenres: =>
            el = @el
            $.each @model.get("genre-list"), (data) ->
                $("#genre-list", el).append '<a href="/mixes/' + @slug + '" class="dss-tag-button">' + @text + '</a>'
                true
            true

        renderComments: =>
            comments = new CommentsCollection()
            comments.url = @model.get("resource_uri") + "comments/"
            comments.mix_id = @model.id
            comments.mix = @model.get("resource_uri")
            comments.fetch success: (data) ->
                console.log(data)
                content = new CommentsListView(collection: comments).render()
                $("#comments", @el).html content.el
                true
            true

        doStart: =>
            console.log("MixItemView: mixStart")
            this.ui.playButton
                .toggleClass('play-button-small-start', false)
                .toggleClass('play-button-small-resume', false)
                .toggleClass('play-button-small-pause', true)

            vent.trigger('mix:init', @model)
            return

        doPause: ->
            console.log("MixItemView: mixPause")
            vent.trigger("mix:pause", @model);
            true

        doResume: ->
            console.log("MixItemView: mixResume")
            vent.trigger("mix:play", @model);
            true

        mixPlay: (model) ->
            if (@model.get('id') == model.get('id'))
                this.ui.playButton
                    .toggleClass('play-button-small-start', false)
                    .toggleClass('play-button-small-resume', false)
                    .toggleClass('play-button-small-pause', true)
            return

        mixPause: (model) ->
            if (@model.get('id') == model.get('id'))
                this.ui.playButton
                    .toggleClass('play-button-small-start', false)
                    .toggleClass('play-button-small-resume', true)
                    .toggleClass('play-button-small-pause', false)
            return

        mixFavourite: ->
            console.log("MixItemView: favouriteMix")
            app = require('app')
            vent.trigger("mix:favourite", @model)
            true

        mixLike: ->
            console.log("MixItemView: likeMix")
            vent.trigger("mix:like", @model)
            true

        mixShare: (e) ->
            console.log("MixItemView: shareMix")
            mode = $(e.currentTarget).data("mode");
            console.log("MixItemView: "+ mode)
            vent.trigger("mix:share", mode, @model)
            true

        mixDownload: ->
            console.log("MixItemView: mixDownload")
            utils.downloadURL("/audio/download/" + @model.get('id'))
            true


    MixItemView
