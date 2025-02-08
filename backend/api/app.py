from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import uuid
import math

app = Flask(__name__)
CORS(app)

current_path = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_path, 'test.json')


try:
  with open(json_file_path, "r", encoding="utf-8") as file:
    courses = json.load(file)
    for course in courses:
      course['id'] = str(uuid.uuid4())
except FileNotFoundError:
    print("output.json not found. Please ensure it exists in the api directory.")
    courses = []


@app.route("/api/courses", methods=["GET"])


def get_courses():
  page = request.args.get('page', default=1, type=int)
  per_page = request.args.get('per_page', default=50, type=int)
  total_pages = math.ceil((len(courses) / per_page))
  if page < 1 or page > total_pages: 
    return jsonify({"error": "Page not found", "total_pages": total_pages}), 404
    
  start = (page - 1) * per_page
  end = start + per_page
  paginated_courses = courses[start:end]
  response = {
    'page': page,
    'per_page': per_page,
    'total_courses': len(courses),
    'total_pages': total_pages,
    'courses': paginated_courses
  }
  return jsonify(response)

if __name__ == "__main__":
  app.run(debug=True)

