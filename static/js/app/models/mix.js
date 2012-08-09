window.Mix = TastypieModel.extend({
    urlRoot:window.appSettings.urlRoot + "mix/"
});
window.MixCollection = TastypieCollection.extend({
    url:window.appSettings.urlRoot + "mix/",
    model:Mix
});
