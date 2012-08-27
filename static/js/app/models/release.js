var Release = TastypieModel.extend({
    urlRoot:window.appSettings.urlRoot + "release/"
});
var ReleaseCollection = TastypieCollection.extend({
    url:window.appSettings.urlRoot + "release/",
    model:Release
});
