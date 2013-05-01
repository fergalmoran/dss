/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var AppRouter = Backbone.Router.extend({
    root: '/',
    routes: {
        "debug": "debug",
        "mixes": "mixList",
        "mixes/:type": "mixList",
        "mix/upload": "mixUpload",
        "mix/:id": "mixDetails",
        "mix/edit/:id": "mixEdit",
        "releases": "releaseList",
        "release/add": "releaseAdd",
        "release/edit/:id": "releaseEdit",
        "release/:id": "releaseDetails",
        "events": "eventList",
        "event/add": "eventAdd",
        "event/:id": "eventDetails",
        //"accounts/social/connections/": "connectAccounts",
        //"accounts/facebook/login": "loginRedirect",
        //"accounts/twitter/login": "loginRedirect",
        //"accounts/login/": "login",
        //"accounts/logout/": "logout",
        "user/:id": "user",
        "upload/": "defaultRoute",
        "me": "userDetails",
        "*path": "defaultRoute"
    },
    initialize: function () {
        this.headerView = new HeaderView();
        $('#header').html(this.headerView.el);
        $('#site-content-fill').html('');
        this.bind('all', this.trackPageView);
    },
    trackPageView: function () {
        var url;
        url = Backbone.history.getFragment();
        return com.podnoms.utils.trackPageView(url);
    },
    defaultRoute: function (path) {
        if (path == undefined || path == "" || path == "/")
            this.mixList('latest');
        else {
            $.get('/tpl/404/', function (data) {
                $('#content').html(_.template(data));
            });

        }
    },
    debug: function () {
        var model = new User({
            id: 'fergalmoran'
        });
        model.fetch({
            success: function(){
                var content= new SidebarViewUser({
                    model: model
                });
                $('#content').html(content.render().el);
            }
        });
    },
    user: function (user) {
        this._renderMixList('latest', { "user": user });
        var model = new User({
            id: user
        });
        model.fetch({
            success: function(){
                var content= new SidebarViewUser({
                    model: model
                });
                $('#sidebar').html(content.render().el);
            }
        });
    },
    userDetails: function () {
        var user = new User({
            id: com.podnoms.settings.currentUser
        });
        $('#site-content-fill').html('');
        user.fetch({
            success: function () {
                var content = new UserView({
                    model: user
                });
                $('#content').html(content.render().el);
            }
        });
    },
    mixList: function (type) {
        this._renderMixList(type);
        this.sidebarView = new SidebarView();
        $('#sidebar').html(this.sidebarView.el);
        startChat(
            $('#chat-messages-body', this.sidebarView.el),
            $('#input', this.sidebarView.el),
            $('#status', this.sidebarView.el),
            $('#header-profile-edit').text());
    },
    _renderMixList: function (type, data) {
        var mixList = new MixCollection();
        mixList.type = type || 'latest';
        $('#site-content-fill').html('');

        var payload = $.extend(type != undefined ? {type: type} : null, data);
        mixList.fetch({
            data: payload,
            success: function () {
                var mixes = new MixListView({
                    collection: mixList
                });
                $('#content').html(mixes.el);
                if (mixes.itemPlaying != null) {
                    com.podnoms.settings.setupPlayer(mixes.itemPlaying.toJSON(), mixes.itemPlaying.get('id'));
                }
            }
        });
    },
    mixDetails: function (id) {
        var mix = new Mix({
            id: id
        });
        mix.fetch({
            success: function () {
                var html = new MixView({
                    model: mix
                });
                $('#content').html(html.el);
                $('#site-content-fill').html('');

                if (com.podnoms.player.isPlayingId(mix.get('id'))) {
                    com.podnoms.settings.setupPlayer(mix.toJSON(), mix.get('id'));
                }
            }
        });
    },
    mixUpload: function () {
        var html = new MixCreateView({
            model: new Mix()
        });
        $('#content').html(html.el);
        $('#site-content-fill').html('');
    },
    mixEdit: function (id) {
        var mix = new Mix({
            slug: id
        });
        mix.fetch({
            success: function () {
                var html = new MixCreateView({
                    model: mix
                });
                $('#content').html(html.el);
                $('#site-content-fill').html('');
            }
        });
    },
    releaseList: function (page) {
        var releaseList = new ReleaseCollection();
        releaseList.fetch({
            success: function () {
                var content = new ReleaseListView({
                    collection: releaseList
                }).el;
                $('#content').html(content);
            }
        });
    },
    releaseDetails: function (id) {
        var release = new Release({
            id: id
        });
        $('#site-content-fill').html('');
        release.fetch({
            success: function () {
                var content = new ReleaseView({
                    model: release
                }).el;
                $('#content').html(content);
            }
        });
    },
    releaseAdd: function () {
        var html = new ReleaseCreateView({
            model: new Release({
                release_date: com.podnoms.utils.getDateAsToday()
            })
        });
        $('#content').html(html.el);
        $('#site-content-fill').html('');
    },
    releaseEdit: function (id) {
        var release = new Release({
            id: id
        });
        release.fetch({
            success: function () {
                var html = new ReleaseCreateView({
                    model: release
                });
                $('#content').html(html.el);
                $('#site-content-fill').html('');
            }
        });
    },
    eventList: function (page) {
        var eventList = new EventCollection();
        eventList.fetch({
            success: function () {
                var content = new EventListView({
                    collection: eventList
                }).el;
                $('#content').html(content);
            }
        });
    },
    eventDetails: function (id) {
        var event = new Event({
            id: id
        });
        $('#site-content-fill').html('');
        event.fetch({
            success: function () {
                var content = new EventView({
                    model: event
                }).el;
                $('#content').html(content);
            }
        });
    },
    eventAdd: function () {
        var html = new EventCreateView({
            model: new Event({
                event_date: com.podnoms.utils.getDateAsToday()
            })
        });
        $('#content').html(html.el);
        $('#site-content-fill').html('');
    },
    loginRedirect: function () {
        com.podnoms.utils.showAlert("Success", "Thank you for logging in.");
        this.defaultRoute();
    },
    connectAccounts: function () {
        alert("Connecting accounts");
    }
});

com.podnoms.utils.loadTemplate(['HeaderView', 'SidebarView', 'SidebarViewUser', 'UserView', 'MixListView', 'MixListItemView', 'MixView', 'MixCreateView', 'CommentListView', 'CommentListItemView', 'ActivityListView', 'ActivityListItemView', 'ReleaseListView', 'ReleaseListItemView', 'ReleaseItemView', 'ReleaseView', 'ReleaseCreateView', 'ReleaseAudioListView', 'ReleaseAudioItemView', 'EventCreateView', 'EventListView', 'EventListItemView', 'EventView', 'EventItemView'], function () {
    window.app = new AppRouter();
    // Trigger the initial route and enable HTML5 History API support, set the
    // root folder to '/' by default.  Change in app.js.
    var enablePushState = true;
    // Disable for older browsers
    var pushState = !!(enablePushState && window.history && window.history.pushState);
    Backbone.history.start({ pushState: pushState, root: app.root, hashChange: true });

    // All navigation that is relative should be passed through the navigate
    // method, to be processed by the router. If the link has a `data-bypass`
    // attribute, bypass the delegation completely.
    $(document).on("click", "a[href]:not([data-bypass])", function (evt) {
        // Get the absolute anchor href.
        var href = { prop: $(this).prop("href"), attr: $(this).attr("href") };
        // Get the absolute root.
        var root = location.protocol + "//" + location.host + app.root;

        // Ensure the root is part of the anchor href, meaning it's relative.
        if (href.prop.slice(0, root.length) === root) {
            // Stop the default event to ensure the link will not cause a page
            // refresh.
            evt.preventDefault();

            // `Backbone.history.navigate` is sufficient for all Routers and will
            // trigger the correct events. The Router's internal `navigate` method
            // calls this anyways.  The fragment is sliced from the root.
            Backbone.history.navigate(href.attr, true);
        }
    });
});
var _eventAggregator = _.extend({}, Backbone.Events);
