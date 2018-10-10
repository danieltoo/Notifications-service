from app import socketio, app


if __name__ == '__main__':
    #app.run(debug = False,host='0.0.0.0', port=8001)
    socketio.run(app,debug = True,host='0.0.0.0', port=8000)

