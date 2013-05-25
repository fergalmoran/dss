// Generated by CoffeeScript 1.3.3
(function() {

  define(['backbone', 'marionette', 'app.lib/router', 'app.lib/panningRegion', 'views/header', 'views/sidebar/sidebar', 'models/mix/collection'], function(Backbone, Marionette, DssRouter, PanningRegion, HeaderView, SidebarView, MixCollection) {
    var App, sidebarView;
    Marionette.Region.prototype.open = function(view) {
      this.$el.hide();
      this.$el.html(view.el);
      this.$el.slideDown("fast");
      return true;
    };
    App = new Marionette.Application();
    App.vent.on("mix:favourite", function(model) {
      console.log("App(vent): mix:favourite");
      model.save('favourited', !model.get('favourited'), {
        patch: true
      });
      return true;
    });
    App.vent.on("mix:like", function(model) {
      console.log("App(vent): mix:like");
      model.save('liked', !model.get('liked'), {
        patch: true
      });
      return true;
    });
    App.vent.on("mix:share", function(mode, model) {
      console.log("App(vent): mix:share");
      if (mode === "facebook") {
        social.sharePageToFacebook(model);
      } else if (mode === "twitter") {
        social.sharePageToTwitter(model);
      }
      return true;
    });
    App.vent.on("routing:started", function() {
      var enablePushState, pushState;
      console.log("App(vent): routing:started");
      enablePushState = true;
      pushState = !!(enablePushState && window.history && window.history.pushState);
      Backbone.history.start({
        pushState: pushState,
        hashChange: true
      });
      return true;
    });
    App.addRegions({
      headerRegion: "#header",
      contentRegion: {
        selector: "#content"
      },
      sidebarRegion: "#sidebar"
    });
    App.addInitializer(function() {
      console.log("App: routing starting");
      App.Router = new DssRouter();
      return App.vent.trigger("routing:started");
    });
    App.addInitializer(function() {
      console.log("App: gobbling links");
      $(document).on("click", "a[href]:not([data-bypass])", function(evt) {
        var href, root;
        href = {
          prop: $(this).prop("href"),
          attr: $(this).attr("href")
        };
        root = location.protocol + "//" + location.host + (App.root || '/');
        if (href.prop.slice(0, root.length) === root) {
          evt.preventDefault();
          App.Router.navigate(href.attr, true);
          return true;
        }
      });
      return true;
    });
    console.warn("Creating event aggregator shim");
    window._eventAggregator = _.extend({}, Backbone.Events);
    App.headerRegion.show(new HeaderView());
    sidebarView = new SidebarView();
    App.sidebarRegion.show(sidebarView);
    return App;
  });

}).call(this);
