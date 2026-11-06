# Benchmark sources and update notes

Updated 6 November 2026. The project page’s [Library](https://harbinzzy.github.io/projects/aioir/#library) and [Leaderboard](https://harbinzzy.github.io/projects/aioir/#leaderboard) share [`catalog.json`](catalog.json). The website fetches this public file and uses a checked-in snapshot if GitHub is unavailable. README tables are generated from the same file with [`scripts/sync_catalog.py`](../scripts/sync_catalog.py).

## What was updated

- Added ClusIR, QuReC, DRNet, SLER-IR, DCMPC-Net and WeatherRemover to their matching benchmark settings: 12 result rows.
- Added a separate **WeatherBench** real-world track with ClusIR and eight reproduced baselines, including PSNR, SSIM and LPIPS: 9 rows.
- Corrected the swapped **InstructIR-5D SOTS / Rain100L columns**. Original Table 2 orders deraining before dehazing; the README orders dehazing first. Correct values are SOTS **27.10 / 0.956** and Rain100L **36.84 / 0.973**. Average remains **29.55 / 0.907**.
- Imported the maintained year-grouped paper list (273 distinct titles) without inventing missing paper or code links.

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

## Publication metadata

Publication venues are checked against publisher DOI records, official proceedings and the TMLR paper catalogue. Journal years use the final publisher citation year when a volume has been assigned; an earlier preprint, acceptance, DOI suffix or early-access year can differ. For example, U-WADN is assigned to the January 2027 Information Sciences issue, while its DOI was registered in 2026.

| Paper | Publication | Record |
| --- | --- | --- |
| Adaptive Blind All-in-One Image Restoration | CVIU 2026 | [Publication](https://doi.org/10.1016/j.cviu.2026.104795) |
| Prompt-in-Prompt Learning for All-in-One Image Restoration | PR 2026 | [Publication](https://doi.org/10.1016/j.patcog.2026.114401) |
| Any Image Restoration via Efficient Spatial-Frequency Degradation Adaptation | TMLR 2026 | [Publication](https://jmlr.org/tmlr/papers/bib/RObgCpdDqr.bib) |
| Learning Continuous Wasserstein Barycenter Space for Generalized All-in-One Image Restoration | TPAMI 2026 | [Publication](https://doi.org/10.1109/TPAMI.2026.3669121) |
| DSwinIR: Rethinking Window-Based Attention for Image Restoration | TPAMI 2026 | [Publication](https://doi.org/10.1109/TPAMI.2025.3646016) |
| Beyond Degradation Redundancy: Contrastive Prompt Learning for All-in-One Image Restoration | TPAMI 2026 | [Publication](https://doi.org/10.1109/TPAMI.2025.3642852) |
| Perceive-IR: Learning to Perceive Degradation Better for All-in-One Image Restoration | TIP 2026 | [Publication](https://doi.org/10.1109/TIP.2025.3566300) |
| Multi-Expert Adaptive Selection: Task-Balancing for All-in-One Image Restoration | TCSVT 2025 | [Publication](https://doi.org/10.1109/TCSVT.2024.3516074) |
| UARE: A Unified Vision-Language Model for Image Quality Assessment, Restoration, and Enhancement | CVPR 2026 | [Publication](https://openaccess.thecvf.com/content/CVPR2026/html/Li_UARE_A_Unified_Vision-Language_Model_for_Image_Quality_Assessment_Restoration_CVPR_2026_paper.html) |
| PhyDAE: Physics-Guided Degradation-Adaptive Experts for All-in-One Remote Sensing Image Restoration | TGRS 2026 | [Publication](https://doi.org/10.1109/TGRS.2026.3656356) |
| TAP: Parameter-efficient Task-Aware Prompting for Adverse Weather Removal | ACM MM 2025 | [Publication](https://doi.org/10.1145/3746027.3755866) |
| CMAWRNet: Multiple Adverse Weather Removal via a Unified Quaternion Neural Architecture | Journal of Imaging 2025 | [Publication](https://doi.org/10.3390/jimaging11110382) |
| DPMambaIR: All-in-One Image Restoration via Degradation-Aware Prompt State Space Model | TMM 2026 | [Publication](https://doi.org/10.1109/TMM.2026.3717468) |
| Lumina-OmniLV: A Unified Multimodal Framework for General Low-Level Vision | ECCV 2026 | [Publication](https://link.springer.com/chapter/10.1007/978-3-032-37041-9_22) |
| VL-UR: Vision-Language-guided Universal Restoration of Images Degraded by Adverse Weather Conditions | ICME 2025 | [Publication](https://doi.org/10.1109/ICME59968.2025.11209564) |
| UniCoRN: Latent Diffusion-based Unified Controllable Image Restoration Network across Multiple Degradations | WACV 2026 | [Publication](https://openaccess.thecvf.com/content/WACV2026/html/Mandal_UniCoRN_Latent_Diffusion-based_Unified_Controllable_Image_Restoration_Network_across_Multiple_WACV_2026_paper.html) |
| USRNet: Unified Scene Recovery Network for Image Restoration under Multiple Adverse Weather Conditions | PR 2026 | [Publication](https://doi.org/10.1016/j.patcog.2025.112534) |
| Boosting Filter Optimization and Prompt-Guided Decoding for Mixed Degradation Image Restoration | IJCV 2026 | [Publication](https://link.springer.com/article/10.1007/s11263-026-02832-0) |
| Diff-Restorer: Unleashing Visual Prompts for Diffusion-based Universal Image Restoration | TCSVT 2026 | [Publication](https://doi.org/10.1109/TCSVT.2025.3629686) |
| Referring Flexible Image Restoration | Expert Systems with Applications 2025 | [Publication](https://doi.org/10.1016/j.eswa.2025.126857) |
| Joint Conditional Diffusion Model for Image Restoration with Mixed Degradations | Neurocomputing 2025 | [Publication](https://doi.org/10.1016/j.neucom.2025.129512) |
| AoSRNet: All-in-One Scene Recovery Networks via Multi-knowledge Integration | Knowledge-Based Systems 2024 | [Publication](https://doi.org/10.1016/j.knosys.2024.111786) |
| Unified-Width Adaptive Dynamic Network for All-In-One Image Restoration | Information Sciences 2027 | [Publication](https://doi.org/10.1016/j.ins.2026.123974) |
| Textual Prompt Guided Image Restoration | Engineering Applications of Artificial Intelligence 2025 | [Publication](https://doi.org/10.1016/j.engappai.2025.110981) |
| DDCNet: Advanced Decoupling of Degradation and Content for Adverse Weather Image Restoration | TNNLS 2025 | [Publication](https://doi.org/10.1109/TNNLS.2025.3594492) |
| On Efficient Transformer-Based Image Pre-training for Low-Level Vision | IJCAI 2023 | [Publication](https://www.ijcai.org/proceedings/2023/121) |
| TAPE: Task-Agnostic Prior Embedding for Image Restoration | ECCV 2022 | [Publication](https://link.springer.com/chapter/10.1007/978-3-031-19797-0_26) |
| RamIR: Reasoning and action prompting with Mamba for all-in-one image restoration | Applied Intelligence 2025 | [Publication](https://link.springer.com/article/10.1007/s10489-024-06226-y) |
| Learning Dual Transformers for All-in-One Image Restoration From a Frequency Perspective | TNNLS 2026 | [Publication](https://doi.org/10.1109/TNNLS.2026.3701139) |

The 2024 AnyIR preprint (2407.13372) and the later spatial-frequency paper (2504.14249, TMLR 2026) remain distinct entries. Shared code repositories do not establish publication identity. Benchmark rows use an explicit `paperTitle` reference: `sync_catalog.py` propagates the linked paper's venue, paper URL and code URL, and `--check` rejects stale metadata. Baseline result values and training settings are preserved.
