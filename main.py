from flask import Flask, render_template, request, session, jsonify
import random
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

HIGH_SCORE_FILE = "high_scores.json"

def load_high_scores():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_high_score(difficulty, attempts):
    scores = load_high_scores()
    if difficulty not in scores or attempts < scores[difficulty]:
        scores[difficulty] = attempts
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f)
        return True
    return False

@app.route('/')
def index():
    scores = load_high_scores()
    return render_template('index.html', scores=scores)

@app.route('/start', methods=['POST'])
def start_game():
    difficulty = request.json.get('difficulty', 'Medium')
    max_attempts = {"Easy": 15, "Medium": 10, "Hard": 5}.get(difficulty, 10)
    
    session['target'] = random.randint(1, 100)
    session['attempts'] = 0
    session['max_attempts'] = max_attempts
    session['difficulty'] = difficulty
    session['game_over'] = False
    
    return jsonify({
        "message": f"Game started! Difficulty: {difficulty}",
        "max_attempts": max_attempts
    })

@app.route('/guess', methods=['POST'])
def guess():
    if 'target' not in session or session.get('game_over'):
        return jsonify({"error": "Game not started"}), 400
        
    try:
        user_guess = int(request.json.get('guess'))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid guess"}), 400
        
    session['attempts'] += 1
    attempts = session['attempts']
    max_attempts = session['max_attempts']
    target = session['target']
    
    result = ""
    status = "playing"
    
    if user_guess == target:
        result = f"🎉 Correct! You won in {attempts} attempts!"
        status = "won"
        session['game_over'] = True
        is_high_score = save_high_score(session['difficulty'], attempts)
    elif attempts >= max_attempts:
        result = f"💀 Game Over! The number was {target}."
        status = "lost"
        session['game_over'] = True
    elif user_guess < target:
        result = "📈 Too low! Try again."
    else:
        result = "📉 Too high! Try again."
        
    return jsonify({
        "result": result,
        "attempts": attempts,
        "status": status,
        "is_high_score": status == "won" and is_high_score if 'is_high_score' in locals() else False
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
