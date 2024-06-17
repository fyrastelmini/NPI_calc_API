# API REST de calculatrice en Notation Polonaise Inverse (NPI)
![Test app](https://github.com/fyrastelmini/NPI_calc_API/actions/workflows/CI.yml/badge.svg)
![Test app (No UI)](https://github.com/fyrastelmini/NPI_calc_API/actions/workflows/CI_no_ui.yml/badge.svg)
![Docker CI](https://github.com/fyrastelmini/NPI_calc_API/actions/workflows/docker-CI.yml/badge.svg)

# Usage:
```bash
make run
```
ou

```bash
docker-compose up
```
# Versions:
Il existe deux versions de cet API, les deux connectés sur la même base de données:
    - Calculator app: Version avec une interface utilisateur web, se lance sur le port 5000
    - Calculator app (no UI): API simple sans interface web, se lance sur le port 5001
Les deux versions ont leurs documentations sous le chemin /docs

# Pour le développement:
# Installation, Pytest, Linting, Formatting
```bash
make all
```