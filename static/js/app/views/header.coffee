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
        ui:
            liveButton: "#header-live-button"

        initialize: ->
            @render()
            @listenTo vent, "mix:play", @trackPlaying
            @listenTo vent, "mix:pause", @trackPaused

        login: ->
            utils.modal "/dlg/LoginView"

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
            $(@ui.liveButton).toggleClass('btn-success')
                             .toggleClass('btn-warning')

            vent.trigger('live:play')

    HeaderView