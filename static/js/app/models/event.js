var Event = DSSModel.extend({
    urlRoot:window.appSettings.urlRoot + "event/"
});
var EventCollection = TastypieCollection.extend({
    url:window.appSettings.urlRoot + "event/",
    model:Event
});
