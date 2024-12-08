# https://colab.research.google.com/drive/1N7WTdVseHg4pNQpDMENo2aHOfsCS2-If?usp=sharing
# https://colab.research.google.com/drive/15jh4v_TBPsTyIBhi0Fz46gEkjvhzGaBR?usp=sharing

# Import packages
import google.generativeai as genai
from typing import List, Tuple
import gradio as gr
import json
import os

# Set up Gemini API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# Check if you have set your Gemini API successfully
# You should see "Set Gemini API sucessfully!!" if nothing goes wrong.
try:
    model.generate_content(
      "test",
    )
    print("Set Gemini API sucessfully!!")
except:
    print("There seems to be something wrong with your Gemini API. Please follow our demonstration in the slide to get a correct one.")

## TODO: Input the prompt in the ""
prompt_for_summarization = "Summarize the following article:"

# TODO: Fill in the below two lines: character_for_chatbot and prompt_for_roleplay
# The first one is the character you want your chatbot to play
# The second one is the prompt to make the chatbot be a certain character
character_for_chatbot = "Donald Trump"
prompt_for_roleplay = "Do role play with me. You will act as a character in a story and respond to my input. Let's start!"

# function to clear the coversation
def reset() -> List:
    return interact_roleplay([], prompt_for_roleplay)

# function to call the model to generate
def interact_roleplay(chatbot: List[Tuple[str, str]], user_input: str, temp=1.0) -> List[Tuple[str, str]]:
    '''
    * Arguments

      - user_input: the user input of each round of conversation

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    '''
    try:
        messages = []
        for input_text, response_text in chatbot:
            messages.append({'role': 'user', 'parts': [input_text]})
            messages.append({'role': 'model', 'parts': [response_text]})

        messages.append({'role': 'user', 'parts': [user_input]})

        response = model.generate_content(
          messages,
          generation_config=genai.types.GenerationConfig(temperature=temp),
          safety_settings=[
          {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE",},
          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE",},
          ]
        )

        chatbot.append((user_input, response.text))


    except Exception as e:
        print(f"Error occurred: {e}")
        chatbot.append((user_input, f"Sorry, an error occurred: {e}"))
    return chatbot

def export_roleplay(chatbot: List[Tuple[str, str]], description: str) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - description: the description of this task

    '''
    target = {"chatbot": chatbot, "description": description}
    with open("part2.json", "w") as file:
        json.dump(target, file)

first_dialogue = interact_roleplay([], prompt_for_roleplay)

# This part constructs the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown(f"# Part2: Role Play\nThe chatbot wants to play a role game with you, try interacting with it!!")
    chatbot = gr.Chatbot(value = first_dialogue)
    description_textbox = gr.Textbox(label=f"The character the bot is playing", interactive = False, value=f"{character_for_chatbot}")
    input_textbox = gr.Textbox(label="Input", value = "")
    with gr.Column():
        gr.Markdown("#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get.")
        temperature_slider = gr.Slider(0.0, 1.0, 0.7, step = 0.1, label="Temperature")
    with gr.Row():
        sent_button = gr.Button(value="Send")
        reset_button = gr.Button(value="Reset")
    with gr.Column():
        gr.Markdown("#  Save your Result.\n After you get a satisfied result. Click the export button to recode it.")
        export_button = gr.Button(value="Export")
    sent_button.click(interact_roleplay, inputs=[chatbot, input_textbox, temperature_slider], outputs=[chatbot])
    reset_button.click(reset, outputs=[chatbot])
    export_button.click(export_roleplay, inputs=[chatbot, description_textbox])


demo.launch(debug = True)
