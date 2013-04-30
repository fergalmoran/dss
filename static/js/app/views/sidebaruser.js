/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

window.SidebarViewUser = Backbone.View.extend({
    events: {
        "click #follow-button": "toggleFollow"
    },
    render: function () {
        ich.addTemplate('sidebaruser', this.template());
        this.model.formatDate = function (date) {
            return 'Yaaaaaaa....';
        };
        $(this.el).html(ich.sidebaruser(this.model.toJSON()));

        this._renderFollowButton();
        return this;
    },
    _renderFollowButton: function () {
        if (this.model.get('profile').following) {
            $('#follow-button', this.el).addClass("btn-warning disabled");
            $('#follow-button', this.el).removeClass("btn-success");
            $('#follow-button', this.el).text("Unfollow");
            $('#follow-icon', this.el).addClass("icon-eye-close");
            $('#follow-icon', this.el).removeClass("icon-eye-open");
        } else {
            $('#follow-button', this.el).removeClass("btn-warning disabled");
            $('#follow-button', this.el).addClass("btn-success");
            $('#follow-button', this.el).text("Follow");
            $('#follow-icon', this.el).removeClass("icon-eye-close");
            $('#follow-icon', this.el).addClass("icon-eye-open");
        }
    },
    toggleFollow: function () {
        var model = this.model;
        $('#follow-button', this.el).addClass("loading");
        $.post(
            "/ajax/toggle_follow/",
            { userId: this.model.get("id") },
            function (data) {
                var result = $.parseJSON(data);
                if (result.value == 'Followed')
                    model.set('profile.following', true);
                else
                    model.set('profile.following', true);
                this._renderFollowButton();
                $('#follow-button', this.el).removeClass("loading");
            }
        );
    }
});
