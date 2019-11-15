# Notes Translator

## Getting Started

* Create a container based on the Dockerfile. Maps API endpoints to port 8000 of host machine
* Access FastAPI docs with http://0.0.0.0:8000/docs

## API details
* Provides 2 endpoints for translation from Fr-En and En-Fr

## Algo Implementation Details

* Model published in Xie19 by Google Research, see github UDA
* Splits text into pagraphas, dthen translates each, and assembles back
* Leverages t2t-decoder 
    * translate_enfr_wmt32k
    * English-French: --problem=translate_enfr_wmt32k



