## Was ist das Erlangen National High-Performance Computing Center (NHR@FAU)?

Großes Rechenzentrum in Erlangen mit vielen modernen GPUs (u.a. 304 Nvidia A100 (40/80 GB), 352 Nvidia A40, 384 Nvidia H100, ...).

Die meisten wichtigen Infos sind in der [offiziellen Dokumentation](https://doc.nhr.fau.de/clusters/overview/) zu finden. 

## Einladung

Siehe auch in der [offiziellen Doku](https://doc.nhr.fau.de/account/).

Läuft grundsätzlich über Professoren an der OTH, d.h. Studenten haben ohne Einladung keinen Zugang. 

ANSPRECHPARTNER??

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

https://slurm.schedmd.com/overview.html



mit job verbinden
```
srun --jobid=<jobID> --overlap --pty /bin/bash -l
```


TODO

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

Ein virtual environment wird am einfachsten mit Conda erstellt

TODO


#### IDEs

Obwohl IDEs keine scripte ausführen sollen, ist es hilfreich (für Annotations etc.) wenn die IDE Zugriff auf das venv hat. Dies ist ohne weiteres möglich.


### Debugger in PyCharm

Problem: Debugserver muss auf der Node gestartet werden um zu funktionieren, das ist nicht ganz straight forward.

#### Konfiguration

Folgende Runconfig für den Debug Server in Pycharm anlegen.

<img src="Screenshot 2026-01-19 214913.png" alt="drawing" width="7500"/>

Wie im screenshot zu sehen
```
pip install pydevd-pycharm~=
```

Folgendes Snippet in den code
```
pydevd_pycharm.settrace(
    host="127.0.0.1",
    port=5678,
    stdout_to_server=True,
    stderr_to_server=True,
    suspend=True
)
```

#### Debugger Starten



0. Node allozieren, Module laden, venv starten
```
salloc --gres=gpu:a40:1 --time=3:00:00
module add python
module add conda
```


1. SSH Tunnel aufbauen 


__Dieser Prozess muss in einem neuen Konsolenfenster gestartet werden, da er NICHT auf der Node laufen soll.__

```
ssh -N -R 5678:localhost:5678 <UserName>@<Node>
```
`<Username>` ist der FAU Username. `<Node>`


2. Debug Server starten


3. Script starten
