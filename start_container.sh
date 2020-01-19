docker build --rm -f "translatorfren/Dockerfile" -v `pwd`/checkpoints/.:/work/checkpoints -t chritter/translatorfren:latest "translatorfren"
