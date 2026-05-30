from flask import Flask, render_template, request
from groq import Groq
from datetime import datetime

app = Flask(__name__)


client = Groq(
    api_key="API"
)

@app.route("/", methods=["GET", "POST"])
def home():

    

    response = ""
    user_message = ""

    quiz_response = ""
    planner_response = ""
    motivation_response = ""

    if request.method == "POST":

        action = request.form.get("action")

        

        if action == "chat":

            user_message = request.form["message"]

            chat_completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are DreamMind AI,
                        a cute, supportive, intelligent AI assistant
                        made for students.

                        Be helpful, friendly, motivational,
                        and structured.
                        """
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],

                model="llama-3.3-70b-versatile"

            )

            response = chat_completion.choices[0].message.content

        

        elif action == "quiz":

            topic = request.form["quiz_topic"]

            prompt = f"""
            Create a well-structured quiz on:

            {topic}

            Rules:
            - Generate 5 MCQs
            - Give 4 options
            - Mention correct answers
            - Add spacing between questions
            - Make it clean and easy to read
            """

            chat_completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model="llama-3.3-70b-versatile"

            )

            quiz_response = chat_completion.choices[0].message.content


        elif action == "planner":

            planner_input = request.form["planner_input"]

            exam_date = request.form["exam_date"]

            # Current Date

            today = datetime.today().date()

            # Convert selected date

            exam = datetime.strptime(exam_date, "%Y-%m-%d").date()

            # Remaining Days

            days_left = (exam - today).days

            prompt = f"""
            Create a detailed student study timetable.

            Today's Date: {today}

            Exam Date: {exam_date}

            Days Remaining: {days_left}

            Subjects/Goals:
            {planner_input}

            Instructions:
            - Divide study plan day by day
            - Add revision sessions
            - Add small breaks
            - Add motivation tips
            - Make the format beautiful and structured
            - Use emojis sometimes
            """

            chat_completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model="llama-3.3-70b-versatile"

            )

            planner_response = chat_completion.choices[0].message.content

       

        elif action == "motivate":

            mood = request.form["mood"]

            prompt = f"""
            Someone is feeling:

            {mood}

            Give:
            - cute motivation
            - emotional support
            - study encouragement
            - confidence boost
            - emojis
            - short affirmations

            Make it aesthetic and comforting.
            """

            chat_completion = client.chat.completions.create(

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                model="llama-3.3-70b-versatile"

            )

            motivation_response = chat_completion.choices[0].message.content

    return render_template(

        "index.html",

        response=response,
        user_message=user_message,

        quiz_response=quiz_response,

        planner_response=planner_response,

        motivation_response=motivation_response

    )

if __name__ == "__main__":
    app.run(debug=True)