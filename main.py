import random
import os
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

HIGH_SCORE_FILE = "high_scores.json"

def load_high_scores():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_high_score(difficulty, attempts):
    scores = load_high_scores()
    if difficulty not in scores or attempts < scores[difficulty]:
        scores[difficulty] = attempts
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f)
        return True
    return False

def get_difficulty():
    print(f"\n{Fore.CYAN}Select Difficulty Level:{Style.RESET_ALL}")
    print(f"1. {Fore.GREEN}Easy (15 attempts) 🟢{Style.RESET_ALL}")
    print(f"2. {Fore.YELLOW}Medium (10 attempts) 🟡{Style.RESET_ALL}")
    print(f"3. {Fore.RED}Hard (5 attempts) 🔴{Style.RESET_ALL}")
    
    while True:
        choice = input(f"{Fore.BLUE}Enter choice (1-3): {Style.RESET_ALL}")
        if choice == '1':
            return "Easy", 15
        elif choice == '2':
            return "Medium", 10
        elif choice == '3':
            return "Hard", 5
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

def play_game():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}✨ Welcome to the Number Guessing Game! ✨{Style.RESET_ALL}")
    
    scores = load_high_scores()
    if scores:
        print(f"\n{Fore.YELLOW}🏆 Current High Scores (Best Attempts):{Style.RESET_ALL}")
        for diff, score in scores.items():
            print(f"  {diff}: {score}")
    
    difficulty_name, max_attempts = get_difficulty()
    secret_number = random.randint(1, 100)
    attempts = 0
    
    print(f"\n{Fore.CYAN}I'm thinking of a number between 1 and 100... 🧐{Style.RESET_ALL}")
    print(f"{Fore.CYAN}You have {max_attempts} attempts.{Style.RESET_ALL}")

    while attempts < max_attempts:
        try:
            guess = int(input(f"\n{Fore.BLUE}Attempt {attempts + 1}/{max_attempts} - Enter your guess: {Style.RESET_ALL}"))
            attempts += 1
            
            if guess < secret_number:
                print(f"{Fore.YELLOW}Too low! 📉 Try again.{Style.RESET_ALL}")
            elif guess > secret_number:
                print(f"{Fore.YELLOW}Too high! 📈 Try again.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 CONGRATULATIONS! You guessed it in {attempts} attempts! 🎉{Style.RESET_ALL}")
                if save_high_score(difficulty_name, attempts):
                    print(f"{Fore.CYAN}New High Score for {difficulty_name}! 🏅{Style.RESET_ALL}")
                return
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    print(f"\n{Fore.RED}Game Over! 💀 You've run out of attempts.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}The secret number was: {secret_number}{Style.RESET_ALL}")

if __name__ == "__main__":
    while True:
        play_game()
        play_again = input(f"\n{Fore.MAGENTA}Do you want to play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            print(f"{Fore.CYAN}Thanks for playing! Goodbye! 👋{Style.RESET_ALL}")
            break
