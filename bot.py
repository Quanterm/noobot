import random

# Begrüßungsnachrichten des Chatbots
greetings = ["Hallo! Wie kann ich Ihnen heute helfen?", "Guten Tag! Wie kann ich Ihnen behilflich sein?", "Willkommen beim IT-Support! Wie kann ich Ihnen weiterhelfen?"]

# Antworten des Chatbots
responses = {
    "Passwort vergessen": "Kein Problem! Ich werde Ihnen helfen, Ihr Passwort zurückzusetzen. Bitte geben Sie Ihren Benutzernamen an.",
    "Druckerproblem": "Welches Problem haben Sie mit dem Drucker? Bitte beschreiben Sie es genauer.",
    "Internetverbindung langsam": "Ich verstehe, dass Ihre Internetverbindung langsam ist. Wir werden uns darum kümmern. Können Sie bitte Ihre IP-Adresse angeben?",
    "Softwareinstallation": "Gerne unterstütze ich Sie bei der Softwareinstallation. Bitte geben Sie den Namen der Software an, die Sie installieren möchten.",
    "Netzwerkproblem": "Bei Netzwerkproblemen kann ich Ihnen helfen. Welches konkrete Problem haben Sie mit Ihrem Netzwerk?",
    "Email-Konfiguration": "Um Ihre E-Mail-Konfiguration zu überprüfen, benötige ich Ihren E-Mail-Anbieter (z. B. Gmail, Outlook) und Ihren Benutzernamen.",
    "Danke": "Gern geschehen! Wenn Sie weitere Fragen haben, stehe ich Ihnen gerne zur Verfügung."
}

# Funktion zur Verarbeitung der Eingabe und Generierung der Antwort
def process_input(user_input):
    for key in responses:
        if key.lower() in user_input.lower():
            return responses[key]
    return "Entschuldigung, aber ich konnte Ihre Anfrage nicht verstehen. Bitte wählen Sie eine der folgenden Optionen: Passwort vergessen, Druckerproblem, Internetverbindung langsam, Softwareinstallation, Netzwerkproblem, Email-Konfiguration."

# Hauptfunktion des Chatbots
def chatbot():
    print(random.choice(greetings))
    
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        else:
            response = process_input(user_input)
            print(response)

# Chatbot starten
chatbot()
