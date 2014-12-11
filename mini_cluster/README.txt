Questa cartella presenta tutti i file necessari a gestire un minicluster
di nodi, composto utilizzando i mac mini presenti nel laboratorio.
Attraverso gli script scritti e' possibile replicare l'installazione di programmi,
la copia di file o l'esecuzione di comandi su ciascun nodo del cluster.

Attualmente l'esecuzione dei comandi viene effettuata in modo sincrono ma la si puo'
avviare in bash ground appendendo il simbolo & al termine di ogni comando.
E' preferibile evitare di eseguire comandi in baskground in quanto non e' possibile
riavviare i mac mini con successo (necessitano del monitor) in modo da evitare l'intervento
manuale per il corretto riavvio di ciascun nodo.


All'interno della cartella sono presenti due script bash:
- install_local.sh : 	corrisponde allo script bash che viene eseguito su ciascuno
			dei nodi del cluster. All'interno di questo file e' possibile
			specificare le installazioni (e' d'obbligo la modalita'	non 
			interattiva) e/o i comandi che devono essere eseguiti.
- install_remote.sh :	contiene la lista di indirizzi IP dei nodi che costituiscono il
			cluster, per ciascun nodo carica il file install_local.sh e lo esegue con
			i privilegi di root sulla base delle credenziali di accesso riportate in
			due variabili.
			Pertanto questo file si occupa di distribuire ed eseguire in modo sincrono
			i comandi su tutti i nodi remoti che costituiscono il cluster.


