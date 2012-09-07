var AppRouter = Backbone.Router.extend({
    routes:{
        "/mixes":"mixList",
        "/mixes/:type":"mixList",
        "/mix/upload":"mixUpload",
        "/mix/:id":"mixDetails",
        "/mix/edit/:id":"mixEdit",
        "/releases":"releaseList",
        "/release/add":"releaseAdd",
        "/release/:id":"releaseDetails",
        "/events":"eventList",
        "/event/add":"eventAdd",
        "/event/:id":"eventDetails",
        "/accounts/social/connections/":"connectAccounts",
        "/accounts/login/":"login",
        "/accounts/logout/":"logout",
        "/me":"userDetails",
        "*path":"defaultRoute"
    },
    initialize:function () {
        this.headerView = new HeaderView();
        $('#header').html(this.headerView.el);
        $('#site-content-fill').html('');
        this.bind('all', this.trackPageView);

    },
    trackPageView:function () {
        var url;
        url = Backbone.history.getFragment();
        return com.podnoms.utils.trackPageView(url);
    },
    defaultRoute:function (path) {
        if (path == undefined || path == "" || path == "/")
            this.mixList('latest');
    },
    mixList:function (type) {
        var mixList = new MixCollection();
        mixList.type = type || 'latest';
        $('#site-content-fill').html('');
        //this.sidebarView = new SidebarView();
        //$('#sidebar').html(this.sidebarView.el);
        var data = type != undefined ? $.param({sort:type}) : null;
        mixList.fetch({
            data:data,
            success:function () {
                var mixes = new MixListView({collection:mixList});
                var content = mixes.el;
                $('#content').html(content);
                if (mixes.itemPlaying != null){
                    com.podnoms.settings.setupPlayer(mixes.itemPlaying.toJSON(), mixes.itemPlaying.get('id'));
                }
            }
        });
    },
    mixDetails:function (id) {
        var mix = new Mix({id:id});
        mix.fetch({
            success:function () {
                var html = new MixView({model:mix});
                $('#content').html(html.el);
                $('#site-content-fill').html('');

                if (com.podnoms.player.isPlayingId(mix.get('id'))){
                    com.podnoms.settings.setupPlayer(mix.toJSON(), mix.get('id'));
                }

                var comments = new CommentCollection();
                comments.url = com.podnoms.settings.urlRoot + mix.attributes.item_url + "/comments/";
                comments.mix_id = id;
                comments.mix = mix.get("resource_uri");
                comments.fetch({success:function (data) {
                    var content = new CommentListView({collection:comments}).render();
                    $('#site-content-fill').html(content.el);
                }});
            }});
    },
    mixUpload:function (id) {
        var html = new MixCreateView({model:new Mix()});
        $('#content').html(html.el);
        $('#site-content-fill').html('');
    },
    mixEdit:function (id) {
        var mix = new Mix({id:id});
        mix.fetch({
            success:function () {
                var html = new MixCreateView({model:mix});
                $('#content').html(html.el);
                $('#site-content-fill').html('');
            }
        });
    },
    releaseList:function (page) {
        var releaseList = new ReleaseCollection();
        releaseList.fetch({
            success:function () {
                var content = new ReleaseListView({collection:releaseList}).el;
                $('#content').html(content);
            }
        });
    },
    releaseDetails:function (id) {
        var release = new Release({id:id});
        $('#site-content-fill').html('');
        release.fetch({success:function () {
            var content = new ReleaseView({model:release}).el;
            $('#content').html(content);
            /*
             var audio = new ReleaseAudioCollection();
             audio.url = com.podnoms.settings.urlRoot + release.attributes.item_url + "/release_audio/";
             audio.audio_id = id;
             audio.release = release.get("resource_uri");
             audio.fetch({success:function (data) {
             var content = new ReleaseAudioListView({collection:audio});
             $('#release-description').html(content.el);
             }});
             */
        }});
    },
    releaseAdd:function () {
        var html = new ReleaseCreateView({model:new Release({ release_date:com.podnoms.utils.getDateAsToday() })});
        $('#content').html(html.el);
        $('#site-content-fill').html('');
    },
    eventList:function (page) {
        var eventList = new EventCollection();
        eventList.fetch({
            success:function () {
                var content = new EventListView({collection:eventList}).el;
                $('#content').html(content);
            }
        });
    },
    eventDetails:function (id) {
        var event = new Event({id:id});
        $('#site-content-fill').html('');
        event.fetch({success:function () {
            var content = new EventView({model:event}).el;
            $('#content').html(content);
        }});
    },
    eventAdd:function () {
        var html = new EventCreateView({model:new Event({ event_date:com.podnoms.utils.getDateAsToday() })});
        $('#content').html(html.el);
        $('#site-content-fill').html('');
    },
    login:function () {
        $.colorbox({
            href:"/tpl/LoginView/",
            onClosed:function () {
                app.navigate('/');
            }
        })
    },
    logout:function () {
        com.podnoms.utils.showAlert("Success", "You are now logged out", "alert-success");
    },
    connectAccounts:function () {
        alert("sdfkjsdlfj");
    },
    userDetails:function () {
        var user = new User();
        $('#site-content-fill').html('');
        user.fetch({success:function () {
            var content = new UserView({model:user}).el;
            $('#content').html(content);
        }});
    }
});

com.podnoms.utils.loadTemplate([
    'HeaderView', 'SidebarView', 'UserView',
    'MixListView', 'MixListItemView', 'MixView', 'MixCreateView',
    'CommentListView', 'CommentListItemView',
    'ReleaseListView', 'ReleaseListItemView', 'ReleaseItemView', 'ReleaseView', 'ReleaseCreateView', 'ReleaseAudioListView', 'ReleaseAudioItemView',
    'EventCreateView', 'EventListView', 'EventListItemView', 'EventView', 'EventItemView'
], function () {
        window.app = new AppRouter();
        Backbone.history.start();
    }
);
var _eventAggregator = _.extend({}, Backbone.Events);
