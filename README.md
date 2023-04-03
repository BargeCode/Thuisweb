# Thuisweb

## Inleiding
De website voor thuis. Ik volg Flask Friday van Codemy.com op youtube terwijl ik deze flask-app bouw. Dit is mijn versie/variant er op.

## Hoe ver zijn we?
Op dit moment is het mogelijk om:
- De app in zijn eigen container te laten starten.
- De MySQL db te starten in zijn eigen container.
- De app en db met elkaar te verbinden.
- een gebruiker toe te voegen.
- een gebruiker aan te passen.
- een gebruiker te verwijderen.
- een wachtwoord aan een gebruiker te hangen, en vervolgens via opgegeven email, het wachtwoord te verifieren. 

## Hoe installeer ik dit?
Het enige wat je nodig heb is Git om de app te downloaden en docker om de app te installeren en te starten.

Kopieer en plak het volgende in terminal als je Git en Docker geinstalleerd heb. 

```bash
git clone https://github.com/BargeCode/Thuisweb.git && docker compose up -d
```

Open een webbrowser en ga naar:
`localhost:3000/index.html` en kijk gerust even rond.
