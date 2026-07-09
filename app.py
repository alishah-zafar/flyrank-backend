from flask import Flask, jsonify
app=Flask(__name__)
@app.route("/")
def home():
  return jsonify({"message":"Hello: this is my smallest backend"})
@app.route("/status")
def status():
  return jsonify({"status":"ok","service":"runnning"})
if __name__ == "__main__":
    app.run(debug=True, port=5000)
