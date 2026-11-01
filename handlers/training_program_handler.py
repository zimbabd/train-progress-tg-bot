from telebot import types
from repository.training_sessions_repository import TrainingSessionsRepository
from repository.exercise_templates_repository import ExerciseTemplatesRepository
from exercises.run import handle_run  # Import the run handler
from exercises.squats import handle_squats  # Import the squat handler
from exercises.push_ups import handle_push_ups # Import the push-up handler
from exercises.plank import handle_plank # Import the plank handler
from exercises.jumping_rope import handle_jumping_rope # Import the jumping-rope handler
from config import DB_PATH

training_repo = TrainingSessionsRepository(str(DB_PATH))
exercise_repo = ExerciseTemplatesRepository(str(DB_PATH))
exercise_repo.fill_table()


def handle_training_program(bot, message):
    # Get all exercise templates from the database
    exercises = exercise_repo.get_all_templates()

    # Create inline buttons for each exercise
    inline_markup = types.InlineKeyboardMarkup()
    for exercise in exercises:
        button = types.InlineKeyboardButton(exercise['template_name'],
                                            callback_data=f"exercise_{exercise['template_id']}")
        inline_markup.add(button)
    bot.send_message(message.chat.id, "Select an exercise:", reply_markup=inline_markup)



def handle_exercise_selection(call, bot):
    # Extract the exercise ID from callback_data
    template_id = int(call.data.split('_')[1])

    # Get template by ID
    template = exercise_repo.get_template_by_id(template_id)

    if template:
        if template['template_name'] == 'run':
            handle_run(bot, call, exercise_repo, training_repo)
        elif template['template_name'] == 'squats':
            handle_squats(bot, call, exercise_repo, training_repo)
        elif template['template_name'] == 'push_ups':
            handle_push_ups(bot, call, exercise_repo, training_repo)
        elif template['template_name'] == 'plank':
            handle_plank(bot, call, exercise_repo, training_repo)
        elif template['template_name'] == 'jumping_rope':
            handle_jumping_rope(bot, call, exercise_repo, training_repo)
        else:
            bot.send_message(call.message.chat.id, "Exercise not supported.")
    else:
        bot.send_message(call.message.chat.id, "Error: Exercise not found.")
