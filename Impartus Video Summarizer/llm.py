import os
from openai import OpenAI
from dotenv import load_dotenv,find_dotenv

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key = "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"
)

def summarize_text(text):

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "Summarize the following lecture text, focusing on core engineering and science subjects and concepts. Provide subheadings based on the main topics covered in the content. Under each subheading, list summary points concisely. Exclude any irrelevant information or tangential details."},
                {"role": "user", "content": text},
            ],
            max_tokens=400,  
            temperature=0.2
        )
        
        # extract and return the summary from the response
        summary = completion.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print("Error during summarization:", e)
        return "Summarization error occurred."