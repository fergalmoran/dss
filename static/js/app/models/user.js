/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
var User = DSSModel.extend({
    urlRoot:com.podnoms.settings.urlRoot + "user/",
    isValid: function () {
        this.errors = {};
        return "";
    },
    avatarGravatar: function(){
        return this.get('profile').avatar_type == 'gravatar';
    },
    avatarSocial: function(){
        return this.get('profile').avatar_type == 'social';
    },
    avatarCustom: function(){
        return this.get('profile').avatar_type == 'custom';
    }
});

var UserCollection = TastypieCollection.extend({
    model: User,
    url:com.podnoms.settings.urlRoot + "users/"
});