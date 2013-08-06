// Generated by CoffeeScript 1.6.2
(function() {
  define(['backbone', 'marionette', 'vent', 'utils', 'app.lib/social', 'app.lib/router', 'app.lib/panningRegion', 'app.lib/realtimeController', 'app.lib/audioController', 'models/user/userItem', 'models/mix/mixCollection', 'views/widgets/headerView', 'views/sidebar/sidebarView'], function(Backbone, Marionette, vent, utils, social, DssRouter, PanningRegion, RealtimeController, AudioController, UserItem, MixCollection, HeaderView, SidebarView) {
    var App, sidebarView;

    App = new Marionette.Application();
    App.audioController = new AudioController();
    App.realtimeController = new RealtimeController();
    App.realtimeController.startSocketIO();
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
      footerRegion: "#footer",
      sidebarRegion: "#sidebar"
    });
    App.addInitializer(function() {
      console.log("App: routing starting");
      App.Router = new DssRouter();
      return App.vent.trigger("routing:started");
    });
    App.addInitializer(function() {
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
    App.addInitializer(function() {
      this.listenTo(vent, "app:login", function() {
        utils.modal("/dlg/LoginView");
        return true;
      });
      this.listenTo(vent, "mix:favourite", function(model) {
        console.log("App(vent): mix:favourite");
        model.save('favourited', !model.get('favourited'), {
          patch: true
        });
        return true;
      });
      this.listenTo(vent, "mix:like", function(model) {
        console.log("App(vent): mix:like");
        model.save('liked', !model.get('liked'), {
          patch: true
        });
        return true;
      });
      this.listenTo(vent, "user:follow", function(model) {
        var target, user,
          _this = this;

        console.log("App(vent): user:follow");
        user = new UserItem({
          id: com.podnoms.settings.currentUser
        });
        target = com.podnoms.settings.urlRoot + "user/" + model.get("id") + "/";
        user.fetch({
          success: function() {
            var f, newFollowers;

            if (!model.get("is_following")) {
              newFollowers = user.get("following").concat([target]);
              user.save({
                "following": newFollowers,
                "is_following": true,
                patch: true
              });
              model.set("is_following", true);
            } else {
              f = user.get("following");
              f.splice(f.indexOf(target), 1);
              user.save({
                "following": f,
                "is_following": false,
                patch: true
              });
              model.set("is_following", false);
            }
          }
        });
        return true;
      });
      return this.listenTo(vent, "mix:share", function(mode, model) {
        console.log("App(vent): mix:share (" + mode + ")");
        if (mode === "facebook") {
          social.sharePageToFacebook(model);
        } else if (mode === "twitter") {
          social.sharePageToTwitter(model);
        } else if (mode === "embed") {
          social.generateEmbedCode(model);
        }
        return true;
      });
    });
    App.headerRegion.show(new HeaderView());
    sidebarView = new SidebarView();
    App.sidebarRegion.show(sidebarView);
    return App;
  });

}).call(this);
