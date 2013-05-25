define(['backbone'], function (Backbone) {
    return Backbone.Collection.extend({
        parse: function (response) {
            this.recent_meta = response.meta || {};
            return response.objects || response;
        }
    });
});
