## Was ist das Erlangen National High-Performance Computing Center (NHR@FAU)?

Großes Rechenzentrum in Erlangen mit vielen modernen GPUs (u.a. 304 Nvidia A100 (40/80 GB), 352 Nvidia A40, 384 Nvidia H100, ...).

Die meisten wichtigen Infos sind in der [offiziellen Dokumentation](https://doc.nhr.fau.de/clusters/overview/) zu finden. 

## Einladung

Siehe auch in der [offiziellen Doku](https://doc.nhr.fau.de/account/).

Läuft grundsätzlich über Professoren an der OTH, d.h. Studenten haben ohne Einladung keinen Zugang. 

Ansprechpartner sind hier grundsätzlich die Professoren, die für euer Projekt zuständig sind.

## Verbindungsaufbau und Node Struktur

Für Details siehe die [offizielle Dokumentation](https://doc.nhr.fau.de/access/overview/)

#### HPC-Portal

Das __[HPC-Portal](https://doc.nhr.fau.de/hpc-portal/)__ ist erreichbar unter https://portal.hpc.fau.de/. Es ist die zentrale Anlaufstelle um Nutzung und Projekte zu verwalten.

#### SSH-Keypair generieren und im HPC-Portal hinterlegen

Der erste Schritt ist es, auf dem eigenen Computer ein SSH Keypair zu erzeugen. Dieser Schritt muss für jeden Computer, der zur Verbindung genutzt werden soll, wiederholt werden.

Der Public SSH Key muss dann im HPC-Portal hinterlegt werden. 

Eine Anleitung dazu findet sich [hier](https://doc.nhr.fau.de/access/ssh-command-line/).

Bei ersten Mal am besten Verbindung mit

```
ssh csnhr.nhr.fau.de
```
testen.

#### Verbindung via SSH

Nun ist eine Verbindung zu den Clustern möglich. Deren SSH Adressen sind [hier](https://doc.nhr.fau.de/clusters/overview/) zu finden.

## Nutzung



### Slurm und Jobs

Das NHR nutzt [Slurm](https://slurm.schedmd.com/overview.html) um Rechenresourcen auf dem Cluster zu verwalten. Über Slurm kann Zugriff zu einer Node angefragt werden, die dem Nutzer dann für einen bestimmten Zeitraum exklusiv zur Verfügung steht.

Um ein Script auf einem der GPUs auszuführen (etwa um ein Modell zu trainieren), kann es mit 
```
sbatch [optionen] <jobscript>
```

Eine interaktive Session kann mit

```
salloc [optionen]
```

gestartet werden. Diese erlaubt über die Konsole direkten Zugang zur zugewiesen Node und eignet sich damit für Tests, Debugging usw.

Um in einem anderen Konsolenfenster auf einen interaktiven Job zuzugreifen kann

```
srun --jobid=<jobID> --overlap --pty /bin/bash -l
```
verwendet werden.

Wenn der interaktive job vor Ablauf der Zeit nicht mehr gebraucht wird, sollte er mit `exit` beendet werden.



#### Wichtiger Hinweis zu IDEs

Die Remote IDE läuft _NICHT_ auf den Nodes, sondern auf dem zentralen Controller. Prozesse, die von der IDE gestartet werden, laufen somit auch nicht auf den Nodes. 

Der Controller ist _NICHT_ dafür gedacht, leistungsintensive Programme auszuführen.

Am einfachsten ist es, scripte in der Konsole auf der Node zu starten, um dieses Problem zu umgehen

##### Lösung in Pycharm:
- Runconfigs für Scripte, die Konsolenbefehl automatisieren
- DebugServer um Debugging zu ermöglichen (siehe unten)

## Setup 

### Module

Module laden mit
```
module add {module}
```
Das muss jedes mal nach dem Verbinden gemacht werden!

Für die Programmierung mit Python ist
```
module add python
```
erforderlich.

### Venv

Als Erstes die [Initialisierungsschritte in der offiziellen Doku](https://doc.nhr.fau.de/environment/python-env/) befolgen.

Ein virtual environment wird am einfachsten mit Conda erstellt.

```
conda create -n <env. name> python=<py. version>
```

Wie mit Conda gewohnt muss es dann jedes Mal for dem start eines Jobs oder zu beginn einer interaktiven Session aktiviert werden.

```
conda activate <my_env_name_here>
```

#### IDEs

Obwohl IDEs keine scripte ausführen sollen, ist es hilfreich (für Annotations etc.) wenn die IDE Zugriff auf das venv hat. Dies ist ohne weiteres möglich.


### Debugger in PyCharm

Problem: Debugserver muss auf der Node gestartet werden um zu funktionieren, das ist nicht ganz straight forward.

#### Konfiguration

Runconfig für den Debug-Server in PyCharm anlegen mit 
```
Hostname: 0.0.0.0
Port: 5678
```
Falls der Port belegt ist einen anderen ausprobieren. Dann die Anweisungen in PyCharm befolgen, um pydevd-pycharm zu installieren und das Skript mit dem Debug-Server zu verbinden.




#### Debugger Starten



##### 0. Node allozieren, Module laden, venv starten
```
salloc --gres=gpu:a40:1 --time=3:00:00
module add python
conda activate <my_env_name_here>
```


##### 1. SSH Tunnel aufbauen 


__Dieser Prozess muss in einem neuen Konsolenfenster gestartet werden, da er NICHT auf der Node laufen soll.__

```
ssh -N -R 5678:localhost:5678 <UserName>@<Node>
```
`<Username>` ist der FAU Username. `<Node>`


##### 2. Debug Server starten
(via PyCharm)

##### 3. Script starten
(Per Befehl in der Konsole auf der Node, nicht in PyCharm)