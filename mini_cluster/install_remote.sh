	#! /bin/bash
# Questo file contiene la lista di comandi che devono essere eseguiti su ciascun nodo per 
# effettuare l'installazione dei pacchetti/librerie necessarie per le computazioni successive
# Questo file viene eseguito in locale e consente di ripere i comandi all'interno del ciclo while
# per ciascuno dei nodi presenti nella lista.

# Per evitare di ottenere in locale gli errori remoti si esegue: sudo bash ./install_remote.sh 2> /dev/null

sudo apt-get install -y sshpass

# lista dei nodi che devono essere considerati
NODES=('156.148.132.70' '156.148.132.71' '156.148.132.72' '156.148.132.74' '156.148.132.79' '156.148.132.80' '156.148.132.182')

# nome utente e password dell'utente root condiviso da tutti i nodi
username='mdtest'
password='mediadart'

# esegue l'installazione dei pacchetti su ciascun nodo
for node in ${NODES[*]}
do
	echo 'Caricamento script sul nodo ' $node
	#sshpass -p $password ssh $username@$node $"echo "$password$" | sudo ls"
	#sshpass -p $password scp ./install_local.sh $username@$node:.
	#sshpass -p $password scp -r ../jobprocessor $username@$node:.
	#sshpass -p $password scp ./Download/opencv-2.4.10.zip $username@$node:.
	
	#echo 'Caricamento Hadoop sul nodo'
	#sshpass -p $password scp ./hadoop-2.6.0.tar.gz $username@$node:.

	#echo 'Esecuzione script installazione sul nodo ' $node
	sshpass -p $password ssh $username@$node "sudo rm -rf jobprocessor"
	#sshpass -p $password ssh $username@$node $"echo "$password$" | sudo -S bash ./install_local.sh > log.txt"
done
