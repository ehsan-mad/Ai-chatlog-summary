def parse_chat_log(file_path):
    """
    Parse a chat log file and separate messages by speaker.
    
    Args:
        file_path (str): Path to the chat log file
        
    Returns:
        tuple: (user_messages, ai_messages) lists of messages from each speaker
    """
    user_messages = []
    ai_messages = []
    
    current_speaker = None
    current_message = ""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Check if this line starts a new message
                if line.startswith("User:"):
                    # Save the previous message if there was one
                    if current_speaker == "AI" and current_message:
                        ai_messages.append(current_message.strip())
                    
                    # Start a new user message
                    current_speaker = "User"
                    current_message = line[5:].strip()  # Remove "User:" prefix
                
                elif line.startswith("AI:"):
                    # Save the previous message if there was one
                    if current_speaker == "User" and current_message:
                        user_messages.append(current_message.strip())
                    
                    # Start a new AI message
                    current_speaker = "AI"
                    current_message = line[3:].strip()  # Remove "AI:" prefix
                
                # If it's a continuation of the current message
                elif current_speaker:
                    current_message += " " + line
            
            # Don't forget to add the last message
            if current_speaker == "User" and current_message:
                user_messages.append(current_message.strip())
            elif current_speaker == "AI" and current_message:
                ai_messages.append(current_message.strip())
                
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], []
        
    return user_messages, ai_messages

def generate_summary(user_messages, ai_messages):
    """
    Generate a summary of the chat log.
    
    Args:
        user_messages (list): List of messages from the user
        ai_messages (list): List of messages from the AI
        
    Returns:
        str: A formatted summary of the chat
    """
    total_messages = len(user_messages) + len(ai_messages)
    
    summary = "=== Chat Summary ===\n"
    summary += f"Total messages: {total_messages}\n"
    summary += f"User messages: {len(user_messages)}\n"
    summary += f"AI messages: {len(ai_messages)}\n"
    
    return summary

def main():
    """Main function to run the chat log summarizer."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python chat_summarizer.py <chat_log_file>")
        return
    
    file_path = sys.argv[1]
    user_messages, ai_messages = parse_chat_log(file_path)
    
    if not user_messages and not ai_messages:
        print("No messages found or error reading file.")
        return
    
    summary = generate_summary(user_messages, ai_messages)
    print(summary)

if __name__ == "__main__":
    main()