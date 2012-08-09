window.ReleaseAudioItemView = Backbone.View.extend({
    tagName:"li",
    initialize:function () {
        $(this.el).data("id", this.model.get("id"));
        $(this.el).addClass("release-audio-entry");
    },
    render:function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});
window.ReleaseAudioListView = Backbone.View.extend({
    initialize:function () {
        this.render();

    },
    events: {
        "click a": "clicked"
    },
    clicked: function(e){
        e.preventDefault();
        this.renderItem($(e.currentTarget).attr("id"));
    },
    render:function () {
        $(this.el).html(this.template()).append('<ul class="release-audio-listing audio-listing"></ul>');
        var i=0;
        this.collection.each(function (item) {
            $('#release-audio-slide-nav', this.el).append('<li><a id="' + i++ + '"" class="selector-button" href="' + item.get('resource_uri') + '">' + (i) + '</a></li>');
        }, this);
        this.renderItem(0);
        return this;
    },
    renderItem: function(id){
        $('.release-audio-listing', this.el).empty();
        $('#' + id, this.el).blur();
        $('#' + id, this.el).addClass('on');
        $('a:not([id="' + id + '"]', this.el).removeClass('on');
        $('.release-audio-listing', this.el).append(new ReleaseAudioItemView({model:this.collection.models[id]}).render().el);
    }
});
