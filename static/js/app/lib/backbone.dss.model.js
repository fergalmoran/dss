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

    return TastypieModel.extend({
        addError: function (field, message) {
            if (_.isUndefined(this.errors[field])) {
                this.errors[field] = [];
            }
            this.errors[field].push(message);
            return field;
        },
        secondsToHms: function (field) {
            var d = this.get(field);
            if (d) {
                d = Number(d);
                var h = Math.floor(d / 3600);
                var m = Math.floor(d % 3600 / 60);
                var s = Math.floor(d % 3600 % 60);
                return ((h > 0 ? h + ":" : "") + (m > 0 ? (h > 0 && m < 10 ? "0" : "") + m + ":" : "0:") + (s < 10 ? "0" : "") + s);
            }else{
                return "00:00:00";
            }
        }
    });
});
