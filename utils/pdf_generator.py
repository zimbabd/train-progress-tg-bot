import os
import tempfile
from fpdf import FPDF
from datetime import datetime
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_statistics_pdf(sessions, user_id):

    # Create PDF
    pdf = FPDF()
    pdf.add_page()

    # Add a font that supports Cyrillic
    font_path = os.path.join(PROJECT_DIR, "fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(200, 10, txt="Full training statistics", ln=True, align="C")
    pdf.ln(10)

    # Dictionary of correspondence between template_id and exercise names
    exercise_names = {
        1: "run",
        2: "squats",
        3: "push_ups",
        4: "plank",
        5: "jumping_rope"
    }

    # Group sessions by exercise type
    grouped_sessions = defaultdict(list)
    for session in sessions:
        template_id = session[2]  # Index of template_id.
        exercise_name = exercise_names.get(template_id, "Unknown")
        grouped_sessions[exercise_name].append(session)

    # Add a separate table for each type of exercise
    for exercise_name, sessions_list in grouped_sessions.items():
        # Table title for the current exercise type
        pdf.set_font("DejaVu", size=12)
        pdf.cell(200, 10, txt=f"Statistics for the exercise: {exercise_name}", ln=True, align="L")
        pdf.ln(5)

        # Table settings
        pdf.set_font("DejaVu", size=10)

        # Column width
        col_widths_date = [50]
        col_widths_run = [50, 30, 30, 30]
        col_widths_squats = [50, 40, 40, 40]
        col_widths_push_ups = [50, 40, 40, 40]
        col_widths_plank = [50, 50, 50]
        col_widths_jumping_rope = [50, 40, 40, 40]

        # Table title
        pdf.cell(col_widths_date[0], 10, "Date", border=1, align="C")

        # Select column headers and column widths depending on the type of exercise
        if exercise_name == "run":  # Example for running
            pdf.cell(col_widths_run[1], 10, "Distance (km)", border=1, align="C")
            pdf.cell(col_widths_run[2], 10, "Pace (km/h)", border=1, align="C")
            pdf.cell(col_widths_run[3], 10, "Pulse (bpm)", border=1, align="C")
        elif exercise_name == "squats":  # Example for squats
            pdf.cell(col_widths_squats[1], 10, "Repetitions count", border=1, align="C")
            pdf.cell(col_widths_squats[2], 10, "Number of sets", border=1, align="C")
            pdf.cell(col_widths_squats[3], 10, "Weight (kg)", border=1, align="C")
        elif exercise_name == "push_ups":  # Example for push-ups
            pdf.cell(col_widths_push_ups[1], 10, "Repetitions count", border=1, align="C")
            pdf.cell(col_widths_push_ups[2], 10, "Number of sets", border=1, align="C")
            pdf.cell(col_widths_push_ups[3], 10, "Weight (kg)", border=1, align="C")
        elif exercise_name == "plank":  # Example for a plank
            pdf.cell(col_widths_plank[1], 10, "Duration", border=1, align="C")
            pdf.cell(col_widths_plank[2], 10, "Number of sets", border=1, align="C")
        elif exercise_name == "jumping_rope":  # Example for jumping rope
            pdf.cell(col_widths_jumping_rope[1], 10, "Jump count", border=1, align="C")
            pdf.cell(col_widths_jumping_rope[2], 10, "Number of sets", border=1, align="C")
            pdf.cell(col_widths_jumping_rope[3], 10, "Duration", border=1, align="C")

        pdf.ln()

        # Fill in the data for each session of the current exercise type
        for session in sessions_list:
            # Validating and formatting dates
            session_date_str = session[3]
            if session_date_str:
                formatted_date = datetime.strptime(session_date_str, "%Y-%m-%d %H:%M:%S.%f").strftime(
                    "%Y-%m-%d %H:%M:%S")
            else:
                formatted_date = "No data"

            # Fill in the data depending on the type of exercise
            pdf.cell(col_widths_date[0], 10, formatted_date, border=1, align="C")

            if exercise_name == "run":
                pdf.cell(col_widths_run[1], 10, f"{session[4]} km" if session[4] else "-", border=1, align="C")
                pdf.cell(col_widths_run[2], 10, f"{session[5]} km/h" if session[5] else "-", border=1, align="C")
                pdf.cell(col_widths_run[3], 10, f"{session[6]} beats/min" if session[6] else "-", border=1, align="C")
            elif exercise_name == "squats":
                pdf.cell(col_widths_squats[1], 10, f"{session[7]} squats" if session[7] else "-", border=1, align="C")
                pdf.cell(col_widths_squats[2], 10, f"{session[8]} sets" if session[8] else "-", border=1, align="C")
                pdf.cell(col_widths_squats[3], 10, f"{session[9]} kg" if session[9] else "-", border=1, align="C")
            elif exercise_name == "push_ups":
                pdf.cell(col_widths_squats[1], 10, f"{session[7]} push-ups" if session[7] else "-", border=1, align="C")
                pdf.cell(col_widths_squats[2], 10, f"{session[8]} sets" if session[8] else "-", border=1, align="C")
                pdf.cell(col_widths_squats[3], 10, f"{session[9]} kg" if session[9] else "-", border=1, align="C")
            elif exercise_name == "plank":
                pdf.cell(col_widths_plank[1], 10, f"{session[10]} second" if session[10] else "-", border=1, align="C")
                pdf.cell(col_widths_plank[2], 10, f"{session[8]} sets" if session[8] else "-", border=1, align="C")
            elif exercise_name == "jumping_rope" :
                pdf.cell(col_widths_squats[1], 10, f"{session[7]} jumps" if session[7] else "-", border=1, align="C")
                pdf.cell(col_widths_squats[2], 10, f"{session[8]} sets" if session[8] else "-", border=1, align="C")
                pdf.cell(col_widths_squats[3], 10, f"{session[10]} second" if session[10] else "-", border=1, align="C")
            # Add other conditions for other exercises
            pdf.ln()

        # Space between tables for different types of exercises
        pdf.ln(10)

    # Get the current date and format it
    current_date = datetime.now().strftime("%d-%m-%Y")  # Format: 2024-09-11

    # Save the PDF to a temporary file with a current date and user ID.
    pdf_path = os.path.join(tempfile.gettempdir(), f"{user_id}_{current_date}_training_statistics.pdf")

    pdf.output(pdf_path)
    return pdf_path
