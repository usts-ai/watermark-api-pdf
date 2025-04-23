# API de Filigrane PDF

Une API RESTful pour appliquer des filigranes (watermarks) à des documents PDF. Cette API utilise l'outil en ligne de commande `pdf-watermark` et offre une interface HTTP simple pour intégrer cette fonctionnalité dans vos applications.

## Caractéristiques

- Application de filigranes texte ou image sur des documents PDF
- Support de deux modes de filigrane : grille (grid) et insertion à position spécifique (insert)
- Nombreuses options de personnalisation (opacité, angle, couleur, etc.)
- Architecture modulaire et extensible
- Documentation intégrée à l'API

## Structure du projet

```
watermark-api-pdf/
├── app/
│   ├── __init__.py         # Factory pattern pour initialiser l'application
│   ├── routes/             # Gestion des routes de l'API
│   │   ├── __init__.py
│   │   ├── main.py         # Route principale (documentation)
│   │   └── watermark.py    # Route pour le filigrane
│   ├── services/           # Logique métier
│   │   ├── __init__.py
│   │   └── watermark_service.py  # Service pour appliquer les filigranes
│   └── utils/              # Utilitaires (pour de futures extensions)
│       └── __init__.py
├── requirements.txt        # Dépendances du projet
├── README.md              # Documentation
└── run.py                 # Point d'entrée de l'application
```

## Installation

### Prérequis

- Python 3.6+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner ce dépôt
   ```bash
   git clone <url-du-depot>
   cd watermark-api-pdf
   ```

2. Créer un environnement virtuel (recommandé)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. Installer les dépendances
   ```bash
   pip install -r requirements.txt
   ```

## Démarrage du serveur

```bash
python run.py
```

Le serveur démarre par défaut sur le port 5000 et est accessible à l'adresse http://localhost:5000.

## Utilisation de l'API

### Documentation de l'API

Accédez à la racine de l'API pour voir la documentation complète :
```
GET /
```

### Application d'un filigrane (multipart/form-data)

```
POST /watermark
```

#### Paramètres principaux

| Paramètre | Type | Description | Obligatoire |
|-----------|------|-------------|-------------|
| file | File | Le fichier PDF à traiter | Oui |
| text | String | Le texte à utiliser comme filigrane | Oui* |
| image | File | L'image à utiliser comme filigrane | Oui* |
| pattern | String | Le motif à utiliser: 'grid' ou 'insert'. Défaut: 'grid' | Non |

*Vous devez fournir soit `text` soit `image`, mais pas les deux.

#### Options communes

| Option | Type | Description | Obligatoire |
|--------|------|-------------|-------------|
| opacity | Float | Opacité du filigrane entre 0 (invisible) et 1 (aucune transparence) | Non |
| angle | Float | Angle d'inclinaison du filigrane en degrés | Non |
| text_color | String | Couleur du texte au format hexadécimal, ex: #000000 | Non |
| text_font | String | Police du texte à utiliser | Non |
| text_size | Integer | Taille de la police | Non |
| unselectable | String | Rendre le texte non sélectionnable ('true'/'false') | Non |
| image_scale | Float | Facteur d'échelle pour l'image | Non |
| save_as_image | String | Convertir chaque page PDF en image ('true'/'false') | Non |
| dpi | Integer | DPI à utiliser lors de la sauvegarde du PDF en image | Non |

#### Options spécifiques au motif 'grid'

| Option | Type | Description | Obligatoire |
|--------|------|-------------|-------------|
| horizontal_boxes | Integer | Nombre de répétitions du filigrane horizontalement | Non |
| vertical_boxes | Integer | Nombre de répétitions du filigrane verticalement | Non |
| margin | String | Laisser une marge autour de la page ('true'/'false') | Non |

#### Options spécifiques au motif 'insert'

| Option | Type | Description | Obligatoire |
|--------|------|-------------|-------------|
| x | Float | Position horizontale du filigrane (entre 0 et 1) | Non |
| y | Float | Position verticale du filigrane (entre 0 et 1) | Non |
| horizontal_alignment | String | Alignement horizontal ('left', 'right', 'center') | Non |

### Application d'un filigrane (données binaires)

```
POST /watermark/binary
```

Ce nouvel endpoint permet d'envoyer le PDF directement en binaire dans le corps de la requête, au lieu d'utiliser multipart/form-data. Les paramètres du filigrane sont passés via les query parameters dans l'URL.

#### En-têtes requis

| En-tête | Valeur |
|---------|--------|
| Content-Type | application/octet-stream |

#### Corps de la requête

Le corps de la requête doit contenir les données binaires du PDF à traiter.

#### Query parameters

| Paramètre | Type | Description | Obligatoire |
|-----------|------|-------------|-------------|
| text | String | Le texte à utiliser comme filigrane | Oui |
| pattern | String | Le motif à utiliser: 'grid' ou 'insert'. Défaut: 'grid' | Non |

Toutes les options communes et spécifiques aux motifs mentionnées ci-dessus peuvent également être passées en tant que query parameters.

## Exemples d'utilisation

### Avec cURL

#### Filigrane texte en grille (multipart/form-data)

```bash
curl -X POST \
  -F "file=@chemin/vers/votre/document.pdf" \
  -F "text=CONFIDENTIEL" \
  -F "pattern=grid" \
  -F "opacity=0.3" \
  -F "angle=45" \
  -F "text_color=#FF0000" \
  http://localhost:5000/watermark \
  -o document_avec_filigrane.pdf
```

#### Filigrane texte en grille (données binaires)

```bash
curl -X POST \
  --data-binary @chemin/vers/votre/document.pdf \
  -H "Content-Type: application/octet-stream" \
  "http://localhost:5000/watermark/binary?text=CONFIDENTIEL&pattern=grid&opacity=0.3&angle=45&text_color=%23FF0000" \
  -o document_avec_filigrane.pdf
```

#### Filigrane texte à position spécifique (multipart/form-data)

```bash
curl -X POST \
  -F "file=@chemin/vers/votre/document.pdf" \
  -F "text=CONFIDENTIEL" \
  -F "pattern=insert" \
  -F "x=0.5" \
  -F "y=0.5" \
  -F "horizontal_alignment=center" \
  http://localhost:5000/watermark \
  -o document_avec_filigrane.pdf
```

#### Filigrane texte à position spécifique (données binaires)

```bash
curl -X POST \
  --data-binary @chemin/vers/votre/document.pdf \
  -H "Content-Type: application/octet-stream" \
  "http://localhost:5000/watermark/binary?text=CONFIDENTIEL&pattern=insert&x=0.5&y=0.5&horizontal_alignment=center" \
  -o document_avec_filigrane.pdf
```

#### Filigrane image

```bash
curl -X POST \
  -F "file=@chemin/vers/votre/document.pdf" \
  -F "image=@chemin/vers/votre/logo.png" \
  -F "pattern=grid" \
  -F "opacity=0.2" \
  http://localhost:5000/watermark \
  -o document_avec_filigrane.pdf
```

### Avec Python (requests)

#### Utilisation avec multipart/form-data

```python
import requests

url = "http://localhost:5000/watermark"
files = {
    "file": open("chemin/vers/votre/document.pdf", "rb"),
    # Utiliser soit "image" soit "text"
    # "image": open("chemin/vers/votre/logo.png", "rb")
}
data = {
    "text": "CONFIDENTIEL",
    "pattern": "grid",
    "opacity": "0.3",
    "angle": "45",
    "text_color": "#FF0000",
    "save_as_image": "true",
    "dpi": "300"
}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    with open("document_avec_filigrane.pdf", "wb") as f:
        f.write(response.content)
    print("Document avec filigrane enregistré avec succès.")
else:
    print(f"Erreur: {response.json()}")
```

#### Utilisation avec données binaires

```python
import requests

# URL avec les paramètres du filigrane en query parameters
url = "http://localhost:5000/watermark/binary?text=CONFIDENTIEL&pattern=grid&opacity=0.3&angle=45&text_color=%23FF0000"

# Lire le fichier PDF en binaire
with open("chemin/vers/votre/document.pdf", "rb") as f:
    pdf_data = f.read()

# Envoyer la requête avec les données binaires
headers = {"Content-Type": "application/octet-stream"}
response = requests.post(url, data=pdf_data, headers=headers)

if response.status_code == 200:
    with open("document_avec_filigrane.pdf", "wb") as f:
        f.write(response.content)
    print("Document avec filigrane enregistré avec succès.")
else:
    print(f"Erreur: {response.json()}")
```

## Déploiement en production

Pour un déploiement en production, vous pouvez utiliser Gunicorn :

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Licence

Propriétaire - USTS.ai 2025
