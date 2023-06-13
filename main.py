from flask import Flask, request, jsonify
from flask_cors import CORS
from services.student_service import get_team
from services.student_service import load_projects
from services.student_service import BY_HARD_SKILLS
from services.student_service import BALANCED
from services.student_service import BY_SOFT_SKILS

# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)

# GET Endpoint =============================================================================
@app.route("/team_hard_skills", methods=["POST"])  
def get_team_by_hard_skills():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return (jsonify({'error': 'No data provided'}), 400)
        team = get_team(data, BY_HARD_SKILLS, 5)
        team = [str(item) for item in team]
        return jsonify({"team": team})
    elif request.method == "GET":
        return (jsonify({'error': 'GET method not supported for /get_team'}), 405)

# GET Endpoint =============================================================================
@app.route("/team_soft_skills", methods=["POST"])  
def get_team_balanced():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return (jsonify({'error': 'No data provided'}), 400)
        team = get_team(data, BY_SOFT_SKILS, 5)
        team = [str(item) for item in team]
        return jsonify({"team": team})
    elif request.method == "GET":
        return (jsonify({'error': 'GET method not supported for /get_team'}), 405)

# GET Endpoint =============================================================================
@app.route("/balanced", methods=["POST"])  
def get_team_by_soft():
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return (jsonify({'error': 'No data provided'}), 400)
        team = get_team(data, BALANCED, 5)
        team = [str(item) for item in team]
        return jsonify({"team": team})
    elif request.method == "GET":
        return (jsonify({'error': 'GET method not supported for /get_team'}), 405)



# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
    app.run(debug=True, port=5001)
