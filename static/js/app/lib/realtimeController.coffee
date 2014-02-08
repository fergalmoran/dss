require ['vent', 'socket.io'],
    ((vent, SocketIO)  ->
    class RealtimeController
        startSocketIO: ->
            console.log("RealtimeController: SocketIO starting on " + com.podnoms.settings.REALTIME_HOST)
            @socket = SocketIO.connect(com.podnoms.settings.REALTIME_HOST);

            @socket.on "connect", ->
                console.log("RealtimeController: Socket connected")

            @socket.on "message", (message) ->
                alert(message)

            @socket.on "server-session", (session) =>
                if session
                    console.log("RealtimeController: Connected " + sessionId)
                    sessionId = session['sessionId']
                    @registerSessionWithServer sessionId
                else
                    console.log("RealtimeController: Can't read sessionId from socket")

            @socket.on "activity", (data) =>
                console.log("RealtimeController: activity " + data['message'])
                vent.trigger("model:activity:new", data['message'])

            @socket.on "notification", (data) =>
                console.log("RealtimeController: notification " + data['message'])
                vent.trigger("model:notification:new", data['message'])

        registerSessionWithServer: (sessionId) ->
            console.log("Registering session: " + sessionId)
        sendMessage: (message) ->
            console.log("RealtimeController: sendMessage")
            console.log(message)

    RealtimeController

, (err) ->
    console.log("Error locating realtime server, push notification will be disabled")
