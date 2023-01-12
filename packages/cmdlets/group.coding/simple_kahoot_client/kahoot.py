import requests

# Replace YOUR_API_KEY with your actual API key
api_key = "YOUR_API_KEY"

# Replace GAME_CODE with the actual game code
game_code = "GAME_CODE"

# Replace USERNAME with the actual username
username = "USERNAME"

# Join the game using the Kahoot API
join_url = f"https://create.kahoot.it/rest/kahoots/{game_code}/join"
join_payload = {"name": username}
join_headers = {"Authorization": f"Bearer {api_key}"}
join_response = requests.post(join_url, json=join_payload, headers=join_headers)

# Get the session ID from the join response
session_id = join_response.json()["id"]

# Get the list of questions for the game using the Kahoot API
questions_url = f"https://create.kahoot.it/rest/kahoots/{game_code}/sessions/{session_id}/questions"
questions_headers = {"Authorization": f"Bearer {api_key}"}
questions_response = requests.get(questions_url, headers=questions_headers)
questions = questions_response.json()

# Iterate over the questions and submit answers using the Kahoot API
for question in questions:
    # Get the prompt and answer choices for the question
    prompt = question["question"]["stem"]
    choices = question["question"]["choices"]

    # Print the prompt and answer choices
    print(prompt)
    for i, choice in enumerate(choices):
        print(f"{i + 1}: {choice['text']}")

    # Prompt the user for their answer
    answer = input("Enter your answer: ")

    # Parse the user's answer
    try:
        answer_index = int(answer) - 1
        if answer_index < 0 or answer_index >= len(choices):
            raise ValueError
    except ValueError:
        print("Invalid answer. Please enter a number between 1 and", len(choices))
        continue

    # Format the answer as a payload to be sent to the Kahoot API
    answer_payload = {
        "type": "manual",
        "questionId": question["id"],
        "choiceId": choices[answer_index]["id"],
    }

    # Submit the answer using the Kahoot API
    submit_url = f"https://create.kahoot.it/rest/kahoots/{game_code}/sessions/{session_id}/answers"
    submit_headers = {"Authorization": f"Bearer {api_key}"}
    submit_response = requests.post(submit_url, json=answer_payload, headers=submit_headers)

    # Print the result of the submission
    if submit_response.status_code == 201:
        print("Answer submitted successfully!")
    else:
        print("Error submitting answer:", submit_response.text)

    # Get the user's score using the Kahoot API
    score_url = f"https://create.kahoot.it/rest/kahoots/{game_code}/sessions/{session_id}/users/{username}"
    score_headers = {"Authorization": f"Bearer {api_key}"}
    score_response = requests.get(score_url, headers=score_headers)
    score = score_response.json()["score"]

    # Display the user's score
    print(f"Your score is: {score}")