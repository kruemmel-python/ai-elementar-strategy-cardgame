### README-TRAINGSDATEN.md

---

## Modell-Training: Elementar-Schlacht KI

Diese Datei beschreibt den Trainingsprozess des KI-Modells für das Kartenspiel "Elementar-Schlacht". Im Folgenden sind die wichtigsten Details und Erkenntnisse aus dem Training zusammengefasst.

---

### Modellinformationen

- **Modelltyp:** Sequentiales neuronales Netzwerk
- **Optimierer:** Adam
- **Loss-Funktion:** Sparse Categorical Crossentropy
- **Trainingsepochen:** 50
- **Trainingsdaten:** Generierte Spieldaten aus Simulationen
- **Modellpfad:** `Simulationen/elementar_schlacht_modell.keras`

---

### Trainingsergebnisse

| Epoche | Trainings-Genauigkeit | Trainings-Verlust | Validierungs-Genauigkeit | Validierungs-Verlust | Lernrate |
|--------|-----------------------|-------------------|--------------------------|----------------------|----------|
| 1      | 94.57%                | 0.1377            | 96.80%                   | 0.0931               | 0.0010   |
| 4      | 94.76%                | 0.1426            | 94.46%                   | 0.1266               | 0.0010   |
| 5      | 96.63%                | 0.0929            | 97.50%                   | 0.0846               | 0.0005   |
| 10     | 97.53%                | 0.0738            | 97.57%                   | 0.0723               | 0.00025  |
| 20     | 97.88%                | 0.0626            | 98.12%                   | 0.0599               | 0.000125 |
| 30     | 98.05%                | 0.0573            | 98.13%                   | 0.0556               | 0.00003125 |
| 50     | 98.15%                | 0.0542            | 98.17%                   | 0.0543               | 0.00001  |

---

### Wichtigste Beobachtungen

1. **Anfangsphase:** Das Modell erreichte in den ersten fünf Epochen eine schnelle Verbesserung der Genauigkeit, was darauf hinweist, dass die Grundstruktur des Modells gut geeignet ist, um die Muster in den Trainingsdaten zu erkennen.

2. **Lernratenanpassung:** Die Lernrate wurde nach bestimmten Epochen reduziert (siehe Epochen 4, 8, 17, 23, 29, 35 und 39), was dazu beitrug, dass das Modell auch in späteren Epochen weiter optimiert wurde, ohne dass es zu Überanpassungen kam.

3. **Stabilität:** Ab Epoche 20 stabilisierten sich die Ergebnisse, und die Genauigkeit pendelte sich bei etwa 98% ein, was auf eine erfolgreiche Optimierung hinweist.

4. **Überanpassung vermeiden:** Durch den Einsatz von `ReduceLROnPlateau` wurde die Lernrate immer dann halbiert, wenn keine Verbesserung der Validierungsverluste mehr auftrat. Dies half, das Modell daran zu hindern, die Trainingsdaten zu überanpassen.

---

### Schlussfolgerung und Bewertung des Modells

Das finale Modell zeigt eine sehr hohe Genauigkeit sowohl auf den Trainings- als auch auf den Validierungsdaten. Die Validierungsgenauigkeit von 98.17% nach 50 Epochen zeigt, dass das Modell die komplexen Regeln und Strategien des Spiels "Elementar-Schlacht" effektiv erlernt hat. 

**Stärken des Modells:**
- **Hohe Genauigkeit:** Das Modell erreicht eine exzellente Genauigkeit, was bedeutet, dass es die korrekten Entscheidungen in den meisten Fällen trifft.
- **Robustheit:** Durch den Einsatz von Mechanismen zur Vermeidung von Überanpassung wie `ReduceLROnPlateau` bleibt das Modell stabil und verallgemeinert gut auf unbekannte Daten.

**Schwächen und mögliche Verbesserungen:**
- **Feinabstimmung der Lernrate:** Während die Reduktion der Lernrate zu einer Verbesserung führte, könnte eine adaptive Lernratenstrategie noch effizienter sein.
- **Komplexität vs. Effizienz:** Das Modell könnte weiter vereinfacht werden, ohne die Genauigkeit zu stark zu beeinträchtigen, um die Trainingszeit zu verkürzen.

Insgesamt ist das Modell sehr gut geeignet, um als KI-Gegner im Spiel "Elementar-Schlacht" zu agieren. Es zeigt eine starke Leistungsfähigkeit und ist gut in der Lage, die Strategien des Spielers zu kontern. Zukünftige Arbeiten könnten sich darauf konzentrieren, die Effizienz weiter zu steigern und das Modell noch besser an spezifische Spielstile anzupassen.

---

### Nächste Schritte

- **Feinabstimmung:** Weitere Experimente mit der Struktur des Modells, der Anzahl der Neuronen und der Lernrate könnten die Leistung weiter verbessern.
- **Integration in das Spiel:** Das trainierte Modell kann nun in das Hauptspiel integriert werden, um die KI zu steuern und reale Spielszenarien zu simulieren.
- **Erweiterung des Datensatzes:** Durch die Generierung zusätzlicher Trainingsdaten könnten noch robustere Modelle entwickelt werden.

---

**Modell gespeichert unter:** `Simulationen/elementar_schlacht_modell.keras`

---

Diese Datei bietet einen umfassenden Überblick über den Trainingsprozess und die Leistung des Modells und dient als Referenz für zukünftige Optimierungen und Tests.
