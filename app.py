import logging

from flask import Flask, render_template, request, redirect, url_for

from ubahn import df

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Drop missing station names and shuffle
df = df.dropna(subset=['Station'])
anagrams = df.sample(frac=1).reset_index(drop=True)


@app.route("/<int:index>", methods=["GET", "POST"])
def anagram_page(index):
    # Get current word and scrambled anagram
    word = anagrams["Station"].iloc[index]
    anagram = word  # Assuming no scrambling for simplicity

    # Handle form submission
    if request.method == "POST":
        user_input = ''.join([request.form.get(f"letter_{i}", "") for i in range(len(word))]).lower()
        if user_input == word.lower():
            return render_template("index.html", anagram=anagram, success=True, index=index, length=len(anagrams))

    return render_template("index.html", anagram=anagram, success=False, index=index, length=len(anagrams))


if __name__ == "__main__":
    app.run(debug=True)
