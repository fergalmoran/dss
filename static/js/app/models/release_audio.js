var ReleaseAudio = TastypieModel.extend({
    urlRoot:window.appSettings.urlRoot + "release_audio/"
});

var ReleaseAudioCollection = TastypieCollection.extend({
    model:ReleaseAudio
});