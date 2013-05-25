Backbone.Validate = function (model, changedAttributes) {

    return (function () {
        this.errors = {};
        this.attributes = _.clone(model.attributes);
        _.extend(this.attributes, changedAttributes);
        _.each(model.validates, function (value, rule) {
            this.validators[rule](value);
        });

        this.validators = {
            required: function (fields) {
                _.each(fields, function (field) {
                    if (_.isEmpty(this.attributes[field]) === true) {
                        this.addError(field, I18n.t('errors.form.required'));
                    }
                });
            }
        };

        this.addError = function (field, message) {
            if (_.isUndefined(this.errors[field])) {
                this.errors[field] = [];
            }
            this.errors[field].push(message);
        };

        return this.errors;
    })();
};

window.TastypieModel = Backbone.Model.extend({
    base_url: function () {
        var temp_url = Backbone.Model.prototype.url.call(this);
        return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url + '/');
    },
    url: function () {
        return this.base_url();
    }
});

window.TastypieCollection = Backbone.Collection.extend({
    parse: function (response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

window.DSSModel = window.TastypieModel.extend({
    addError: function (field, message) {
        if (_.isUndefined(this.errors[field])) {
            this.errors[field] = [];
        }
        this.errors[field].push(message);
        return field;
    }
});

