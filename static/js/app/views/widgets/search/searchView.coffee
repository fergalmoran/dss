define ['jquery', 'underscore', 'marionette', 'vent',
        'models/mix/mixCollection',
        'views/widgets/search/searchItemView', 'text!/tpl/SearchView'],
($, _, Marionette, vent,
 MixCollection,
 SearchItemView, Template) ->
    class SearchView extends Marionette.CompositeView
        template: _.template(Template)

        ui:
            searchText: '#search-text'

        events:
            'keyup #search-text': 'doSearch'

        engine:
            compile: (template) ->
                compiled = _.template(template)
                render: (context) ->
                    compiled context


        doSearch: () ->
            inputString = @ui.searchText.val()
            if inputString.length is 0
                $("#suggestions").fadeOut() # Hide the suggestions box
            else
#               $.get "/api/v1/mix/?limit=3&title__icontains=" + inputString
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

    SearchView