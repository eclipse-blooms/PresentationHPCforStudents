# Was ist KIGS

OTH interner KI-GPU Server mit 4 RTX 6000 GPUs mit je 50GB Memory. Alle Nutzer haben vollen geteilten Zugriff auf die GPUs. Infos auch im [ELO-Kurs](https://elearning.oth-regensburg.de/course/view.php?id=4786).


## Verbindungsaufbau zu KIGS

1. VPN Verbindung aufbauen ([FortiClient](https://rzwww.oth-regensburg.de/supportwiki/doku.php?id=en:public:netz:vpn-forticlient)) (Falls nicht bereits im OTH Netzwerk)

2. Folgenden Befehl in die Konsole eingeben:

```
    ssh {RZ-Kürzel}@im-kigs.oth-regensburg.de
```
also z.B.
```
    ssh abc12345@im-kigs.oth-regensburg.de
```

3. RZ Passwort Eingeben

### Fertig

```
                   _     _
                  | | __(_)  __ _  ___
                  | |/ /| | / _` |/ __|
                  |   < | || (_| |\__ \
    Willkommen am |_|\_\|_| \__, ||___/ ,
    dem GPU-Server für die  |___/
    KI-Lehre in der IM-Fakultät.
```

<img src="https://www.digisaurier.de/wp-content/uploads/2015/03/boris_becker_bin_ich_schon_drin.jpg" alt="drawing" width="500"/>

### Was wenn ich eine IDE verwenden will?

#### Pycharm
(nur in Pro Version, welche für Studenten kostenlos ist)

Verbindung unter:
File -> Remote Development -> SSH -> New Project
```
Username: RZ-Kennung
Host: im-kigs.oth-regensburg.de
Port: 22
```

##### Alternativ: Jetbrains Toolbox

#### VS-Code etc. unterstützen Remote development auch, siehe entsprechende Dokumentation


## Hinweise zur Nutzung gemeinsamer GPU Resourcen

### GPU Memory ist begrenzt, unnötige Belegung behindert andere Nutzer

- (halbwegs) optimierten Code schreiben
- sinnvolle Modellgrößen und Datensätze benutzen
- __Beende Prozesse__ die nicht mehr benötigt werden
  - __Insbesondere Jupyter Notebooks__ belegen gerne viel speicher der erst freigegeben wird, wenn der Jupyter server beendet wird

### Restarts und Downtime
- Server Restarts in der Nacht von Sonntag auf Montag um 3:00 Morgens
- Darüber Hinaus manchmal Downtime
- Datenverlust minimieren durch Trainingscheckpoints etc.

### Python Virtual Environments

Es ist im Allgemeinen notwending, für jedes Projekt ein eigenes Virtual Environment anzulegen. Pakete können dann im Virtual Environment verwaltet werden.

Dafür gibt es mehrere Möglichkeiten, die auch von IDEs teilweise oder vollständig automatisiert werden können (z.B [unten rechts im Pycharm GUI](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html))

Alternativ können diese natürlich auch über die Konsole angelegt werden, hierzu gibt es Dokumentation im Internet (z.B. für [python venv](https://docs.python.org/3/library/venv.html) und [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) )

## Die Wichtigsten Konsolenbefehle

Hinweis: Auf KIGS läuft Linux, entsprechend kann vieles mit den entsprechenden Befehlen in der Konsole gemach werden (z.B. Dateiverwaltung, Toolinstallation etc.).

### überflüssige Prozesse beenden

Bitte regelmäßig überprüfen (siehe unten) ob Prozesse laufen, die nicht mehr notwendig sind. Verantwortlich sind hier oft Jupyter Server. 
Diese Prozesse können dann mit 
```
kill {ProcessID}
```
beendet werden.


### GPU Auslastung Überwachen

Der einfachste Befehl um schnell die GPU Auslastung auf KIGS zu überprüfen ist
```
nvidia-smi
```

So ist es einfach festzustellen, welche GPUs grade frei sind.

Mit der Option 
```
nvidia-smi -l
```
erneuert sich die Ausgabe alle paar Sekunden automatisch. Das macht es einfach in einem eigenen Fenster die GPU Auslastung ständig zu überwachen.

#### Für mehr Details


```
nvtop
```

Startet eine Anwendung in der Konsole, die noch detailliertere Informationen zu laufenden Prozessen ausgibt. Hier findet sich u.a. auch der Nutzer, der den Prozess gestartet hat. Falls ein Nutze viele tote Prozesse hat, die Vram verschwenden kann and diesen so eine freundliche E-Mail geschrieben werden.

