from flask import Flask, request, render_template
import random
import ast

# Setup

with open('word-list.txt', 'r') as f:
    word_list = f.read().splitlines()

last_word = dict()

chances = 5

def restart():
    global word
    word = "bingo"
    # print(word)

# Flask Stuff & Game Logic

app = Flask(__name__)

@app.route('/')
def home():
    restart()
    global chances
    chances = 5
    open('user-words.txt', 'w').close()
    return render_template('index.html', data=[])

@app.route('/game', methods=['POST', 'GET'])
def game():
    restart()
    again = False
    result = {}
    last_word.clear()
    print(f'Clearing last word {last_word}')
    global chances
    if chances > 0:
        user_word = request.form.get("word").lower()
        if len(user_word) == 5:
            if user_word in word_list:
                chances -= 1

                if user_word == word:
                    result["You got that right!"] = "green"
                    for i in range(len(user_word)):
                        last_word[i] = [user_word[i], "green"]
                    again = True
                else:
                    for i in range(len(user_word)):
                        if chances == 0:
                            again = True
                            result[f"You lost! The word was '{word}'."] = "red"
                        if user_word[i] in word:
                            corr_letter = user_word[i]
                            corr_index = [i for i, ltr in enumerate(word) if ltr == corr_letter]
                            if i in corr_index:
                                # result.append(f"{user_word[i]} is at the correct position")
                                last_word[i] = [user_word[i], "green"]
                            else:
                                # result.append(f"{user_word[i]} is not at the correct position")
                                last_word[i] = [user_word[i], "goldenrod"]
                        else:
                            # result.append(f"{user_word[i]} is not in the word")
                            last_word[i] = [user_word[i], "red"]

            else:
                result["Invalid word"] = "red"

        else:
            result["Only 5 letter words are allowed!"] = "red"

    # else:
    #     again = True
    #     result[f"You lost! The word was '{word}'."] = "red"

    with open('user-words.txt', 'a') as f1:
        if last_word:
            f1.write(str(last_word)+'\n')
     
    with open('user-words.txt', 'r') as f2:
        string = f2.read().splitlines()
    data = []
    for line in string:
        data.append(ast.literal_eval(line))

    print(chances)
    if data:
        return render_template('index.html', result=result, data=data, again=again)
    else:    
        return render_template('index.html', result=result, again=again)

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

