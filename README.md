# Suivi DCAM – MSCI World (PEA)

Site statique qui suit l'ETF Amundi PEA Monde (DCAM) : cours, courbes, mon investissement,
comparaison avec WPEA et CW8, performances annuelles du MSCI World, grosses baisses passées
et simulateur d'investissement mensuel.

Les données viennent gratuitement de Yahoo Finance (sans clé d'API) et sont mises à jour
automatiquement chaque soir de semaine par GitHub Actions.

## Mise en ligne sur GitHub Pages

1. Crée un dépôt public sur GitHub et envoie-y tous les fichiers (y compris le dossier `.github`).
2. **Settings → Actions → General → Workflow permissions** : coche « Read and write permissions ».
3. **Settings → Pages** : Source « Deploy from a branch », branche `main`, dossier `/ (root)`.
4. **Actions → Mise à jour des données → Run workflow** pour une première mise à jour.

Le site est ensuite à l'adresse `https://<ton-pseudo>.github.io/<nom-du-depot>/`.

## Tester en local

```bash
pip install yfinance
python scripts/fetch_data.py
python -m http.server
```
puis ouvre http://localhost:8000.

## Fichiers

- `index.html` : le site (graphiques avec Chart.js)
- `data.json` : les cours, régénérés automatiquement
- `scripts/fetch_data.py` : télécharge les cours
- `.github/workflows/update-data.yml` : la mise à jour automatique

Outil d'information, pas un conseil en investissement.
