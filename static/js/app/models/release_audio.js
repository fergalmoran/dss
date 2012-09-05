var ReleaseAudio = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "release_audio/"
});

var ReleaseAudioCollection = TastypieCollection.extend({
    model:ReleaseAudio
});