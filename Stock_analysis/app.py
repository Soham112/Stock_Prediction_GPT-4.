from flask import Flask, render_template, request, jsonify
import os
import sys
import base64
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from image_trading_view import extract_images
from gpt4o_technical_analysis import analyze_images_in_directory, filter_yes_investment_opportunities

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json'

# Store analysis results
all_analysis_results = []
image_directory = os.path.join(os.path.dirname(__file__), '../images')  # Define image_directory globally

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-extraction', methods=['POST'])
def start_extraction():
    extract_images()
    return jsonify({"message": "Extraction started"})

@app.route('/start-analysis', methods=['POST'])
def start_analysis():
    global all_analysis_results
    global image_directory  # Ensure image_directory is accessible globally
    analysis_results = analyze_images_in_directory(image_directory)
    yes_investments = filter_yes_investment_opportunities(analysis_results)
    
    # Store all results
    all_analysis_results = yes_investments
    
    return jsonify({"message": "Analysis complete, you can now view the results"})

@app.route('/get-results', methods=['GET'])
def get_results():
    global all_analysis_results
    global image_directory  # Ensure image_directory is accessible globally
    
    results = {}
    for file, analysis in all_analysis_results:
        image_path = os.path.join(image_directory, file)
        base64_image = encode_image_to_base64(image_path)
        analysis_content = analysis['choices'][0]['message']['content']
        results[file] = {
            "analysis": analysis_content,
            "image": base64_image
        }

    return jsonify({
        "results": results,
        "total": len(all_analysis_results)
    })

@app.route('/in-depth-analysis', methods=['POST'])
def in_depth_analysis():
    prompt = request.form['prompt']
    in_depth_result = f"In-depth analysis for: {prompt}"
    return jsonify({"message": "In-depth analysis complete", "result": in_depth_result})

if __name__ == '__main__':
    app.run(debug=True)
