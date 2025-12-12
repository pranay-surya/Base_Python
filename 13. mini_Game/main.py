import random

# Display the rules of the game
print("Wining Rule is follow as ::\n"
      + "Rock vs paper == Paper wins\n"
      + "Rock vs Scissor == Rock wins\n"
      + "Scissor vs Paper == Scissor wins")
print("__________________________")
print("__________________________")

# Infinite loop to keep the game running
while True:
    # Display choices to the user
    print("Enter your choice\n"
          + "1 - Rock\n"
          + "2 - Paper\n"
          + "3 - Scissor")
    
    # Take user input
    choose = int(input("Enter your choice::"))

    # Check for invalid input
    if choose > 3 or choose < 1:
        print("Invalid choice.........")
        continue  # Skip to next loop iteration

    # Map number to user choice
    if choose == 1:
        choice_name = "Rock"
    elif choose == 2:
        choice_name = "Paper"
    elif choose == 3:
        choice_name = "Scissor"

    print("Your choice is", choice_name)

    # Generate computer's choice randomly
    comp_choice = random.choice([1, 2, 3])
    if comp_choice == 1:
        comp_name = "Rock"
    elif comp_choice == 2:
        comp_name = "Paper"
    elif comp_choice == 3:
        comp_name = "Scissor"

    print("Computer choice is", comp_name)

    # Determine the winner
    if choose == comp_choice:
        print("It's a draw")
    elif choose == 1 and comp_choice == 2:
        print("Computer wins")
    elif choose == 2 and comp_choice == 3:
        print("Computer wins")
    elif choose == 3 and comp_choice == 1:
        print("Computer wins")
    elif choose == 2 and comp_choice == 1:
        print("You win")
    elif choose == 3 and comp_choice == 2:
        print("You win")
    elif choose == 1 and comp_choice == 3:
        print("You win")

    # Ask user if they want to play again
    print("Do you want to play again? (Y/N)")
    ans = input().lower()
    if ans == 'n':
        break  # Exit the loop if user says no
