# README

# StikeSlipLabCorrelation
This project is a compilation of Python scripts that can be used to visualise and perform correlation calculations on images from experiments on analogue models of strike-slip faults and to generate corresponding figures. 


## Description

Ce script Python permet de visualiser des corrélations sur des images d'expériences de modèles analogiques et de générer des figures correspondantes. Il est nécessaire d'organiser les fichiers et dossiers de manière spécifique pour que le script fonctionne correctement.

## Arborescence des dossiers

L'arborescence des dossiers doit être la suivante :

```
Correlations/
├── Scripts/
│ ├── Visu_correl.py
│ └── plot_save_correl_function.py
├── Correlation_experience/
│ ├── E570/
│ │ ├── frame1
│ │ │	├── Px1_Num6_DeZoom1_LeChantier.tif
│ │ │	└── Px2_Num6_DeZoom1_LeChantier.tif
│ │ ├── frame2
│ │ └── ...
│ ├── E571/
│ │ ├── frame1
│ │ ├── frame2
│ │ └── ...
│ └── E...
├── figures/
│ ├── E570
│ │ ├── Norm of displacement
│ │ └── ...
│ ├── E571
│ └── ...
├── param_correl.xlsx
└── parameters.yaml

```

### Description des dossiers et fichiers :

- **scripts/** : Contient le script Python principal (`votre_script.py`) ainsi que les différentes fonctions nécessaires.
- **Correlation_experience/** : Contient un dossier par expérience. Chaque dossier d'expérience doit contenir les fichiers de données (par exemple, `data1.csv`, `data2.csv`).
- **figures/** : Les figures générées par le script seront enregistrées dans ce dossier.
- **param_correl.xlsx** : Fichier Excel contenant les paramètres des expériences. Chaque ligne correspond à une expérience.

## Prérequis

Avant d'exécuter le script, assurez-vous d'avoir les éléments suivants installés :

- Python 3.x
- Les bibliothèques Python nécessaires (pandas, matplotlib, etc.)

Vous pouvez installer les bibliothèques requises en utilisant la commande suivante :

```bash
pip install -r requirements.txt
```
## Utilisation
1. Assurez-vous que l'arborescence des dossiers est correcte comme décrit ci-dessus.
2. Remplissez le fichier param_correl.xlsx avec les paramètres de vos expériences. Chaque ligne doit correspondre à une expérience spécifique.
3. Placez vos fichiers de données dans les dossiers respectifs sous Correlation_experience/.
4. Exécutez le script principal depuis le dossier scripts/ :

```bash
python scripts/Visu_correl.py
```
Les figures générées seront enregistrées dans le dossier figures/.

## Fichier param_correl.xlsx
Le fichier param_correl.xlsx doit avoir la structure suivante :

| Expérience | Epaisseur materiaux [mm] | debut expe | fin expe | Resolution [pxl/mm] | Limite deplacement min [mm] | Limite deplacement max [mm] | ... 
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--
| Nom de l'exprérience | Epaisseur totale des matériaux | Première frame de l'expérience | Dernière frame de l'expérience | Résolution de la photo en pxl/mm | Limite minimale de la colorbar pour le déplacement | Limite maximale de la colorbar pour le déplacement | ...

| ... | stock | vitesse moteur [mm/s] | temps photos | sens | mode depot  
|------------|:------------:|:------------:|:-----:|:-----:|:-----:
| ... | Nom de l'emplacement des correlations, si c'est un disque dur mettre son nom, si les correlations sont dans le dossier `Correlation_experience` écrire `Local` | Vitesse du moteur en mm/s | Mettre le temps entre deux photos en seconde | Utile pour les expériences du laboratoire GEC. Mettre 1 si la partie haute de la photo corresponds à la plaque fixe, sinon mettre 0| Mettre 1 pour les expériences utilisant la semeuse et 0 pour celle sans 

Exemple :

| Expérience | Epaisseur materiaux [mm] | debut expe | fin expe | Resolution [pxl/mm] | Limite deplacement min [mm]| Limite deplacement max [mm]| ... 
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--
| E571 | 60 | 1 | 3000 | 8.8 | -0.01 | 0.08 | ...

| ... | stock | vitesse moteur [mm/s] | temps photos | sens | mode depot  
|------------|:------------:|:------------:|:-----:|:-----:|:-----:
| ... | Local | 0.0125 | 2 | 0 | 1  





