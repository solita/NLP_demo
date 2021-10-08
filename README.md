# NLP demo
Demotaan NLP-menetelmien käyttöä tekstin luokittelussa.

Käynnistä komennolla:

```bash
bash run-demo.sh &
```

Demo toimii Pythonin Jupyter lab -moduulilla. Käynnistääksesi Jupyter labin, etsi konsolista alla olevan kaltainen rivi
```bash
NLP_python  |     To access the server, open this file in a browser:
NLP_python  |         file:///home/ml_user/.local/share/jupyter/runtime/jpserver-1-open.html
NLP_python  |     Or copy and paste one of these URLs:
NLP_python  |         http://c389eac31c44:8888/lab?token=<tunniste>
NLP_python  |      or http://127.0.0.1:8888/lab?token=<tunniste>
```
ja kopio se selaimeesi.

Katso myös ohjeet notebookin *demo.ipynb* alusta datan hakua, lähteitä jne varten. */notebooks* -kansiossa on myös tiedosto *browse_imdb_data.py* imdb-datan selailua varten.

Pysäytä komennolla:

```bash
docker compose down
```
