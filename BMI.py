import sys


def calculate_bmi(weight_kg, height_m):
    """
    Calculates the Body Mass Index (BMI) using the formula: BMI = weight (kg) / height^2 (m^2).
    """
    if height_m <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive values for BMI calculation.")

    # BMI formula
    bmi = weight_kg / (height_m ** 2)
    return bmi


def classify_bmi(bmi):
    """
    Classifies the BMI result into standard categories based on WHO standards.
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:  # bmi >= 30.0
        return "Obesity"


def get_valid_float_input(prompt):
    """
    Prompts the user for a positive float number and handles input errors.
    """
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Error: The value must be greater than zero. Please try again.")
        except ValueError:
            print("Error: Invalid input. Please enter a numerical value (e.g., 70.5).")
        except EOFError:
            print("\nInput cancelled. Exiting.")
            sys.exit(0)


def main():
    """
    Main function to run the BMI calculator program.
    """
    print("=" * 40)
    print("--- Body Mass Index (BMI) Calculator ---")
    print("  Input required: Weight (kg), Height (m)")
    print("=" * 40)

    # Get validated user input
    weight = get_valid_float_input("Enter your weight in kilograms (kg): ")
    height = get_valid_float_input("Enter your height in meters (m): ")

    try:
        # Calculate and classify
        bmi_result = calculate_bmi(weight, height)
        category = classify_bmi(bmi_result)

        # Print results
        print("\n" + "=" * 40)
        print("--- Your BMI Analysis ---")
        print(f"Input Weight: {weight:.2f} kg")
        print(f"Input Height: {height:.2f} m")
        print(f"Calculated BMI: {bmi_result:.2f}")
        print(f"BMI Category:   {category}")
        print("=" * 40)

    except ValueError as e:
        print(f"\n[Calculation Error] {e}")
    except Exception as e:
        print(f"\n[An unexpected error occurred] {e}")


if __name__ == "__main__":
    main()