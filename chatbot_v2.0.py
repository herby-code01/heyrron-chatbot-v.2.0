from google import genai as heyrronChat

cli = heyrronChat.Client(api_key="AQ")

run = True
exit = {'stop', 'quit','close','Q', 'Break'}

while run: 
    question = input("You: ...\n")

    if question.lower() in exit:
        run = False

    initial_input = cli.models.generate_content(model="gemini-3.8-flash", contents="Start by saying I'm HeyrronChat version 2.0")    

    response = cli.models.generate_content(model ="gemini-3.8-flash", contents=question)

    print(initial_input +"\n")
    print("heyrronChat: ", response)