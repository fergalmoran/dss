###
@license

----------------------------------------------

Copyright (c) 2012, Fergal Moran. All rights reserved.
Code provided under the BSD License:
###
define ["underscore", "marionette", "vent", "utils", "views/widgets/searchView",
        "views/notifications/notificationsListView", "text!/tpl/HeaderView"],
(_, Marionette, vent, utils, SearchView, NotificationsListView, Template) ->
    class HeaderView extends Marionette.Layout
        NowrapRegion = Marionette.Region.extend(open: (view) ->
            debugger
            @$el.html view.$el.html()
        )
        template: _.template(Template)
        events:
            "click #header-play-pause-button": "togglePlayState"
            "click #header-login-button": "login"
            "click #header-live-button.btn-success": "playLive"
            "click #header-live-button.btn-danger": "pauseLive"
        ui:
            liveButton: "#header-live-button"

        regions:
            searchRegion: "#header-search"
            notificationsRegion:
                selector: "#header-notifications"
                #regionType: NowrapRegion

        initialize: ->
            @render()
            @listenTo vent, "mix:play", @trackPlaying
            @listenTo vent, "mix:pause", @trackPaused

        onShow: ->
            @searchRegion.show(new SearchView())
            if com.podnoms.settings.currentUser != -1
                @notificationsRegion.show(new NotificationsListView())

        login: ->
            vent.trigger('app:login')

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
            console.log("HeaderView: playLive")
            $(@ui.liveButton).toggleClass('btn-success', false)
            .toggleClass('btn-danger', true)

            vent.trigger('live:play')

        pauseLive: ->
            console.log("HeaderView: pauseLive")
            $(@ui.liveButton).toggleClass('btn-success', true)
            .toggleClass('btn-danger', false)

            vent.trigger('live:pause')

    HeaderView