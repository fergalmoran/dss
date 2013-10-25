define ['vent', 'socket.io'],
(vent, SocketIO)  ->
    class RealtimeController
        startSocketIO: ->
            console.log("RealtimeController: SocketIO starting on " + com.podnoms.settings.REALTIME_HOST)
            @socket = SocketIO.connect(com.podnoms.settings.REALTIME_HOST);

            @socket.on 'connect', ->
                console.log("RealtimeController: Socket connected")
                @socket.emit('client-reg', {sessionId: com.podnoms.settings.currentUser, userName: com.podnoms.settings.userName})

                @socket.on "server-session", (data) =>
                    if data
                        console.log("RealtimeController: Connected " + data['sessionId'])
                    else
                        console.log("RealtimeController: Can't read sessionId from socket")

            """
            @socket.on "activity", (data) =>
                console.log("RealtimeController: activity " + data['message'])
                vent.trigger("model:activity:new", data['message'])
            """

            @socket.on "notification", (data) =>
                console.log("RealtimeController: notification " + data['message'])
                vent.trigger("model:notification:new", data['message'])

        sendMessage: (message) ->
            console.log("RealtimeController: sendMessage")
            console.log(message)

    RealtimeController

