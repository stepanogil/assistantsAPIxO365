import requests
import os
import json
import time
from dotenv import load_dotenv


load_dotenv("/home/stepanogil/ChatBotDev/.env-files/openai/.env")


openai_api_key = os.getenv('OPENAI_API_KEY')

from openai import OpenAI
client = OpenAI()


from tools.get_user_profile import get_user_profile
from tools.get_events_for_week import get_events_for_week
from tools.get_flagged_emails import get_flagged_emails
from tools.get_emails_with_specific_content_from_sender import get_emails_with_specific_content_from_sender
from tools.reply_to_email import reply_to_email

def chat(user_message, thread_id):
    
    # thread id    
    if thread_id is None:
        raise ValueError("No thread ID. Please create a new thread before chatting.")
    
    # set assistant    
    assistant_id = os.getenv('OAI_X_O365_ASSISTANT_ID') # this has to be created in the playground: https://platform.openai.com/playground
        
    # create thread
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )

    # Create the run
    run = client.beta.threads.runs.create(  
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while True:
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )

        if run.status in ['completed', 'failed']:
            #print(run.status)
            res = client.beta.threads.messages.list(thread_id=thread_id)
            print(res.data[0].content)

            chatbot_response = res.data[0].content[0].text.value
            return chatbot_response
            
        elif run.status == "requires_action":
            tool_outputs_list = []
            tools_to_call = run.required_action.submit_tool_outputs.tool_calls            
            for tool in tools_to_call:
                tool_call_id = tool.id
                function_name = tool.function.name
                #print(function_name)                            
                function_args = json.loads(tool.function.arguments)                
                #print(function_args)                 
                
                if function_name == "RetrieveUserProfile":
                    output = get_user_profile(**function_args)

                if function_name == "RetrieveEventsForWeek":
                    output = get_events_for_week(**function_args)                  
                
                if function_name == "RetrieveFlaggedEmails":
                    output = get_flagged_emails(**function_args)

                if function_name == "RetrieveEmailsWithSpecificContentFromSender":
                    output = get_emails_with_specific_content_from_sender(**function_args)

                if function_name == "ReplyToEmail":
                    output = reply_to_email(**function_args)                         
                                
                if output:
                    #print(output)
                    tool_outputs_list.append({"tool_call_id": tool_call_id, "output": output})
            
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs_list
            )

            # Loop continues after submitting tool outputs to check the updated status
            continue

        # If the status is not one of the specified, continue the loop
        else:
            continue

def new_thread():
    thread = client.beta.threads.create()    
    return thread.id