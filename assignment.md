# Ipotetico servizio di raccolta notifiche
## Specifiche

### porta

Server in ascolto sulla porta 30123 TCP per raccogliere notifiche sono
stringhe di testo, ogni connessione rappresenta una notifica troncare
a 300 caratteri massimo).

### ricerca cliente
Trovare a quale cliente appartiene la notifica in base a ricerca case
insensitive di una label (tabella customers campo notification_label)
nel testo della notifica

### salvataggio su db

Salvare la notifica su DB Sql con ID cliente di appartenenza.

### contatore
Incrementare contatore notifiche giornaliero per cliente.

### atomico
Il salvataggio della notifica e l’incremento del contatore devono
essere eseguiti in modo atomico.

### performance

ogni connessione deve durare il meno possibile e non dev’essere
dipendente dai tempi di I/O wait del DB.

### log

Il servizio deve scrivere log su file con diversi tipi di verbosità:

1.  INFO: con descrizione sintetica delle azioni intraprese.

2.  DEBUG: con query ed eventuali dump di dati utili a ricercare possibili bug.

3.  ERROR: in caso di errori imprevisti.

### conflitti
In caso di conflitti (notifica contenente più di una label) la
notifica dovrà essere salvata su DB senza campo id_customer
valorizzato.
