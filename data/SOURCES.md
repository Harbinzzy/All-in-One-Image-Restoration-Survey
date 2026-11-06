# Benchmark sources and update notes

Updated 6 November 2026. The [paper library](https://harbinzzy.github.io/projects/aioir/) and [leaderboard](https://harbinzzy.github.io/projects/aioir/leaderboard.html) share [`catalog.json`](catalog.json). The website fetches this public file and uses a checked-in snapshot if GitHub is unavailable. README tables are generated from the same file with [`scripts/sync_catalog.py`](../scripts/sync_catalog.py).

## What was updated

- Added ClusIR, QuReC, DRNet, SLER-IR, DCMPC-Net and WeatherRemover to their matching benchmark settings: 12 result rows.
- Added a separate **WeatherBench** real-world track with ClusIR and eight reproduced baselines, including PSNR, SSIM and LPIPS: 9 rows.
- Corrected the swapped **InstructIR-5D SOTS / Rain100L columns**. Original Table 2 orders deraining before dehazing; the README orders dehazing first. Correct values are SOTS **27.10 / 0.956** and Rain100L **36.84 / 0.973**. Average remains **29.55 / 0.907**.
- Imported the maintained year-grouped paper list (270 distinct titles) without inventing missing paper or code links.

## Original sources used for additions

| Method | Original paper | Tables used | Settings |
| --- | --- | --- | --- |
| ClusIR | [2512.10948](https://arxiv.org/abs/2512.10948) | [1](https://arxiv.org/html/2512.10948#S3.T1), [2](https://arxiv.org/html/2512.10948#S3.T2), [4](https://arxiv.org/html/2512.10948#S3.T4), [5](https://arxiv.org/html/2512.10948#S4.T5), S2 | Three tasks, five tasks, CDD-11, WeatherBench; 54.66M base model |
| QuReC | [2607.15097](https://arxiv.org/abs/2607.15097) | [1](https://arxiv.org/html/2607.15097#S3.T1), [2](https://arxiv.org/html/2607.15097#S4.T2), [3](https://arxiv.org/html/2607.15097#S4.T3) | Three tasks, five tasks, CDD-11; 29.61M |
| DRNet | [2605.08627](https://arxiv.org/abs/2605.08627) | [I](https://arxiv.org/html/2605.08627#S3.T1), [II](https://arxiv.org/html/2605.08627#S3.T2), VII | Five tasks, three tasks; 7.39M inference model |
| SLER-IR | [2603.05940](https://arxiv.org/abs/2603.05940) | [1](https://arxiv.org/html/2603.05940#S3.T1), [2](https://arxiv.org/html/2603.05940#S4.T2) | Three tasks, five tasks; parameter count left unreported |
| DCMPC-Net | [2608.06939](https://arxiv.org/abs/2608.06939) | [I](https://arxiv.org/html/2608.06939#S4.T1), [XI](https://arxiv.org/html/2608.06939#S4.T11) | All-Weather; restoration model 37.60M, excluding vision-language / text encoders |
| WeatherRemover | [2604.06623](https://arxiv.org/abs/2604.06623) | [I](https://arxiv.org/html/2604.06623#S4.T1), [II](https://arxiv.org/html/2604.06623#S4.T2), [III](https://arxiv.org/html/2604.06623#S4.T3) | All-Weather **Multi Weather** rows; 24.3M |
| InstructIR correction | [2401.16468](https://arxiv.org/abs/2401.16468) | [2](https://arxiv.org/html/2401.16468#S4.T2) | Five-task SOTS / Rain100L column order |

All listed sources were retrieved and their relevant tables inspected on 6 November 2026. Venue labels follow the maintained paper catalogue. These are author-reported values, not new independent evaluations. This update is a verified selection of recent papers with matching results; it does not claim every recent paper has been exhaustively evaluated.

## Comparability and averages

1. **Existing baselines:** preserved from [the survey, arXiv v3, Tables II–VI](https://arxiv.org/html/2410.15067v3#S4.T2), except the documented InstructIR correction. A model’s results and parameters may differ across independently trained settings. Do not replace a baseline with a number from a different paper or setting merely because the method name matches.
2. **Three / five tasks:** legacy headers use BSD68; ClusIR and SLER-IR call the color set CBSD68. Five-task denoising uses σ = 25. The three-task average covers haze, rain and the three noise levels, not three equally weighted task means.
3. **All-Weather:** Snow is Snow100K-L; Rain+Fog is Outdoor-Rain; Raindrop is RainDrop-A. DCMPC-Net’s Table I reports a four-dataset mean including Snow100K-S. For compatibility with the existing three-column table, compute **(32.35 + 32.49 + 33.08) / 3 = 32.64 dB** and **(0.9302 + 0.9477 + 0.9474) / 3 = 0.9418 SSIM**. Its reported four-dataset average, 34.03 / 0.9486, is deliberately not substituted.
4. **WeatherRemover:** use the Multi Weather rows, **30.87 / 0.9121**, **31.52 / 0.9170**, **31.51 / 0.9307**. The mean computed here is **31.30 / 0.9199**. Single-weather-trained results are excluded. Its training mixture is 9,000 snow + 1,069 raindrop + 9,000 Outdoor-Rain images. DCMPC-Net uses a different reported mixture of 9,001 + 818 + 8,250 = 18,069 images. Thus even these multi-weather results are not guaranteed to use identical training data.
5. **Real-world:** WeatherStream, the survey’s Real-World dataset and WeatherBench are isolated tracks. WeatherBench baseline scores are reproduced from ClusIR Table 5, with that provenance attached to every row. LPIPS is lower-is-better. Other metrics are higher-is-better.
6. **Reported means:** retained exactly, including source rounding. Only the two explicitly identified All-Weather means are computed here. Parameters include “+” components as given by the source; missing or ambiguous counts are not guessed. DCMPC-Net’s asterisk denotes omitted external encoder parameters.
7. **Scope:** PVRF ([2605.14045](https://arxiv.org/abs/2605.14045)) was checked but excluded from these tables: its five-task setting includes desnowing, not the requested denoising benchmark. Real-image quality scores without matching PSNR / SSIM or datasets are not inserted into the older WeatherStream comparison.

## Keeping GitHub and the website in sync

Edit verified result entries in `data/catalog.json`, including `source`, `sourceLabel`, `note`, exact model variant, dataset track and parameter convention. Update `updated` when publishing changes, then run:

```sh
python scripts/sync_catalog.py --import-papers
python scripts/sync_catalog.py --check
```

If the Pages repository is checked out locally, refresh its offline snapshot too:

```sh
python scripts/sync_catalog.py --site ../Harbinzzy.github.io/projects/aioir
python scripts/sync_catalog.py --check --site ../Harbinzzy.github.io/projects/aioir
```

The live website reads the public JSON after rendering its local snapshot. No credentials, write-enabled browser tokens or framework build service are needed.
