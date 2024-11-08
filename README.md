# Manipulation de la mémoire d'un processus

Ce script permet d'accéder à la mémoire d'un processus en cours d'exécution pour scanner, lire et modifier les adresses. Le script utilise le module `ptrace` pour interagir avec la mémoire et offre des commandes pour effectuer diverses manipulations sur le processus.

**⚠️ Avertissement : Ce projet est à but éducatif uniquement. La modification de la mémoire d’un programme en cours d'exécution peut être contraire aux conditions d’utilisation de certains logiciels et peut causer des problèmes de sécurité et de stabilité. Utilisez ce code de manière responsable et uniquement avec des applications autorisées.**

## Fonctionnalités

Le script propose les fonctionnalités suivantes :

- **Attacher/Détacher un processus en cours d'exécution**.
- **Scanner la mémoire** pour localiser les adresses contenant le score.
- **Lire et écrire** des valeurs dans des adresses mémoire spécifiques.
- **Manipuler les signaux** pour arrêter et reprendre l'exécution du processus.
- **Afficher la pile** du processus cible pour aider au débogage.

## Prérequis

- Python 3.x
- Le module `ptrace` pour Python (installez-le via `pip install python-ptrace`)
- Permissions d'accès suffisantes pour lire/écrire dans la mémoire des processus (souvent nécessite l'exécution en tant que super-utilisateur)

## Guide d'utilisation

### Étape 1 : Lancer le Script

```bash
sudo python3 MemoryHack.py
```

### Étape 2 : Entrer le PID du Processus
Lorsque vous exécutez le script, vous serez invité à saisir le PID (Process ID) du processus que vous souhaitez manipuler. Vous pouvez obtenir le PID du jeu Alex4 en cours d'exécution en utilisant la commande suivante :

```sh
ps aux | grep alex4
```

Ou en utilisant :

```sh
htop
```

Commandes Disponibles
Une fois que le processus est attaché, vous pouvez utiliser les commandes suivantes :

| Commande | Description |
| :--------: | :--------: |
| STOP | Stoppe l'exécution du processus cible. |
| CONT | Reprend l'exécution du processus cible. |
| FIN	| Détache le débogueur et termine le script.
| MAPS |	Affiche les régions de mémoire mappées du processus (permissions, adresse de début et de fin). |
| STACK |	Affiche le contenu de la pile (stack) du processus cible. |
| SCAN | Scanne les régions de mémoire pour localiser les adresses contenant la valeur du score. |
| READ |	Lit une adresse mémoire spécifique et affiche la valeur stockée. |
| WRITE |	Écrit une nouvelle valeur dans une adresse mémoire spécifique. |

Explication des Commandes
STOP et CONT : Utilisées pour suspendre et reprendre le processus. Cela permet de stopper le processus pendant la manipulation de la mémoire.

MAPS : Affiche les informations des régions de mémoire mappées, ce qui est utile pour identifier les sections de la mémoire où la veleur pourrait être stocké.

STACK : Affiche le contenu de la pile (stack) pour mieux comprendre l'état du processus au moment du débogage.

SCAN : Permet de rechercher une valeur spécifique (par exemple, le score actuel). Vous serez invité à entrer la valeur actuelle, et le script identifiera les adresses où ce score est trouvé en mémoire. Ce scan devra être exécuté plusieurs fois pour affiner les adresses stables.

READ : Utilisée pour lire une adresse mémoire spécifique. Par exemple, vous pouvez lire la valeur du score en mémoire pour vérifier qu'elle correspond à ce que vous attendez.

WRITE : Permet d'écrire une nouvelle valeur dans une adresse mémoire. Cela vous permet de modifier le score en écrivant directement une nouvelle valeur dans l'adresse correspondante.

# Exemple d'Utilisation :

* Démarrez le jeu Alex4.
* Exécutez le script et entrez le PID du jeu.
* Utilisez SCAN pour identifier l'adresse de la valeur cherchée.
* Avec READ, vérifiez que l'adresse identifiée contient bien la valeur.
* Utilisez WRITE pour modifier l'addresse à la valeur souhaitée.

# Notes Importantes
Permissions : L'accès à la mémoire d'un autre processus nécessite souvent des privilèges root.  
Risques de stabilité : Modifier la mémoire d'un processus peut provoquer des plantages ou des comportements inattendus.  
Compatibilité : Ce code est testé sous Linux en raison de sa dépendance aux fichiers /proc/[pid]/maps et /proc/[pid]/mem.  
