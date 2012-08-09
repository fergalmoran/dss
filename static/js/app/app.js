var AppRouter = Backbone.Router.extend({
    routes:{
        "application/":"defaultRoute",
        "/mixes":"mixList",
        "/mixes/:type":"mixList",
        "/mix/:id":"mixDetails",
        "/releases":"releaseList",
        "/release/:id":"releaseDetails",
        "/accounts/login/":"login",
        "/accounts/logout/":"logout"
    },
    initialize:function () {
        this.headerView = new HeaderView();
        $('#header').html(this.headerView.el);
        this.sidebarView = new SidebarView();
        //$('#sidebar').html(this.sidebarView.el);
        $('#site-content-fill').html('');
    },
    defaultRoute:function (path) {
        if (path == "" || path == "/")
            this.mixList(0);
    },
    mixList:function (type) {
        var mixList = new MixCollection();
        mixList.type = type || 'latest';
        $('#site-content-fill').html('');
        var data = type != undefined ? $.param({sort: type}) : null;
        mixList.fetch({
            data: data,
            success:function () {
                var content = new MixListView({collection:mixList}).el;
                $('#content').html(content);
            }
        });
    },
    mixDetails:function (id) {
        var mix = new Mix({id:id});
        mix.fetch({success:function () {
            var html = new MixView({model:mix});
            $('#content').html(html.el);
            $('#site-content-fill').html('');
            var comments = new CommentCollection();
            comments.url = window.appSettings.urlRoot + mix.attributes.item_url + "/comments/";
            comments.mix_id = id;
            comments.mix = mix.get("resource_uri");
            comments.fetch({success:function (data) {
                var content = new CommentListView({collection:comments}).render();
                $('#site-content-fill').html(content.el);
            }});
        }});
    },
    releaseList:function (page) {

    },
    releaseDetails:function (id) {
        var release = new Release({id:id});
        $('#site-content-fill').html('');
        release.fetch({success:function () {
            var content = new ReleaseView({model:release}).el;
            $('#content').html(content);
            var audio = new ReleaseAudioCollection();
            audio.url = window.appSettings.urlRoot + release.attributes.item_url + "/release_audio/";
            audio.audio_id = id;
            audio.release = release.get("resource_uri");
            audio.fetch({success:function (data) {
                var content = new ReleaseAudioListView({collection:audio});
                $('#release-description').html(content.el);
            }});
        }});
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
        window.utils.showAlert("Success", "You are now logged out", "alert-success");
    }
});

utils.loadTemplate([
    'HeaderView', 'SidebarView',
    'MixListView', 'MixItemView', 'MixView',
    'CommentListView', 'CommentItemView',
    'ReleaseListView', 'ReleaseItemView', 'ReleaseView', 'ReleaseAudioListView', 'ReleaseAudioItemView'], function () {
    window.app = new AppRouter();
    Backbone.history.start();
});
var _eventAggregator = _.extend({}, Backbone.Events);
