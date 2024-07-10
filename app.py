from flask import Flask, render_template, request, jsonify
import os
import sys
import logging

app = Flask(__name__)

# Set up logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

questions = [
    {"question": "1 + 1 = ?", "options": ["1", "2", "3", "4"], "answer": "2"},
    {"question": "2 + 1 = ?", "options": ["1", "2", "3", "4"], "answer": "3"},
    {"question": "4 - 3 = ?", "options": ["0", "1", "2", "3"], "answer": "1"},
    {"question": "6 + 4 = ?", "options": ["8", "9", "10", "11"], "answer": "10"},
    {"question": "3 * 2 = ?", "options": ["4", "5", "6", "7"], "answer": "6"},
    {"question": "2 * 4 = ?", "options": ["6", "7", "8", "9"], "answer": "8"},
    {"question": "3 * 12 = ?", "options": ["33", "34", "35", "36"], "answer": "36"},
    {"question": "9 + 12 = ?", "options": ["20", "21", "22", "23"], "answer": "21"},
    {"question": "81 / 9 = ?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"question": "1 / 2 = ?", "options": ["0.25", "0.5", "0.75", "1"], "answer": "0.5"}
]

@app.route('/')
def index():
    try:
        # Enumerate questions here instead of in the template
        enumerated_questions = list(enumerate(questions))
        return render_template('index.html', enumerated_questions=enumerated_questions)
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "An error occurred", 500

@app.route('/check_answers', methods=['POST'])
def check_answers():
    try:
        user_answers = request.json
        score = 0
        results = []
        
        for i, q in enumerate(questions):
            user_answer = user_answers.get(str(i))
            correct = user_answer == q['answer']
            if correct:
                score += 1
            results.append({
                'question': q['question'],
                'user_answer': user_answer,
                'correct_answer': q['answer'],
                'is_correct': correct
            })
        
        return jsonify({
            'score': score,
            'total': len(questions),
            'results': results
        })
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
