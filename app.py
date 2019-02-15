from flask import Flask, render_template, jsonify
import faadata

app = Flask(__name__)

@app.route('/')
def splash():	
	return render_template("splash.html")

@app.route("/app.html")
def appPage():
	# data = faadata.fetch()
	data = faadata.mock()
	return render_template("data.html", data=data)

@app.route("/api")
def api():
	return jsonify(faadata.fetch())

@app.route("/manifest.json")
def manifest():
	return app.send_static_file('manifest.json')

if __name__ == '__main__':
	app.run(debug=True)