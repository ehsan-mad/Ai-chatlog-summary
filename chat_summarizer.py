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

def extract_keywords(messages, top_n=5):
    """
    Extract the most common keywords from a list of messages.
    
    Args:
        messages (list): List of messages to analyze
        top_n (int): Number of top keywords to return
        
    Returns:
        list: Top keywords with their counts
    """
    import re
    from collections import Counter
    
    # Common English stop words to exclude
    stop_words = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
        'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
        'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 
        'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
        'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 
        'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 
        'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
        'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
        'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
        'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 
        'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 
        'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
    }
    
    # Combine all messages into one text
    all_text = ' '.join(messages)
    
    # Extract words (only alphabetic characters, convert to lowercase)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
    
    # Filter out stop words
    filtered_words = [word for word in words if word not in stop_words]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Return top N keywords
    return word_counts.most_common(top_n)

def determine_conversation_nature(keywords):
    """
    Determine the nature of the conversation based on keywords.
    
    Args:
        keywords (list): List of (keyword, count) tuples
        
    Returns:
        str: Description of the conversation nature
    """
    if not keywords:
        return "Unable to determine the nature of the conversation."
    
    # Extract just the keywords
    topics = [keyword for keyword, _ in keywords]
    
    # Join the keywords into a readable string
    topic_str = ', '.join(topics)
    
    return f"The conversation was mainly about {topic_str}."

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
    
    # Calculate the number of exchanges (a user message followed by an AI response)
    exchanges = min(len(user_messages), len(ai_messages))
    
    # Add any remaining messages that don't form complete exchanges
    if len(user_messages) > len(ai_messages):
        exchanges += 1
    
    # Extract keywords from all messages
    all_messages = user_messages + ai_messages
    top_keywords = extract_keywords(all_messages, top_n=5)
    
    # Determine the nature of the conversation
    conversation_nature = determine_conversation_nature(top_keywords)
    
    # Format the keywords for display
    keyword_str = ', '.join([f"{keyword}" for keyword, _ in top_keywords])
    
    # Create the detailed summary
    summary = "=== Chat Summary ===\n"
    summary += f"Total messages: {total_messages}\n"
    summary += f"User messages: {len(user_messages)}\n"
    summary += f"AI messages: {len(ai_messages)}\n"
    summary += f"Total exchanges: {exchanges}\n"
    
    if top_keywords:
        summary += f"\nMost common keywords: {keyword_str}\n"
    
    # Add the simplified summary format
    summary += "\nSummary:\n"
    summary += f"- The conversation had {exchanges} exchanges.\n"
    summary += f"- {conversation_nature}\n"
    summary += f"- Most common keywords: {keyword_str}.\n"
    
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
    