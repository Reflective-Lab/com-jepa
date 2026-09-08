# TabPFN-3 GPU comparison

This optional adapter compares a pretrained TabPFN-3 classifier with the Random Forest and historical base rate on the **same fictional data, temporal split, feature allowlist, and scoring targets**. It does not change the generator, label the discussion cases, or introduce real organisational data.

## What is pinned

| Component | Selection |
| --- | --- |
| TabPFN package | `8.5.0` |
| PyTorch | `2.11.0`, official CUDA 13.0 build for the GPU experiment |
| Model repository | `Prior-Labs/tabpfn_3` |
| Model revision | `24a16a89d245878b846555110985634aa2e656d7` |
| Checkpoint | `tabpfn-v3-classifier-v3_default.ckpt` |
| Checkpoint SHA-256 | `d0d865d54dfbc524f5703104be90620182dca7e5fb2c16de72e9959ea18f3988` |
| Candidate ensemble | Four estimators; automatic ensemble scaling disabled |
| Test protocol | One test row per prediction call, fixed historical training context |

The adapter verifies the checkpoint hash before loading it. It requires CUDA and does not silently fall back to another model or device. A future checkpoint comparison must update provenance explicitly.

## Environment and model access

The GPU setup uses Linux ARM64, Python 3.12, and an NVIDIA GB10. The pinned tabular dependencies also support this Python version. Create an isolated environment on the GPU machine; keep its existing inference service separate.

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cu130
.venv/bin/python -m pip install -r requirements-tabpfn.txt
.venv/bin/python -m pip check
```

The [upstream package](https://github.com/PriorLabs/TabPFN) documents local inference. The model weights and outputs have a [separate non-commercial licence](https://huggingface.co/Prior-Labs/tabpfn_3/blob/24a16a89d245878b846555110985634aa2e656d7/LICENSE). The repository's MIT licence does not grant production rights for TabPFN. This example is a non-commercial synthetic evaluation; it does not distribute weights, distil their outputs into another model, or deploy a service.

After reviewing the applicable model terms, download the fixed revision:

```sh
.venv/bin/python - <<'PY'
from huggingface_hub import hf_hub_download
from com_jepa.tabpfn_demo import MODEL_REPO, MODEL_REVISION, MODEL_FILENAME
for filename in ('LICENSE', MODEL_FILENAME):
    hf_hub_download(
        repo_id=MODEL_REPO, revision=MODEL_REVISION, filename=filename,
        local_dir='artifacts/tabpfn-3',
    )
PY
```

At initial inspection this revision was publicly downloadable without authentication. If access requirements change, use the publisher's authorised access process. The adapter never accepts a licence, logs into an account, or downloads an unspecified replacement model.

## Run the experiment

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m com_jepa validate examples/fictional-trajectory.jsonl
.venv/bin/python -m com_jepa.tabpfn_demo \
  --checkpoint artifacts/tabpfn-3/tabpfn-v3-classifier-v3_default.ckpt \
  --output artifacts/tabpfn-comparison.json
.venv/bin/python -m pip freeze > artifacts/tabpfn-environment.txt
```

The output file must be new. The model and reports stay in ignored `artifacts/`. To initiate an already prepared run from another machine, use SSH to the experiment checkout and invoke the same module. Host aliases and paths are operator configuration, not embedded in the adapter.

The default PyTorch allocator budget is 4 GiB, adjustable with `--gpu-memory-gib` up to 8 GiB. This is not a hard bound on all process or unified-memory use. Check available memory and other workloads before running. The adapter does not stop, replace, or reconfigure an existing model service, and no GPU runner is added to CI.

## What is compared

The adapter first runs the original forest demonstration, then reconstructs and verifies identical training/test identities and exclusions. The pretrained candidate gets only the selected training features and labels. It processes each test row separately; it never receives future test rows or any test labels as context. Four feature values and the fixed historical examples are its entire task input.

TabPFN uses external pretraining, so equal task data does not imply equal total training information or compute. This is a practical estimator comparison, not an experiment isolating model architecture from pretraining. It is also not a JEPA experiment or a test of organisational transfer.

The JSON report extends the baseline report with candidate metrics, per-row probabilities, checkpoint provenance, code hashes, device/library versions, timing, and peak PyTorch memory. `fit` includes checkpoint loading and preparation of the training context; it is not fine-tuning the neural weights. Prediction time covers individual calls and must not be advertised as maximum batched throughput. The machine may be sharing its GPU with another workload.

GPU timings and floating-point outputs need not be bitwise reproducible across hardware and versions. Preserve the environment capture alongside the report. A single generator/seed cannot establish broad model superiority, even if one model scores better on this run. Probability calibration, uncertainty intervals, multiple reviewed generators, and real-data evaluation remain separate work.

## Testing boundaries

Unit tests verify checkpoint rejection, positive-class mapping, probability validity, and one-row-per-call isolation without downloading a model. The existing temporal and missing-label tests still apply. A real checkpoint execution is a separate, explicitly invoked GPU experiment, not a stubbed test result.
