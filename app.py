from flask import Flask, render_template, request
import requests
import urllib.parse

app = Flask(__name__)

OMDB_API_KEY = "81ec7219"  # <- put your actual key here
OMDB_URL = "http://www.omdbapi.com/"

@app.route("/", methods=["GET", "POST"])
def index():
    movies = []         # always defined so no NameError
    error_msg = None

    if request.method == "POST":
        title = request.form.get("movie_name", "").strip()
        if title:
            params = {"apikey": OMDB_API_KEY, "s": title, "type": "movie"}
            try:
                resp = requests.get(OMDB_URL, params=params, timeout=10)
                data = resp.json()
                if data.get("Response") == "True":
                    movies = data.get("Search", [])
                    # add a pre-encoded YouTube search query for each movie
                    for m in movies:
                        t = m.get("Title", "")
                        m["yt_query"] = urllib.parse.quote_plus(f"{t} trailer")
                else:
                    error_msg = data.get("Error", "No results found.")
            except Exception as e:
                error_msg = f"Request failed: {e}"
        else:
            error_msg = "Please enter a movie name."

    return render_template("index.html", movies=movies, error_msg=error_msg)

if __name__ == "__main__":
    app.run(debug=True)
