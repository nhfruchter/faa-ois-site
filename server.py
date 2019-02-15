from flask import Flask, render_template, jsonify
import faadata
import mockdata

app = Flask(__name__)

@app.route('/')
def splash():	
	return render_template("splash.html")

@app.route("/app.html")
def appPage():
	data = faadata.fetch()
	# data = mockdata.mock(empty=False) # Testing data.	
	return render_template("data.html", data=data)

@app.route("/api")
def api():
	return jsonify(faadata.fetch())

@app.route("/manifest.json")
def manifest():
	return app.send_static_file('manifest.json')

if __name__ == '__main__':
	app.run(debug=True)