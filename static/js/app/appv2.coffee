define ['backbone', 'marionette', 'vent', 'utils'
        'app.lib/router', 'app.lib/panningRegion', 'app.lib/realtimeController', 'app.lib/audioController',
        'views/widgets/headerView', 'views/sidebar/sidebarView', 'models/mix/mixCollection'],
(Backbone, Marionette, vent, utils,
 DssRouter, PanningRegion, RealtimeController, AudioController,
 HeaderView, SidebarView, MixCollection) ->
    App = new Marionette.Application();
    App.audioController = new AudioController();
    App.realtimeController = new RealtimeController();
    App.realtimeController.startSocketIO();

    App.vent.on "routing:started", ->
        console.log "App(vent): routing:started"
        enablePushState = true;
        #Disable for older browsers
        pushState = !!(enablePushState && window.history && window.history.pushState)
        Backbone.history.start({
            pushState: pushState,
            hashChange: true
        })
        true

    App.addRegions
        headerRegion: "#header"
        contentRegion:
            selector: "#content"
        footerRegion: "#footer"
        sidebarRegion: "#sidebar"

    App.addInitializer ->
        console.log("App: routing starting");
        App.Router = new DssRouter();
        App.vent.trigger("routing:started");

    App.addInitializer ->
        $(document).on("click", "a[href]:not([data-bypass])", (evt) ->
            href = { prop: $(this).prop("href"), attr: $(this).attr("href") };
            root = location.protocol + "//" + location.host + (App.root || '/');
            if (href.prop.slice(0, root.length) == root)
                evt.preventDefault();
                App.Router.navigate(href.attr, true);
                true
        )
        true

    App.addInitializer ->
        @listenTo vent, "mix:favourite", (model) ->
            console.log "App(vent): mix:favourite"
            model.save 'favourited', !model.get('favourited'), patch: true
            true

        @listenTo vent, "mix:like", (model) ->
            console.log "App(vent): mix:like"
            model.save 'liked', !model.get('liked'), patch: true
            true

        @listenTo vent, "mix:share", (mode, model) ->
            console.log "App(vent): mix:share"
            if (mode == "facebook")
                social.sharePageToFacebook(model);
            else if (mode == "twitter")
                social.sharePageToTwitter(model);
            true

        @listenTo vent, "user:follow", (model)->
            console.log "App(vent): user:follow"
            model.save 'following', !model.get('following'), patch: true
            true

        @listenTo vent, "app:login", ->
            utils.modal "/dlg/LoginView"
            true

    App.headerRegion.show(new HeaderView());
    sidebarView = new SidebarView();
    App.sidebarRegion.show(sidebarView)

    return App;
