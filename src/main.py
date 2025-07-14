#!/usr/bin/env python3

from chatbot import process_user_input

def main():
    print("Mutil-agent Chatbot")
    print("=" * 50)
    print("Supported Features:")
    print("- Query Weather")
    print("- Input 'quit' or 'exit' to quit")
    print("=" * 50)
    
    while True:
        try:
            # get user input
            user_input = input("\n User: ").strip()
            
            # check exit command
            if user_input.lower() in ['quit', 'exit']:
                print("bye")
                break
            
            # check empty input
            if not user_input:
                print("Please enter a valid question")
                continue
            
            # process user input
            print("\n Agent is thinking...")
            response = process_user_input(user_input)
            print(f" Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n   BYE!")
            break
        except Exception as e:
            print(f"    Error: {e}")

if __name__ == "__main__":
    main() 