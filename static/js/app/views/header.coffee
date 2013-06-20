###
@license

----------------------------------------------

Copyright (c) 2012, Fergal Moran. All rights reserved.
Code provided under the BSD License:
###
define ["underscore", "backbone", "vent", "utils", "text!/tpl/HeaderView"],
(_, Backbone, vent, utils, Template) ->
    class HeaderView extends Backbone.View
        template: _.template(Template)
        events:
            "click #header-play-pause-button": "togglePlayState"
            "click #header-login-button": "login"
            "click #header-live-button": "playLive"

        initialize: ->
            @render()
            @listenTo vent, "mix:play", @trackPlaying
            @listenTo vent, "mix:pause", @trackPaused

        login: ->
            utils.modal "dlg/LoginView"

        logout: ->
            utils.showAlert "Success", "You are now logged out"

        trackChanged: (data) ->
            $(@el).find("#track-description").text data.title
            $(@el).find("#track-description").attr "href", "#" + data.item_url

        trackPlaying: (data) ->
            $(@el).find("#header-play-button-icon").removeClass "icon-play"
            $(@el).find("#header-play-button-icon").addClass "icon-pause"

        trackPaused: (data) ->
            $(@el).find("#header-play-button-icon").removeClass "icon-pause"
            $(@el).find("#header-play-button-icon").addClass "icon-play"

        render: ->
            $(@el).html @template()
            this

        playLive: ->
            vent.trigger('live:play')

        togglePlayState: ->
            button = $(@el).find("#header-play-pause-button")
            mode = button.data("mode")
            if mode is "play"
                dssSoundHandler.resumeSound()
                _eventAggregator.trigger "track_playing"
                button.data "mode", "pause"
            else
                dssSoundHandler.pauseSound()
                _eventAggregator.trigger "track_paused"
                button.data "mode", "play"

    HeaderView