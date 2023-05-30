import random

# Begrüßungsnachrichten mit Hilfstexten
GREETING_INPUTS = ["hallo", "guten tag", "hi", "hey"]
GREETING_RESPONSES = [
    "Hallo! Wie kann ich Ihnen helfen? Hier sind einige Beispiele, wie ich Ihnen helfen kann:\n"
    "1. Passwort zurücksetzen\n"
    "2. Probleme mit der Internetverbindung\n"
    "3. Druckerprobleme\n"
    "4. E-Mail-Probleme\n"
    "5. Fragen zu Ihrem Benutzerkonto",
    "Guten Tag! Wie kann ich Ihnen behilflich sein? Hier sind einige Beispiele, wie ich Ihnen helfen kann:\n"
    "1. Passwort zurücksetzen\n"
    "2. Probleme mit der Internetverbindung\n"
    "3. Druckerprobleme\n"
    "4. E-Mail-Probleme\n"
    "5. Fragen zu Ihrem Benutzerkonto",
    "Hi! Wie kann ich Ihnen weiterhelfen? Hier sind einige Beispiele, wie ich Ihnen helfen kann:\n"
    "1. Passwort zurücksetzen\n"
    "2. Probleme mit der Internetverbindung\n"
    "3. Druckerprobleme\n"
    "4. E-Mail-Probleme\n"
    "5. Fragen zu Ihrem Benutzerkonto",
    "Hey! Was kann ich für Sie tun? Hier sind einige Beispiele, wie ich Ihnen helfen kann:\n"
    "1. Passwort zurücksetzen\n"
    "2. Probleme mit der Internetverbindung\n"
    "3. Druckerprobleme\n"
    "4. E-Mail-Probleme\n"
    "5. Fragen zu Ihrem Benutzerkonto"
]

# Standardantwort, wenn der Bot die Eingabe nicht versteht
DEFAULT_RESPONSE = "Entschuldigung, ich habe das nicht verstanden. Könnten Sie Ihre Frage bitte anders formulieren?"

# Funktion zur Begrüßung des Benutzers
def greet():
    return random.choice(GREETING_RESPONSES)

# Funktion zur Verarbeitung der Eingabe des Benutzers
def get_response(user_input):
    if user_input.lower() in GREETING_INPUTS:
        return greet()
    elif "passwort" in user_input.lower() and "zurücksetzen" in user_input.lower():
        return "Um Ihr Passwort zurückzusetzen, folgen Sie bitte diesen Schritten:\n1. Besuchen Sie die Website 'www.example.com'.\n2. Klicken Sie auf 'Passwort vergessen'.\n3. Geben Sie Ihre E-Mail-Adresse ein, mit der Sie sich registriert haben.\n4. Überprüfen Sie Ihre E-Mails und folgen Sie den Anweisungen, um Ihr Passwort zurückzusetzen."
    elif user_input.lower() == "hilfe":
        return greet()
    else:
        return DEFAULT_RESPONSE

# Haupt-Chatbot-Schleife
print("Willkommen beim IT-Support-Chatbot. Wie kann ich Ihnen helfen?")
while True:
    user_input = input("> ")
    if user_input.lower() == "beenden":
        print("Auf Wiedersehen!")
        break
    response = get_response(user_input)
    print(response)
