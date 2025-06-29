def get_optimized_prompt() -> str:
    """SPEED-OPTIMIZED prompt - shorter = faster response"""
    return """
Classify truck view and our plate. Respond with JSON only:

TYPES: FRONT, RIGHT_SIDE, LEFT_SIDE, BACK, INTERIOR, UNKNOWN

{
"detected_type": "FRONT",
"confidence_score": "100%",
"reasoning": "headlights visible"
"plate_number": "ABC1D23" or "not_visible"
}
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
4. How confident are you in percentage string?
5. The plate can be visible or not.
6. if i seed the plate, what is the license plate number?

STRICT JSON RESPONSE:
{{
    "detected_type": "one_of_the_six_options_above",
    "confidence_score": "100%",
    "reasoning": "brief_explanation"
    "plate_number": "ABC1D23" or "not_visible"
}}
"""