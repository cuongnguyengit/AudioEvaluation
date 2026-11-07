# AudioEvaluation — MOS listening test for TTS

A tiny Flask web app for running **Mean Opinion Score (MOS)** listening tests on text-to-speech output. Listeners
enter a few demographic fields (age, region/dialect, sex), play each sample and rate it 1–5; ratings are appended to
`result.txt` for analysis.

I used it in 2021 to compare Vietnamese TTS models (Tacotron 2, FastSpeech 2, FastPitch) with native listeners from
different dialect regions — dialect matters a lot when judging Vietnamese naturalness.

## Run

```bash
pip install -r requirements.txt
python main.py --port 8000          # open http://localhost:8000
```

- Put the samples to rate in `wavs/` and list them (with their transcripts) in `show_entries()` in `main.py`.
- Each submission writes lines `name|age|region|sex|file|score` to `result.txt`; `GET /admin/get` downloads it.
- `Procfile` / `runtime.txt` allow a one-click Heroku-style deploy.

Compute MOS per system from `result.txt`, e.g.:

```python
import pandas as pd
df = pd.read_csv("result.txt", sep="|", names=["name", "age", "region", "sex", "file", "score"])
print(df.groupby("file")["score"].agg(["mean", "count"]))
```

## Caveats

This is a demo-grade tool: there is no authentication, the static route serves the app directory (including
`result.txt`), and listener names are stored in plain text. Run it on a private network or add auth before collecting
real ratings, and do not commit `result.txt` (it is git-ignored).
