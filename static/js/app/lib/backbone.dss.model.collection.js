define(['backbone'], function (Backbone) {
    return Backbone.Collection.extend({
        parse: function (response) {
            this.meta = response.meta || {};
            this.page_count = this.meta.total_count / this.meta.limit;
            return response.objects || response;
        }
    });
});
