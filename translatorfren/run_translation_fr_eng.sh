#!/bin/bash

#'''
#replicas: An argument for parallel preprocessing. For example, when replicas=3,
#we divide the data into three parts, and only process one part
#according to the worker_id.
#'''
replicas=1
worker_id=0

sampling_temp=$1

echo 'use sampling temp '${sampling_temp}

input_file='fr_text.txt'

cat $input_file

# Dirs
data_dir=back_trans_data
doc_len_dir=${data_dir}/doc_len
src_dir=${data_dir}/src_dir
gen_dir=${data_dir}/gen_dir
para_dir=${data_dir}/paraphrase

mkdir -p ${data_dir}
mkdir -p ${src_dir}
mkdir -p ${gen_dir}
mkdir -p ${doc_len_dir}
mkdir -p ${para_dir}

echo "*** spliting paragraph ***"
echo "write to "${para_dir}/file_${worker_id}_of_${replicas}.json

# install nltk
python split_paragraphs.py \
  --input_file=${input_file} \
  --output_file=${src_dir}/file_${worker_id}_of_${replicas}.txt \
  --doc_len_file=${doc_len_dir}/doc_len_${worker_id}_of_${replicas}.json \
  --replicas=${replicas} \
  --worker_id=${worker_id} \


echo "*** translation Fr En ***"
t2t-decoder \
  --problem=translate_enfr_wmt32k_rev \
  --model=transformer \
  --hparams_set=transformer_big \
  --hparams="sampling_method=random,sampling_temp=${sampling_temp}" \
  --decode_hparams="beam_size=1,batch_size=16,alpha=0" \
  --checkpoint_path=checkpoints/fren/model.ckpt-500000 \
  --output_dir=/tmp/t2t \
  --decode_from_file=${src_dir}/file_${worker_id}_of_${replicas}.txt \
  --decode_to_file=${gen_dir}/file_${worker_id}_of_${replicas}.txt \
  --data_dir=checkpoints

echo "*** transform sentences back into paragraphs***"
python sent_to_paragraph.py \
  --input_file=${gen_dir}/file_${worker_id}_of_${replicas}.txt \
  --doc_len_file=${doc_len_dir}/doc_len_${worker_id}_of_${replicas}.json \
  --output_file=${para_dir}/file_${worker_id}_of_${replicas}.json


