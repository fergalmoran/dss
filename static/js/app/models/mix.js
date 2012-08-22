window.Mix = TastypieModel.extend({
    urlRoot:window.appSettings.urlRoot + "mix/",
    schema:{
        title:'Text',
        description:'Text'
    }
});
window.MixCollection = TastypieCollection.extend({
    url:window.appSettings.urlRoot + "mix/",
    model:Mix
});
