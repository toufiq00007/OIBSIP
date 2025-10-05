from flask import Flask, request, jsonify, render_template

# The Flask application instance
app = Flask(__name__)


# --- Core BMI Logic ---
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculates BMI: weight (kg) / height (m)^2."""
    if height_m <= 0:
        raise ValueError("Height must be positive.")
    return weight_kg / (height_m ** 2)


def interpret_bmi(bmi: float) -> str:
    """Interprets the BMI value to determine the weight category."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight"
    elif 25.0 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obesity"


# --- API Endpoint (Backend Logic) ---

# This endpoint handles the actual calculation request from the frontend JS
@app.route('/calculate', methods=['POST'])
def handle_calculation():
    try:
        data = request.get_json()
        weight_kg = float(data.get('weight'))
        height_cm = float(data.get('height'))

        if weight_kg <= 0 or height_cm <= 0:
            return jsonify({"error": "Input must be positive."}), 400

        height_m = height_cm / 100

        bmi_value = calculate_bmi(weight_kg, height_m)
        category = interpret_bmi(bmi_value)

        return jsonify({
            "bmi": round(bmi_value, 2),
            "category": category,
            "success": True
        })

    except ValueError:
        return jsonify({"error": "Invalid input format. Please use numbers."}), 400
    except Exception:
        return jsonify({"error": "An unexpected server error occurred."}), 500


# --- Frontend Serving (Root Route) ---

# This route serves the HTML file located in the 'templates' folder when the user visits the root URL.
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # host='0.0.0.0' makes the server accessible from any device on your network
    app.run(debug=True, host='0.0.0.0')