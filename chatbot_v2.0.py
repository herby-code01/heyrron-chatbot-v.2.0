from google import genai as heyrronChat

cli = heyrronChat.Client(api_key="A")

run = True
exit = {'stop', 'quit','close','Q', 'Break'}

while run: 
    question = input("You: ...\n")

    if question.lower() in exit:
        run = False

    response = cli.models.generate_content(model ="gemini-3.8-flash", contents=question)