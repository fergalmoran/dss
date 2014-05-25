@Dss.module "SearchApp.Views", (Views, App, Backbone, Marionette, $, _, vent) ->
    class Views.SearchView extends Marionette.Layout
        template: "search"

        ui:
            searchText: '#search-text'

        events:
            'keyup #search-text': 'doSearch'
            'blur #search-text': 'closeSearch'
        engine:
            compile: (template) ->
                compiled = _.template(template)
                render: (context) ->
                    compiled context

        closeSearch: () ->
            $("#suggestions").fadeOut()

        doSearch: () ->
            inputString = @ui.searchText.val()
            if inputString.length is 0
                $("#suggestions").fadeOut()
            else
                results = new MixCollection()
                results.fetch
                    data: $.param(
                        limit: "4"
                        title__icontains: inputString
                    )
                    success: (data) ->
                        $("#suggestions", @el).find("li:gt(0)").remove()
                        $("#suggestions").fadeIn() # Hide the suggestions box
                        results.each (item)->
                            html = new SearchItemView()
                            $("#suggestions", @el).append html.template(item.attributes)

                        return

    Views.SearchView