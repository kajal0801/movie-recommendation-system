from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OMDB_API_KEY = "81ec7219"  # Replace with your key

@app.route("/", methods=["GET", "POST"])
def index():
    movies = []
    if request.method == "POST":
        movie_name = request.form["movie_name"]
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={movie_name}"
        response = requests.get(url)
        data = response.json()
        if data.get("Response") == "True":
            movies = data["Search"]
    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
