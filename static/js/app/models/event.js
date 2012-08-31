var Event = DSSModel.extend({
    urlRoot:window.appSettings.urlRoot + "event/",
    isValid:function () {
        this.errors = {};
        if (isEmpty(this.get('event_description'))) {
            return this.addError('event_description', 'Please enter description');
        }
        return "";
    }
});
var EventCollection = TastypieCollection.extend({
    url:window.appSettings.urlRoot + "event/",
    model:Event
});
