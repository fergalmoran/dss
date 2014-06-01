@Dss.module "HeaderApp.Views", (Views, App, Backbone, Marionette, $, _, vent) ->
    class Views.Header extends Marionette.Layout
        template: "header"
        className: "navbar navbar-default"
        events:
            "click #header-random-button": "showRandom"
            "click #header-play-pause-button": "togglePlayState"
            "click #header-login-button": "login"
            "click #header-logout-button": "logout"
            "click #header-donate-button": "donate"
            "click #header-live-button.btn-success": "playLive"
            "click #header-live-button.btn-danger": "pauseLive"
        ui:
            liveButton: "#header-live-button"

        regions:
            searchRegion: "#header-search"
            notificationsRegion:
                selector: "#header-notifications"

        initialize: ->
            @listenTo App.vent, "live:stop", @liveStopped
            @listenTo App.vent, "mix:play", @trackPlaying
            @listenTo App.vent, "mix:pause", @trackPaused

        onShow: ->
            @searchRegion.show(new App.SearchApp.Views.SearchView())
            if com.podnoms.settings.currentUser != -1
                @notificationsRegion.show(new App.NotificationApp.Views.NotificationsListView())

        showRandom: ->
            console.log("headerView: showRandom")
            App.vent.trigger("mix:random")

        login: ->
            App.vent.trigger('app:login')

        logout: ->
            App.vent.trigger('app:logout')

        donate: ->
            App.vent.trigger('app:donate')

        trackChanged: (data) ->
            $(@el).find("#track-description").text data.title
            $(@el).find("#track-description").attr "href", "#" + data.item_url

        trackPlaying: (data) ->
            $(@el).find("#header-play-button-icon").removeClass "fa-play"
            $(@el).find("#header-play-button-icon").addClass "fa-pause"

        trackPaused: (data) ->
            $(@el).find("#header-play-button-icon").removeClass "fa-pause"
            $(@el).find("#header-play-button-icon").addClass "fa-play"

        playLive: ->
            console.log("HeaderView: playLive")
            $(@ui.liveButton).toggleClass('btn-success', false).toggleClass('btn-danger', true)

            App.vent.trigger('live:play')

        pauseLive: ->
            console.log("HeaderView: pauseLive")
            $(@ui.liveButton).toggleClass('btn-success', true).toggleClass('btn-danger', false)

            App.vent.trigger('live:pause')

        liveStopped: ->
            console.log("HeaderView: liveStopped")
            $(@ui.liveButton).toggleClass('btn-success', true).toggleClass('btn-danger', false)

    Views.Header
