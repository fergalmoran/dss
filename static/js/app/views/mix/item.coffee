define ['moment', 'app', 'marionette', 'models/comments/collection', 'views/comments/list', 'text!/tpl/MixListItemView'],
(moment, App, Marionette, CommentsCollection, CommentsListView, Template) ->
    class MixItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: @tagName or "li"
        className: @className or ""

        events: {
            "click .play-button-small-start": "startMix",
            "click .play-button-small-resume": "resumeMix",
            "click .play-button-small-pause": "pauseMix",
            "click .mix-link": "mixLink",
            "click .like-button a": "likeMix",
            "click .favourite-button a": "favouriteMix",
            "click .share-button": "shareMix",
            "click .download-button a": "downloadMix"
        }

        initialize: =>
            @listenTo(@model, 'change:favourited', @render)
            @listenTo(@model, 'change:liked', @render)
            true


        onRender: =>
            id = @model.get('id')
            if @model.get('duration')
                totalDuration = moment.duration(this.model.get('duration'), "seconds")
                totalDurationText = if totalDuration.hours() != 0 then moment(totalDuration).format("HH:mm:ss") else moment(totalDuration).format("mm:ss");
                $('#player-duration-' + id, this.el).text(totalDurationText)

            @renderGenres()
            return

        startMix: =>
            console.log("MixItemView: starting mix")
            id = @model.get('id')
            $.getJSON "/ajax/mix_stream_url/" + id + "/", (data) ->
                com.podnoms.settings.setupPlayer(data, id)
                com.podnoms.player.startPlaying
                    success: ->
                        window._eventAggregator.trigger "track_playing"
                        window._eventAggregator.trigger "track_changed", data
                        com.podnoms.utils.checkPlayCount()
                        return
                    error: ->
                        com.podnoms.utils.showWarning "Ooops", "Error playing mix. If you have a flash blocker, please disable it for this site. Otherwise, do please try again."

                com.podnoms.storage.setItem "now_playing", id
            return

        pauseMix: ->
            console.log("MixItemView: pauseMix")
            com.podnoms.player.pause();
            @.trigger("mix:paused", @model);
            true

        resumeMix: ->
            console.log("MixItemView: resumeMix")
            com.podnoms.player.resume();
            @trigger("mix:resumed", @model);
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
                $('#mix-tab a:first', @el).tab('show');
            true

        favouriteMix: ->
            console.log("MixItemView: favouriteMix")
            app = require('app')
            app.vent.trigger("mix:favourite", @model)
            true

        likeMix: ->
            console.log("MixItemView: likeMix")
            app = require('app')
            app.vent.trigger("mix:like", @model)
            true

        shareMix: (e) ->
            console.log("MixItemView: shareMix")
            mode = $(e.currentTarget).data("mode");
            console.log("MixItemView: "+ mode)
            app = require('app')
            app.vent.trigger("mix:share", mode, @model)
            true


    MixItemView
