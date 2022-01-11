from flask import Flask, request, render_template
import random
import ast

# Setup

with open('word-list.txt', 'r') as f:
    word_list = f.read().splitlines()

last_word = dict()

word = random.choice(word_list)
chances = 5
print(word)

def restart():
    global word
    word = random.choice(word_list)
    global chances
    chances = 5
    print(word)
    open('user-words.txt', 'w').close()

# Flask Stuff & Game Logic

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', result='opening', data=[])

@app.route('/game', methods=['POST', 'GET'])
def game():
    result = []
    last_word.clear()
    print(f'Clearing last word {last_word}')
    user_word = request.form.get("word").lower()
    
    if len(user_word) == 5:
        if user_word in word_list:
            global chances
            chances -= 1
            if user_word == word:
                result.append("You got that right!")
                restart()
            else:
                for i in range(len(user_word)):
                    if user_word[i] in word:
                        corr_letter = user_word[i]
                        corr_index = word.find(corr_letter)
                        if i == corr_index:
                            result.append(f"{user_word[i]} is at the correct position")
                            last_word[i] = [user_word[i], "green"]
                        else:
                            result.append(f"{user_word[i]} is not at the correct position")
                            last_word[i] = [user_word[i], "goldenrod"]
                    else:
                        result.append(f"{user_word[i]} is not in the word")
                        last_word[i] = [user_word[i], "red"]
                        
        else:
            result.append("Invalid word")

    else:
        result.append("Only 5 letters words are allowed!")

    with open('user-words.txt', 'a') as f1:
        if last_word:
            f1.write(str(last_word)+'\n')
     
    with open('user-words.txt', 'r') as f2:
        string = f2.read().splitlines()
    data = []
    for line in string:
        data.append(ast.literal_eval(line))

    print(data)
    print(chances)
    if data:
        return render_template('index.html', result=result, data=data)
    else:    
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

