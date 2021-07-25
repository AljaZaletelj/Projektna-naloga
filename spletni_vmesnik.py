import bottle

@bottle.get("/")
def osnovna_stran():
    return bottle.template("osnovna_stran.html")

bottle.run(debug=True, reloader=True)