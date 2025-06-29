from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import blood_test_tool, nutrition_tool, exercise_tool

# Creating a task to help solve user's query
help_patients = Task(
    description="""
    Analyze the blood test report and provide comprehensive medical insights for the user's query: {query}
    
    Steps to follow:
    1. Read and analyze the blood test report from the provided file path: {file_path}
    2. Identify key blood markers and their values
    3. Compare values against normal reference ranges
    4. Identify any abnormal values or concerning patterns
    5. Provide clear explanations of what the results mean
    6. Offer evidence-based recommendations for health improvement
    7. Suggest when to consult healthcare providers
    
    Focus on accuracy, clarity, and patient safety in your analysis.
    """,
    expected_output="""
    A comprehensive blood test analysis report including:
    - Summary of key findings
    - Detailed explanation of abnormal values (if any)
    - Health implications of the results
    - Evidence-based recommendations for improvement
    - Clear next steps and when to seek medical attention
    - Professional medical references where appropriate
    
    Format the response in clear, easy-to-understand language suitable for patients.
    """,
    agent=doctor,
    tools=[blood_test_tool]
)

# Creating a verification task
verification = Task(
    description="""
    Verify that the uploaded document is a valid blood test report containing readable medical data.
    
    Use the file path: {file_path}
    
    Check for:
    1. Presence of standard blood test markers
    2. Numerical values and reference ranges
    3. Laboratory information and dates
    4. Patient information (anonymized)
    5. Overall document authenticity and completeness
    """,
    expected_output="""
    Verification report stating:
    - Whether the document is a valid blood test report
    - What types of tests/markers are included
    - Data quality assessment
    - Any issues or limitations found
    """,
    agent=verifier,
    tools=[blood_test_tool]
)

# Creating a nutrition analysis task
nutrition_analysis = Task(
    description="""
    Analyze the blood test results to provide evidence-based nutritional recommendations.
    
    Use the file path: {file_path}
    
    Focus on:
    1. Nutritional markers (vitamins, minerals, proteins)
    2. Metabolic indicators (glucose, lipids, liver function)
    3. Signs of nutritional deficiencies or excesses
    4. Dietary recommendations based on findings
    5. Supplement suggestions if medically indicated
    
    User query context: {query}
    """,
    expected_output="""
    Nutritional analysis including:
    - Assessment of nutrition-related blood markers
    - Identification of potential deficiencies or concerns
    - Specific dietary recommendations
    - Food sources for important nutrients
    - Supplement recommendations (if appropriate)
    - Timeline for reassessment
    """,
    agent=nutritionist,
    tools=[blood_test_tool, nutrition_tool]
)

# Creating an exercise planning task
exercise_planning = Task(
    description="""
    Develop safe exercise recommendations based on blood test results and overall health indicators.
    
    Use the file path: {file_path}
    
    Consider:
    1. Cardiovascular markers (cholesterol, blood pressure indicators)
    2. Metabolic health (glucose, insulin resistance markers)
    3. Inflammation markers
    4. Overall fitness and health status
    5. Any contraindications for exercise
    
    User query context: {query}
    """,
    expected_output="""
    Exercise plan including:
    - Assessment of exercise readiness based on blood work
    - Recommended types of exercise
    - Appropriate intensity levels
    - Frequency and duration guidelines
    - Safety considerations and contraindications
    - Progression plan
    - When to reassess or consult healthcare providers
    """,
    agent=exercise_specialist,
    tools=[blood_test_tool, exercise_tool]
)