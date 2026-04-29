---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:22794
- loss:OnlineContrastiveLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: Computed Tomography Scan CHEST WITHOUT CNTRST
  sentences:
  - Magnetic Resonance Imaging BRAIN WITHOUT AND WITH CONTRAST
  - FOOT, LEFT - COMPL MIN 3 VWS
  - Xray Chest 1 view Frontal Only
- source_sentence: Visual Analogue Scale transcranial doppler
  sentences:
  - Computed Tomography Scan abdomen pelvis w con
  - Xray Chest 1 view Frontal Only
  - MAMMOGRAPHY SCREEN BILAT W Computer-Aided Detection
- source_sentence: Ultrasound pelvis AND ENDOVAGINAL
  sentences:
  - Mammography SCREEN BILAT W/ Computer-Aided Detection/Tomosynthesis
  - MAMMOGRAPHY SCREENING BILATERAL
  - CERVICL SPINE, MIN 4 VIEWS
- source_sentence: Computed Tomography Scan abdomen pelvis w con
  sentences:
  - Echocardiogram Stress Echocardiogram NC for report
  - Ultrasound transvaginal
  - Computed Tomography Scan LUMBAR SPINE WITHOUT CNTRST
- source_sentence: Computed Tomography Scan abdomen pelvis w con
  sentences:
  - Visual Analogue Scale Ultrasound carotid BIL
  - Ultrasound THYROID/SOFT TISSUE NECK
  - Computed Tomography Scan LE left wo con
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision c9745ed1d9f207416be6d2e6f8de32d1f16199bf -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'Computed Tomography Scan abdomen pelvis w con',
    'Computed Tomography Scan LE left wo con',
    'Ultrasound THYROID/SOFT TISSUE NECK',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.7525, 0.6074],
#         [0.7525, 1.0000, 0.5953],
#         [0.6074, 0.5953, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 22,794 training samples
* Columns: <code>sentence1</code>, <code>sentence2</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence1                                                                         | sentence2                                                                         | label                                           |
  |:--------|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:------------------------------------------------|
  | type    | string                                                                            | string                                                                            | int                                             |
  | details | <ul><li>min: 5 tokens</li><li>mean: 12.06 tokens</li><li>max: 20 tokens</li></ul> | <ul><li>min: 3 tokens</li><li>mean: 10.02 tokens</li><li>max: 23 tokens</li></ul> | <ul><li>0: ~81.60%</li><li>1: ~18.40%</li></ul> |
* Samples:
  | sentence1                              | sentence2                                            | label          |
  |:---------------------------------------|:-----------------------------------------------------|:---------------|
  | <code>Xray pelvis, 1 or 2 views</code> | <code>Computed Tomography Scan LE left wo con</code> | <code>1</code> |
  | <code>Xray pelvis, 1 or 2 views</code> | <code>Xray hip bilateral w AP pelvis min 5V</code>   | <code>1</code> |
  | <code>Xray pelvis, 1 or 2 views</code> | <code>Xray lumbar spine limited</code>               | <code>1</code> |
* Loss: [<code>OnlineContrastiveLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#onlinecontrastiveloss) with these parameters:
  ```json
  {
      "distance_metric": "SiameseDistanceMetric.COSINE_DISTANCE",
      "margin": 0.5
  }
  ```

### Evaluation Dataset

#### Unnamed Dataset

* Size: 4,820 evaluation samples
* Columns: <code>sentence1</code>, <code>sentence2</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence1                                                                        | sentence2                                                                         | label                                           |
  |:--------|:---------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:------------------------------------------------|
  | type    | string                                                                           | string                                                                            | int                                             |
  | details | <ul><li>min: 4 tokens</li><li>mean: 9.95 tokens</li><li>max: 17 tokens</li></ul> | <ul><li>min: 3 tokens</li><li>mean: 10.24 tokens</li><li>max: 24 tokens</li></ul> | <ul><li>0: ~75.10%</li><li>1: ~24.90%</li></ul> |
* Samples:
  | sentence1                         | sentence2                                                         | label          |
  |:----------------------------------|:------------------------------------------------------------------|:---------------|
  | <code>Xray lumbar puncture</code> | <code>pelvis</code>                                               | <code>0</code> |
  | <code>Xray lumbar puncture</code> | <code>Computed Tomography Scan ANGIOGRAM CARDIAC INSURANCE</code> | <code>0</code> |
  | <code>Xray lumbar puncture</code> | <code>Magnetic Resonance Imaging thoracic spine wo/w con</code>   | <code>0</code> |
* Loss: [<code>OnlineContrastiveLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#onlinecontrastiveloss) with these parameters:
  ```json
  {
      "distance_metric": "SiameseDistanceMetric.COSINE_DISTANCE",
      "margin": 0.5
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 64
- `learning_rate`: 2e-05
- `warmup_steps`: 0.1
- `per_device_eval_batch_size`: 64

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 64
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 2e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0.1
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1.0
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 64
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 1.4006 | 500  | 0.7113        |
| 2.8011 | 1000 | 0.3051        |


### Training Time
- **Training**: 57.2 seconds

### Framework Versions
- Python: 3.14.0
- Sentence Transformers: 5.4.1
- Transformers: 5.6.2
- PyTorch: 2.11.0+cu130
- Accelerate: 1.13.0
- Datasets: 4.8.5
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->