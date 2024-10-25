from flask import Flask, render_template, request
import google.generativeai as genai
genai.configure(api_key="AIzaSyAl4NDlsCEJxQpBhqa-3IRxxLSMw1gI-Dc")
app = Flask(__name__)
questions = [
    {"id": 1, "question": "How would you describe your current mood in a flavor?", 
     "options": ["Sweet like a dessert", "Salty like ocean breeze", "Spicy like a hot pepper", "Savory like comfort food", "Sour like a citrus burst"]},
    {"id": 2, "question": "What texture matches your current vibe?", 
     "options": ["Crispy and crunchy", "Smooth and creamy", "Chewy and soft", "Melty and gooey", "Juicy and refreshing"]},
    {"id": 3, "question": "What kind of food experience are you in the mood for right now?", 
     "options": ["A big, satisfying meal", "A quick snack", "Something unique and exotic", "Comfort food I know and love", "Something light and refreshing"]},
    {"id": 4, "question": "If your mood was a drink, what would it be?", 
     "options": ["Iced coffee for a cool pick-me-up", "A smoothie to stay fresh", "A spicy chai to heat things up", "A fruity mocktail to relax", "A fizzy soda for some energy"]},
    {"id": 5, "question": "What flavor profile do you think would boost your mood right now?", 
     "options": ["Sweet to lift me up", "Spicy for excitement", "Sour for a refreshing kick", "Umami for comfort", "Bitter for a bold taste"]},
    {"id": 6, "question": "What color do you associate with your current mood?", 
     "options": ["Bright and vibrant", "Calm and soothing", "Bold and intense", "Warm and inviting", "Cool and refreshing"]},
    {"id": 7, "question": "If you could have any food as a reward for your mood, what would it be?", 
     "options": ["Decadent chocolate cake", "Spicy tacos", "Fresh salad", "Comforting mac and cheese", "Exotic sushi"]},
    {"id": 8, "question": "What type of meal would you want to share with a friend right now?", 
     "options": ["Finger foods like sliders", "A hearty pizza", "A warm bowl of soup", "A colorful fruit platter", "A fancy three-course dinner"]},
    {"id": 9, "question": "Which smell would make your day better?", 
     "options": ["Freshly baked cookies", "Grilled vegetables", "Herbs and spices", "Freshly brewed coffee", "Fruits"]},
    {"id": 10, "question": "If your mood had a signature dish, what would it be?", 
     "options": ["Indulgent lasagna", "Zesty ceviche", "Hearty chili", "Light sushi rolls", "Comforting chicken noodle soup"]}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question', methods=['POST', 'GET'])
def question():
    return render_template('question.html', questions=questions)

@app.route('/suggest', methods=['POST'])
def suggest_food():
    # Gather user's survey responses
    user_answers = {}
    for question in questions:
        user_answers[question['id']] = request.form.get(str(question['id']))
    prompt = "Suggest six suitable food items based on the following preferences, and return them in an array format:\n"
    for question in questions:
        answer = user_answers[question['id']]
        prompt += f"{question['question']} {answer}\n"
    prompt += "\nReturn only an array of six food items in the format ['','','','','','']."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    print(latitude)
    print(longitude)
    prompt = "Suggest ten restaurants near the location provided, "
    prompt += f"Location: Latitude {latitude}, Longitude {longitude}\n"
    prompt += "\nReturn only an array of ten restaurant names in this format: ['','','','','','','','','','']." 
    model = genai.GenerativeModel('gemini-pro')
    res_response = model.generate_content(prompt)
    return render_template('suggestion.html', suggestion=response.text , ress = res_response.text)

if __name__ == '__main__':
    app.run(debug=True)