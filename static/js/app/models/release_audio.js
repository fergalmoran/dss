/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var ReleaseAudio = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "release_audio/"
});

var ReleaseAudioCollection = TastypieCollection.extend({
    model:ReleaseAudio
});