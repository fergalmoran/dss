define(['backbone'], function (Backbone) {

    var TastypieModel = Backbone.Model.extend({
        base_url: function () {
            var temp_url = Backbone.Model.prototype.url.call(this);
            return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url + '/');
        },
        url: function () {
            return this.base_url();
        }
    });

    var TastypieCollection = Backbone.Collection.extend({
        parse: function (response) {
            this.meta = response.meta || {};
            return response.objects || response;
        }
    });

    return TastypieModel.extend({
        addError: function (field, message) {
            if (_.isUndefined(this.errors[field])) {
                this.errors[field] = [];
            }
            this.errors[field].push(message);
            return field;
        }
    });
});
