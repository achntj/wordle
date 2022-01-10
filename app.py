from flask import Flask, request, render_template
import random

# Flask Stuff

app = Flask(__name__)

@app.route('/')
@app.route('/model')
def home():
    return render_template('index.html', result='opening')

@app.route('/game', methods=['POST', 'GET'])
def game():
    result = []
    with open('word-list.txt', 'r') as f:
        word_list = f.read().splitlines()

    word = random.choice(word_list)
    print(word)

    user_word = request.form.get("word").lower()
    
    if len(user_word) == 5:
        if user_word in word_list:
            if user_word == word:
                result.append("You got that right!")
            else:
                for i in range(len(user_word)):
                    if user_word[i] in word:
                        corr_letter = user_word[i]
                        corr_index = word.find(corr_letter)
                        if i == corr_index:
                            result.append(f"{user_word[i]} is at the correct position")
                        else:
                            result.append(f"{user_word[i]} is not at the correct position")
                    else:
                        result.append(f"{user_word[i]} is not in the word")
                        
        else:
            result.append("Invalid word")
    else:
        result.append("Only 5 letters words are allowed!")

    return render_template('index.html', result=result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title=404)


@app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html", title=403)


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html", title=500)


if __name__ == "__main__":
    app.run()


