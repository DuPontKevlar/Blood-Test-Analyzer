import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader
from typing import Optional

# Creating search tool
search_tool = SerperDevTool()

@tool("read_blood_test_report")
def blood_test_tool(path: str = 'data/sample.pdf') -> str:
    """
    Tool to read and extract content from blood test PDF reports.
    Provide the path to the PDF file to analyze.
    
    Args:
        path: Path to the PDF file to read (default: 'data/sample.pdf')
    
    Returns:
        str: Extracted content from the PDF report
    """
    try:
        if not os.path.exists(path):
            return f"Error: File not found at path: {path}"
        
        docs = PyPDFLoader(file_path=path).load()
        
        full_report = ""
        for data in docs:
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report if full_report.strip() else "Error: No content found in PDF"
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@tool("analyze_nutrition")
def nutrition_tool(blood_report_data: str) -> str:
    """
    Analyze nutrition based on blood report data and provide personalized
    dietary recommendations based on blood markers and health indicators.
    
    Args:
        blood_report_data: Blood report data to analyze for nutrition recommendations
    
    Returns:
        str: Nutrition analysis and recommendations
    """
    try:
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        if processed_data:
            processed_data = processed_data.replace("  ", " ")
            
        # Enhanced nutrition analysis logic based on common blood markers
        analysis = "Based on your blood report, here are some nutritional recommendations:\n\n"
        
        # Check for common deficiencies and markers
        if "hemoglobin" in processed_data.lower() or "hb" in processed_data.lower():
            analysis += "🩸 Iron & Hemoglobin:\n"
            analysis += "- Include iron-rich foods like spinach, lentils, and lean meats\n"
            analysis += "- Pair iron sources with vitamin C for better absorption\n\n"
            
        if "vitamin" in processed_data.lower():
            analysis += "💊 Vitamins:\n"
            analysis += "- Ensure adequate vitamin D through sunlight and fortified foods\n"
            analysis += "- Include B-complex vitamins through whole grains and leafy greens\n\n"
            
        if "cholesterol" in processed_data.lower():
            analysis += "❤️ Heart Health:\n"
            analysis += "- Limit saturated fats and trans fats\n"
            analysis += "- Include omega-3 rich foods like fish and walnuts\n"
            analysis += "- Increase soluble fiber through oats and beans\n\n"
            
        if "glucose" in processed_data.lower() or "sugar" in processed_data.lower():
            analysis += "🍎 Blood Sugar Management:\n"
            analysis += "- Choose complex carbohydrates over simple sugars\n"
            analysis += "- Include protein with each meal to stabilize blood sugar\n"
            analysis += "- Consider smaller, more frequent meals\n\n"
        
        # General recommendations
        analysis += "🥗 General Nutritional Guidelines:\n"
        analysis += "- Maintain a balanced diet with adequate protein (0.8-1g per kg body weight)\n"
        analysis += "- Include 5-7 servings of fresh fruits and vegetables daily\n"
        analysis += "- Stay hydrated with 8-10 glasses of water daily\n"
        analysis += "- Limit processed foods and added sugars\n"
        analysis += "- Consider consulting a registered dietitian for personalized advice\n"
        analysis += "\n⚠️ Always discuss dietary changes with your healthcare provider."
        
        return analysis
    except Exception as e:
        return f"Error in nutrition analysis: {str(e)}"

@tool("create_exercise_plan")
def exercise_tool(blood_report_data: str) -> str:
    """
    Create a personalized exercise plan based on blood report data,
    considering health markers and any potential limitations or recommendations.
    
    Args:
        blood_report_data: Blood report data to create personalized exercise plan
    
    Returns:
        str: Personalized exercise plan and recommendations
    """
    try:
        # Enhanced exercise planning logic based on blood markers
        plan = "Based on your blood report, here's a personalized exercise plan:\n\n"
        
        # Check for specific conditions that affect exercise
        if "hemoglobin" in blood_report_data.lower() or "anemia" in blood_report_data.lower():
            plan += "🩸 For Iron/Hemoglobin Concerns:\n"
            plan += "- Start with low-intensity activities (walking, gentle yoga)\n"
            plan += "- Gradually increase intensity as levels improve\n"
            plan += "- Monitor fatigue levels closely\n\n"
            
        if "cholesterol" in blood_report_data.lower():
            plan += "❤️ Cardiovascular Health Focus:\n"
            plan += "- Prioritize aerobic exercises (brisk walking, cycling, swimming)\n"
            plan += "- Aim for 150 minutes of moderate cardio per week\n"
            plan += "- Include 2-3 resistance training sessions\n\n"
            
        if "glucose" in blood_report_data.lower() or "diabetes" in blood_report_data.lower():
            plan += "🍎 Blood Sugar Management:\n"
            plan += "- Exercise 30-60 minutes after meals to help glucose control\n"
            plan += "- Combine cardio with resistance training\n"
            plan += "- Monitor blood sugar before and after exercise\n\n"
            
        # General exercise recommendations
        plan += "🏃‍♂️ Weekly Exercise Structure:\n\n"
        plan += "📅 Monday, Wednesday, Friday - Cardio Days:\n"
        plan += "- 30-45 minutes of moderate cardio (walking, swimming, cycling)\n"
        plan += "- Start at 60-70% max heart rate\n\n"
        
        plan += "📅 Tuesday, Thursday - Strength Training:\n"
        plan += "- Full-body resistance exercises\n"
        plan += "- 2-3 sets of 8-12 repetitions\n"
        plan += "- Focus on major muscle groups\n\n"
        
        plan += "📅 Saturday - Active Recovery:\n"
        plan += "- Gentle yoga or stretching (20-30 minutes)\n"
        plan += "- Light walking or recreational activities\n\n"
        
        plan += "📅 Sunday - Rest Day:\n"
        plan += "- Complete rest or very light activities\n\n"
        
        plan += "⚠️ Important Safety Guidelines:\n"
        plan += "- Always warm up for 5-10 minutes before exercise\n"
        plan += "- Cool down and stretch after each session\n"
        plan += "- Stay hydrated throughout your workout\n"
        plan += "- Listen to your body and rest when needed\n"
        plan += "- Start slowly and gradually increase intensity\n"
        plan += "- ALWAYS consult your doctor before starting any exercise program\n"
        plan += "- Stop exercising and seek medical attention if you experience chest pain, severe shortness of breath, or dizziness\n"
        
        return plan
    except Exception as e:
        return f"Error in exercise planning: {str(e)}"

# Export the tools for use in your agents
__all__ = ['blood_test_tool', 'nutrition_tool', 'exercise_tool', 'search_tool']