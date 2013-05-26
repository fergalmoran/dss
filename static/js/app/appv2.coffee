define ['backbone', 'marionette', 'app.lib/router', 'app.lib/panningRegion', 'views/header', 'views/sidebar/sidebarView',
        'models/mix/mixCollection'],
(Backbone, Marionette, DssRouter, PanningRegion, HeaderView, SidebarView, MixCollection) ->
    Marionette.Region.prototype.open = (view) ->
        @.$el.hide();
        @.$el.html(view.el);
        @.$el.slideDown("fast");
        true

    App = new Marionette.Application();

    App.vent.on "mix:favourite", (model) ->
        console.log "App(vent): mix:favourite"
        model.save 'favourited', !model.get('favourited'), patch: true
        true

    App.vent.on "mix:like", (model) ->
        console.log "App(vent): mix:like"
        model.save 'liked', !model.get('liked'), patch: true
        true

    App.vent.on "mix:share", (mode, model) ->
        console.log "App(vent): mix:share"
        if (mode == "facebook")
            social.sharePageToFacebook(model);
        else if (mode == "twitter")
            social.sharePageToTwitter(model);
        true

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

    App.addRegions {
        headerRegion: "#header",
        contentRegion: {
            selector: "#content"
            #regionType: PanningRegion
        }
        sidebarRegion: "#sidebar"
    }

    App.addInitializer ->
        console.log("App: routing starting");
        App.Router = new DssRouter();
        return App.vent.trigger("routing:started");

    App.addInitializer ->
        console.log("App: gobbling links");
        $(document).on("click", "a[href]:not([data-bypass])", (evt) ->
            href = { prop: $(this).prop("href"), attr: $(this).attr("href") };
            root = location.protocol + "//" + location.host + (App.root || '/');
            if (href.prop.slice(0, root.length) == root)
                evt.preventDefault();
                App.Router.navigate(href.attr, true);
                true
        )
        true

    console.warn("Creating event aggregator shim")
    window._eventAggregator = _.extend({}, Backbone.Events);
    App.headerRegion.show(new HeaderView());
    sidebarView = new SidebarView();
    App.sidebarRegion.show(sidebarView)

    return App;
