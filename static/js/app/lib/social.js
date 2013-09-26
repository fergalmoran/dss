// Generated by CoffeeScript 1.6.2
(function() {
  define(['jquery', 'utils'], function($, utils) {
    return {
      postFacebookLike: function(mixId) {
        return $.getJSON("social/like/" + mixId + "/", function(data) {
          return com.podnoms.utils.showAlert("Posted your like to facebook, you can stop this in your settings page.", "Cheers feen");
        });
      },
      generateEmbedCode: function(model) {
        console.log("Generating embed code");
        return utils.modal("/dlg/embed/" + model.get('slug'));
      },
      sharePageToTwitter: function(model) {
        var loc, title;

        loc = $(this).attr("href");
        title = $(this).attr("title");
        return window.open("http://twitter.com/share?url=" + "http://" + window.location.host + "/" + model.get("item_url") + "&amp;text=" + model.get("title"), "twitterwindow", "height=450, width=550, top=" + ($(window).height() / 2 - 225) + ", left=" + $(window).width() / 2 + ", toolbar=0, location=0, menubar=0, directories=0, scrollbars=0");
      },
      sharePageToFacebook: function(model) {
        return FB.ui({
          method: "feed",
          name: "Check out this mix on Deep South Sounds",
          display: "popup",
          link: "http://" + window.location.host + "/" + model.get("item_url"),
          picture: com.podnoms.settings.staticUrl + model.get("mix_image"),
          caption: model.get("title"),
          description: model.get("description")
        }, function(response) {
          if (response && response.post_id) {
            return utils.showAlert("Success", "Post shared to facebook");
          } else {
            return utils.showError("Error", "Failure sharing post");
          }
        });
      }
    };
  });

}).call(this);
