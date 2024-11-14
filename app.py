from flask import Flask, render_template, request
from ubahn import df

app = Flask(__name__)

idx = 0
df = df.dropna(subset=['Station'])
anagrams = df.sample(frac=1).reset_index(drop=True)
word = anagrams["Station"].iloc[idx]
anagram = word


@app.route("/", methods=["GET", "POST"])
def index():
    global word
    global idx
    global anagram

    action = request.form.get("action")

    # Handle navigation via GET request
    if action == 'previous':
        idx = (idx - 1) % len(anagrams)
    elif action == 'next':
        idx = (idx + 1) % len(anagrams)
    elif action == 'submit':
        pass

    if request.method == "POST":
        user_input = ''.join([request.form.get(f"letter_{i}", "") for i in range(len(word))]).lower()
        if user_input.lower() == word:
            return render_template("index.html", anagram=anagram, success=True)
    word = anagrams["Station"].iloc[idx]
    anagram = word
    return render_template("index.html", anagram=anagram, success=False)


if __name__ == "__main__":
    app.run(debug=True)

