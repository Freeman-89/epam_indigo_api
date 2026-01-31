# Chemical Structure Renderer API


## POST /api/render

Renders an image from a SMILES string or a MOL file via multipart/form-data.

Form parameters:
- smiles — SMILES string (if used)
- mol — MOL file (if used)
- width (optional) — image width
- height (optional) — image height
- format (optional) — image format (svg or png)

Example request with SMILES:
```
curl -X POST "https://localhost:8000/api/render" \
  -F "smiles=CCO" \
  -F "width=400" -F "height=400" -F "format=png"
```

Example request with a MOL file:
```
curl -X POST "https://localhost:8000/api/render" \
  -F "mol=@ethanol.mol" \
  -F "width=400" -F "height=400" -F "format=svg"
```


## GET /api/render

Renders an image from a SMILES string.

Parameters:
- smiles (required) — SMILES string of the molecule
- width (optional, default=400) — image width
- height (optional, default=400) — image height
- format (optional, default=svg) — image format (svg or png)

Example request:
```
curl -v "https://localhost:8000/api/render?smiles=C(C1C(C(C(C(O1)O)O)O)O)O&width=400&height=400&format=svg"

```

## Setup

```
docker build -t chem-renderer .
docker run -p 0.0.0.0:8000:8000 chem-renderer
```

### Swagger

Swagger UI is available at:
You can view all API endpoints, their parameters, and try test requests directly from your browser.
```
https://localhost:8000/api/static/swagger
```