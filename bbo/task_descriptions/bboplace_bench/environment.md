# Environment Setup

This task wraps a published BBOPlace-Bench evaluator image behind an HTTP API instead of rebuilding the full upstream benchmark inside this repository.
The current published image referenced by this repo is `gaozhixuan/bboplace-bench` on Docker Hub.

## Host requirements

- Docker Engine with permission to pull and run public images.
- Python 3.11+ and `uv` for this repo.
- Optional: GPU-enabled Docker runtime if your local deployment of the image expects GPU access.

## Pull the evaluator image

```bash
docker pull gaozhixuan/bboplace-bench
```

## Run the evaluator service

CPU-style invocation:

```bash
docker run --rm -p 8080:8080 gaozhixuan/bboplace-bench
```

If your local setup requires GPU access, add `--gpus all` before the image name.
The `--rm` flag is convenient for disposable smoke tests; omit it if you want to keep the container around for debugging or to inspect logs after exit.

The packaged task defaults to `http://127.0.0.1:8080` and posts evaluations to `/evaluate`.
Override the base URL when the service is hosted elsewhere:

```bash
export BBOPLACE_BASE_URL=http://127.0.0.1:8080
```

## Install this repo

```bash
uv sync --extra dev
```

## Smoke test

With the container running, execute:

```bash
export BBOPLACE_BASE_URL=http://127.0.0.1:8080
uv run python -m bbo.run --algorithm random_search --task bboplace_bench --max-evaluations 1
```

A healthy setup should complete without connection or JSON-schema errors and write run artifacts under `artifacts/`.
If you need the full upstream workflow, such as rebuilding DREAMPlace, downloading benchmark datasets, or running SP / HPO / GP-HPWL / PPA pipelines, follow the official BBOPlace-Bench repository rather than this lightweight HTTP wrapper.
