def get_truck_classification_prompt(expected_type: str) -> str:
    """
    Simple and effective prompt for truck image classification
    """
    
    prompt = f"""
Analyze this truck image and identify the view type.

TRUCK VIEWS:
- front: Front view (headlights, grille, windshield)
- right_side: Right side view
- left_side: Left side view  
- back: Rear view (tail lights, back doors)
- interior: Inside cabin view
- unknown: Not a clear truck view

EXPECTED: {expected_type}

Respond with JSON only:
{{
    "detected_type": "front",
    "confidence_score": 0.85,
    "reasoning": "I can see headlights and front grille"
}}
"""
    return prompt.strip()


# Alternative prompts for testing different approaches
def get_simple_prompt(expected_type: str) -> str:
    """Even simpler prompt for basic testing"""
    return f"""
What truck view is this image showing?

Options: front, right_side, left_side, back, interior, unknown
Expected: {expected_type}

JSON response only:
{{"detected_type": "front", "confidence_score": 0.9}}
"""


def get_detailed_prompt(expected_type: str = "dont have an expected type") -> str:
    """More detailed prompt if we need better accuracy later"""
    return f"""
You are a truck inspection expert. Analyze this image carefully.

TRUCK VIEW TYPES:
1. FRONT: Shows headlights, front bumper, grille, windshield
2. RIGHT_SIDE: Shows right side of truck body, right wheels, passenger side
3. LEFT_SIDE: Shows left side of truck body, left wheels, driver side  
4. BACK: Shows rear doors, tail lights, license plate area
5. INTERIOR: Shows inside cabin - dashboard, seats, steering wheel
6. UNKNOWN: Image unclear or not a truck

EXPECTED TYPE: {expected_type}

ANALYSIS STEPS:
1. Is this a truck/commercial vehicle?
2. What specific features are visible?
3. What angle/view does this represent?
4. How confident are you (0.0 to 1.0)?

STRICT JSON RESPONSE:
{{
    "detected_type": "one_of_the_six_options_above",
    "confidence_score": 0.85,
    "reasoning": "brief_explanation"
}}
"""