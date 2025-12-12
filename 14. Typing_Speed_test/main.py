import time   
import random   

# Function to pick a random sentence from a predefined list
def get_random_sentence():
    sentences = [
        "Python is a powerful and easy to learn programming language.",
        "Artificial Intelligence is shaping the future of technology.",
        "Typing speed depends on practice and accuracy.",
        "The quick brown fox jumps over the lazy dog.",
        "Practice makes a person perfect in every task."
    ]
    return random.choice(sentences)  # Randomly select one sentence


# Display the typing test heading
print("||---------- TYPING SPEED TEST ----------||")
print()

# Get a random sentence to type
sentence = get_random_sentence()
print(" TYPE THE FOLLOWING SENTENCE ...\n")
print()
print(">>>", sentence)  # Show the sentence to the user
print()

# Record the start time just before the user starts typing
time_start = time.time()

# Take input from the user (the typed sentence)
type = input("START TYPING :: \n>>>")
print()

# Record the end time after the user finishes typing
time_end = time.time()

# Calculate total time taken in seconds (rounded to 2 decimal places)
taken_time = round(time_end - time_start, 2)

# Count total words typed
total_words = len(type.split())

# Calculate Words Per Minute (WPM)
wpm = round((total_words / taken_time) * 60, 2)

# Count the number of correctly typed characters
correct_chars = 0
for i in range(min(len(type), len(sentence))):
    if type[i] == sentence[i]:
        correct_chars += 1

# Calculate typing accuracy percentage
accuracy = round((correct_chars / len(sentence)) * 100, 2)

# Display the results to the user
print("||---------- RESULT ----------||")
print()
print(f"Time Taken    :: {taken_time} seconds")
print(f"Words Per Min :: {wpm} WPM")
print(f"Accuracy      :: {accuracy} %")
