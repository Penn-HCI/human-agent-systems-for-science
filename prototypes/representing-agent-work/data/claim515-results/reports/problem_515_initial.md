# Decoding and repairing file-transfer authorization in Qwen2.5-7B-Instruct

| Field | Value |
|---|---|
| **Problem ID** | 515 |
| **Scenario** | Lack of adherence: Drift in long contexts, responses to knowledge conflict, incorrect tool use, bias |
| **Assessment Verdict** | +1 Likely feasible |
| **Likert Score** | +1 |
| **Confidence** | 0.78 |
| **Date** | 2026-10-05 |

## Bottom line

Correct permission information can remain accessible despite a wrong authorization decision: a frozen recipient decoder exceeds 90% even on errors, while a working nine-head intervention exceeds the repair target without changing any initially correct decisions. The assessment is **+1 Likely feasible**, score **+1**, confidence **0.78**: the remaining hurdle is achieving the decoder and intervention results together under one frozen presentation and test distribution, rather than combining successes from different setups. [experiment_sc102] [experiment_sc6]

## 1. Introduction

> On 1,200 held-out file-transfer problems balanced between permitted and forbidden requests, with four files and four recipients, linear decoders of Qwen2.5-7B-Instruct's final prompt-token residual state identify the requested file and its permitted recipient with at least 90% accuracy each, even among incorrect authorization decisions. Patching a fixed set of at most 12 attention heads from correct runs containing the same permission facts in reordered table rows corrects at least 30% of all initial errors while changing no more than 3% of correct decisions. Decoders, heads, and donor-selection rules are fixed on separate development data, with decoders trained on both correct and incorrect development runs; test names and permission assignments are unseen.

I read this as an existential claim that one development-fixed configuration of the named model meets all six accuracy and intervention-rate criteria on the same held-out set, with identity labels defined consistently for unseen names and correct donors verified by a prespecified procedure.

1. Both identities must be decoded at least 90% accurately overall and separately among all initial authorization errors.
2. One fixed set of at most 12 heads must repair at least 30% of all initial errors while changing at most 3% of initially correct decisions.
3. Development/test separation, unseen names and assignments, and frozen selection rules must hold throughout.

Every part is required; their joint compatibility, particularly recipient decoding on the error distribution used for patching, decides the claim. This would distinguish inaccessible permission information from information the model represents but fails to use, enabling targeted adherence interventions.

## 2. What the literature establishes

The closest work concerns **binding**, the internal association between an entity and its attribute—in this case, a file and its permitted recipient.

| Prior work | Published result beside the claim's threshold | Relevance and boundary |
|---|---|---|
| *Legible failures* | Qwen2.5-7B **Base**: failure-conditioned linear binding accuracy 27.6%, seed range 23.6–34.5%, versus the claim's 90%. In a separate steering setting: 29% repair and 79% preservation, versus required 30% repair and at least 97% preservation. | Direct evidence that prompt-supplied bindings can survive wrong answers, but neither its model variant nor residual-direction intervention matches the claim. [web_legible_failures_error_decoding_and_steering](https://arxiv.org/abs/2609.11216) |
| *How do Language Models Bind Entities in Context?* | On two-binding tests, control accuracy exceeds 99%; separate entity or attribute interventions reduce original-association accuracy below 3%; simultaneous interventions restore it above 97%. | Establishes manipulable binding representations in LLaMA/Pythia. The restoration reverses an artificial intervention, not natural authorization errors, and does not establish sparse-head repair. [web_binding_id_representations](https://arxiv.org/abs/2310.17191) |
| *Mixing Mechanisms* | A model combining positional, lexical and direct-pointer retrieval achieves 0.95 Jensen–Shannon similarity, a measure of agreement between probability distributions. Experiments include Qwen2.5-7B-Instruct. | Supports causal accessibility at the final token, but 0.95 distribution similarity is not 95% identity-decoding accuracy. Different retrieval signals make fact-equivalent row orders potentially different activation donors. [web_mixing_mechanisms_qwen_binding](https://arxiv.org/abs/2510.06182) |

**The strongest published case for the claim** is the instruction-tuned OLMo binding result in *Legible failures*: 38% repair with 97% preservation already meets the claimed intervention-rate trade-off, albeit with residual steering rather than donor-head replacement. **The strongest published case against it** is the same paper's Qwen Base result above; even its four-binding replication across other models reaches only 47.4–79.9% failure-conditioned decoding. These results establish an actionable mechanism, not the conjunction of thresholds; the negative case survives as a warning about model, presentation and intervention-site dependence, rather than a bound on the four-file Instruct task. [web_legible_failures_error_decoding_and_steering](https://arxiv.org/abs/2609.11216)

## 3. What the literature leaves open

The literature does not settle identity decoding with unseen names and assignments on this authorization task. Frozen linear-decoder experiments therefore tested requested-file decoding, overall recipient decoding, and recipient decoding among initial errors; a higher-data recipient experiment tested whether a stronger readout could close the observed shortfall.

Nor does residual steering settle the fixed-head donor intervention. Two experiments tested active head-output replacement from correct row-reordered donors, scoring repair and preservation together; none measured both decoders and patching in one configuration.

## 4. What our experiments show

Intervals below are supplementary 95% Wilson intervals; the claim itself specifies finite-set point thresholds.

**Requested-file decoding cleared both file accuracy bounds in one distribution.** A block-20 decoder trained on correct and incorrect development runs achieved 1,175/1,200, or 97.92% accuracy (96.94–98.58%), against 90%. Its supplementary initial-error result was 123/125, or 98.40% (94.35–99.56%); recipient decoding and patching were not tested. [experiment_sc1]

**The smaller overall-recipient experiment fell substantially short.** With shared-stem identifiers, the request before a reversed-column table, and 8,192 training problems, the selected block-20 decoder achieved 849/1,200, or 70.75% (68.11–73.25%), against 90%. Above-control performance shows a learned but insufficient readout, not a nonfunctioning method. [experiment_sc2]

**Recipient decoding on errors also failed in a history-containing presentation.** A converged decoder trained on 4,096 development problems achieved 197/290, or 67.93% (62.35–73.04%), among all initial errors, against 90%. This is direct negative evidence for that admissible presentation, including confusable names and explicitly nonauthoritative routing history. [experiment_sc4]

**Eleven-head patching met both intervention bounds.** Replacing outputs at semantically aligned tokens repaired 112/123 errors, or 91.06% (84.69–94.93%), against 30%, while changing 2/1,077 correct decisions, or 0.1857% (0.05094–0.6746%), against 3%. Two errors without qualifying donors remained in the denominator; self-patching and random-head controls supported a selective intervention effect. [experiment_sc5]

**Nine-head final-token patching independently met the coupled bounds.** The development-fixed intervention repaired 213/229 errors, or 93.01% (88.95–95.65%), and changed 0/971 correct decisions, or 0% (upper interval bound 0.3941%). It used a different frozen donor-ranking rule and presentation, so it demonstrates another working intervention instance, not decoder compatibility. [experiment_sc6]

**The higher-data recipient experiment cleared the recipient bounds.** With 65,536 training problems, independent shared-stem names and catalog-slot labels, the frozen block-20 decoder achieved 1,141/1,200, or 95.08% (93.71–96.17%). Its supplementary initial-error result was 300/309, or 97.09% (94.56–98.46%), against 90%; the changed presentation and training procedure prevent attributing the improvement over the smaller experiment solely to dataset size. [experiment_sc102]

See Appendix A for experimental details and for runs that produced no measurement.

## 4b. In the News (non-academic sources)

The news and podcast channel found no relevant items.

## 5. Why the claim succeeds or fails

**The claim can be true if authorization errors leave the file–recipient association readable and reordered donors supply a better retrieval computation.** Binding interventions establish that associations are causally manipulable, while Qwen's mixed retrieval mechanisms explain why equivalent facts can produce different internal states. The claim allows choosing the residual layer, token alignment and donor procedure on development data; it does not require label-free donor verification or universal success across prompt formats. [web_binding_id_representations](https://arxiv.org/abs/2310.17191) [web_mixing_mechanisms_qwen_binding](https://arxiv.org/abs/2510.06182)

**The strongest evidence is now on the named authorization task, not merely analogous binding tasks.** Recipient decoding reached 95.08% overall and 97.09% on errors, while final-token sparse patching reached 93.01% repair with no observed correct-decision changes. Those working instances outweigh the much lower published Qwen Base results for these components, but they use different presentations and do not establish the full conjunction. [experiment_sc102] [experiment_sc6]

**Joint generalization remains the key driver, and the evidence shows a concrete route toward it.** The converged history-presentation decoder's 67.93% error accuracy is a real shortfall, not an optimization failure that can simply be dismissed. Within the higher-data presentation, a fixed layer and penalty yielded development-selection accuracies of 89.72%, 93.31% and 95.13% as training grew from 8,192 to 32,768 to 65,536 problems: generalization improved within one controlled readout family. This supports training a sufficiently strong decoder, but does not demonstrate that it retains those accuracies on the initial-error distribution where the sparse patch succeeds. [experiment_sc4] [compute_2]

## 6. Assessment

**The evidence favors +1 Likely feasible, score +1, confidence 0.78, within about three months for a relevant mechanistic-interpretability lab.** The estimate rests on component demonstrations with substantial threshold margins and a measured decoder learning curve, rather than on presumed resources or an unspecified future breakthrough. Confidence is below a demonstrated-feasibility judgment because the successful readouts and interventions were selected for different presentations, and the literature shows strong dependence on retrieval setting. [experiment_sc102] [web_legible_failures_error_decoding_and_steering](https://arxiv.org/abs/2609.11216)

**A single joint held-out demonstration would move the score up; repeated joint shortfalls would move it down.** An independently frozen configuration satisfying all four decoder bounds and both patching bounds would justify +2 Feasible. Conversely, if the high-data decoder falls below 90% on the sparse-patching error distribution, or the corresponding fixed patch cannot maintain at least 30% repair with at most 3% changes, repeated well-functioning attempts would undermine the compatibility argument and lower the score. These tests directly connect the existing isolated successes. [experiment_sc102] [experiment_sc6]

### Why not the neighbouring scores

**+2 Feasible would overstate demonstrated compatibility, while 0 Evenly balanced would underweight the working components.** The high-data catalog readout has not been shown to coexist with the nine-head patch on the same presentation and original errors, so transfer between those specific configurations remains consequential. Nevertheless, 95.08% overall recipient decoding, 97.09% error-conditioned decoding, and 93.01% repair with zero observed disruption are positive measurements beyond the required bounds, not merely reasons the claim cannot be ruled out. [experiment_sc102] [experiment_sc6]

## 7. Limitations and further directions

The sampled-task intervals do not measure variation across independently trained decoders or head selections. These synthetic, single-token authorization tasks also do not establish persistent adherence in long workflows; donor checking uses task ground truth, which is allowed here but does not demonstrate autonomous deployment. [experiment_sc102] [experiment_sc5]

**Further directions**

- Train both identity decoders on one patch-compatible development distribution, freeze every choice, and evaluate all six criteria on the same 1,200 held-out problems. Passing would establish the joint instance; failing would locate the remaining incompatibility.
- Repeat the recipient learning curve under an unchanged prompt, label mapping and permission split, including all initial errors. This would distinguish sample-size gains from presentation changes and determine whether the decoder shortfalls have a demonstrated remedy.
- Repeat the joint configuration with independent development/test draws and fixed donor budgets. Stable margins would strengthen confidence; unstable conditional decoding or preservation would lower it.

## Appendix A: Experimental Details

All measured experiments used the Hugging Face **Qwen/Qwen2.5-7B-Instruct** checkpoint, revision `a09a35458c702b33eeacc393d103063234e8bc28`: 7.616 billion parameters, frozen BF16 weights, native chat template, SDPA attention, and no quantization or generated reasoning. Every test contained four files, four recipients and exactly 600 permitted plus 600 forbidden requests; test names and canonical permission assignments were disjoint from development. Decoder inputs were one original, unnormalized post-block residual vector at the final actual prompt token; training-only coordinate standardization and affine classifiers preserved linear readouts. Model weights were never updated. [experiment_sc1] [experiment_sc102]

Percentages and intervals below retain the records' endpoint definitions. Wilson intervals are 95% unless stated; reported cluster bootstraps address repeated permission assignments. Uncertainty not supplied for a control is marked “not reported,” rather than inferred.

### A.1 Requested-file decoder

**Target:** at least 90% requested-file accuracy overall and on initial errors; lower measured accuracy would fail the relevant bound. **Model:** common Qwen checkpoint above. **Data:** locally generated FourFileTransfer-Generated-v1; 4,096 fitting, 1,024 validation, four pilots of 256, and a separate 512/128 disclosed-label control. Complete cyclic recipient-relabeling orbits divided permission vectors into 128 development and 128 test assignments.

**Procedure:** (1) Select the first prespecified pilot with a nontrivial error signal; independent opaque names were chosen. (2) Extract all block states and fit every layer/regularization candidate using both correctness groups. (3) Select on validation, freeze, generate the test set and score one selected decoder plus controls. Training included 3,691 correct and 405 incorrect authorization runs.

| Setting | Actual value |
|---|---|
| Identity labels / decision readout | File catalog position / A permitted, B forbidden |
| Selected residual block / weight decay | 20 / 0.1 |
| Training | AdamW; learning rate 0.01; 80 epochs; probe batches 256 |
| Candidate search | 28 blocks × four weight decays |
| Compute | One H100 80GB; 270.9 s; seed 42; inference batches 8 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Requested file, full test | 1,175/1,200 | 97.92 | 96.94–98.58 |
| Requested file, initial errors; supplementary | 123/125 | 98.40 | 94.35–99.56 |
| Shuffled-label decoder, full test | 258/1,200 | 21.50 | 19.27–23.91 |
| Disclosed-label control, validation | 118/128 | 92.19 | Not reported in the control record |

The selected block passed the extraction comparison; stricter batched/single-example tolerances failed at later, unselected blocks. [experiment_sc1]

### A.2 Smaller overall-recipient decoder

**Target:** at least 1,080 recipient predictions correct out of 1,200. **Model:** common Qwen checkpoint. **Data:** FourFilePermissionBinding-v1; 8,192 training, 2,048 selection, eight pilots of 256; permission pools of 160/32/64 assignments for training/selection/test, with every file–recipient cell represented. Test allocation balanced file, true-recipient and authorization labels.

**Procedure:** (1) Select the most error-producing format-compliant pilot. (2) Fit all linear candidates on original states from 4,874 correct and 3,318 incorrect training runs. (3) Freeze the validation-selected decoder and controls before generating and evaluating test problems.

| Setting | Actual value |
|---|---|
| Presentation | Shared-stem names; request before table; recipient column first |
| Labels / authorization | Recipient catalog slots R1–R4 / Y versus N logits |
| Selected block / L2 penalty | 20 / 0.01 |
| Search / optimizer | Seven blocks × five penalties; float32 full-batch L-BFGS |
| Compute | One H100; 273.2 s; seed 42; inference batches 16 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Recipient, full test | 849/1,200 | 70.75 | 68.11–73.25 |
| Recipient, initial errors; supplementary | 384/476 | 80.67 | 76.89–83.97 |
| Shuffled-label decoder | 320/1,200 | 26.67 | 24.24–29.24 |
| Request/decision frequency comparator | 600/1,200 | 50.00 | 47.18–52.82 |

The assignment-cluster bootstrap interval for overall decoding was 67.85–73.51%. The selected fit's maximum gradient was 9.638e-5 against a 1e-5 diagnostic tolerance; this limits claims of optimal fitting but does not erase the measured shortfall. [experiment_sc2]

### A.3 Recipient decoder on initial errors

**Target:** at least 90% among all initial errors, requiring 261/290 successes in this test. **Model:** common Qwen checkpoint. **Data:** synthetic_file_transfer_4x4_v1; 2,048 calibration, 4,096 fitting and 1,024 validation problems. Cyclic-relabeling orbits reserved 64 permission vectors for test and 192 for development; names were globally fresh.

**Procedure:** (1) Select a calibration presentation using authorization errors, not probe performance. (2) Fit 35 standardized multinomial logistic regressions on 3,260 correct and 836 incorrect runs. (3) Select by validation-error accuracy, freeze, and score every original test error without confidence filtering.

| Setting | Actual value |
|---|---|
| Presentation | Confusable 24-character stems; request after table; four nonauthoritative history records after table |
| Labels / authorization | Recipient directory position / Yes versus No logits |
| Selected block / inverse regularization C | 20 / 0.01 |
| Search / fitting | Blocks 4, 8, 12, 16, 20, 24, 28; five C values; converged L-BFGS fit |
| Compute / seeds | One H100 80GB; 3,187 s; optimizer 42, split 53, test 442; batches 8 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Recipient, all initial errors | 197/290 | 67.93 | 62.35–73.04 |
| Recipient, full test | 851/1,200 | 70.92 | 68.28–73.42 |
| Shuffled decoder, initial errors | 75/290 | 25.86 | 21.16–31.19 |
| Copy requested recipient, initial errors | 226/290 | 77.93 | 72.81–82.32 |

Selected-fit convergence and above-shuffled validation performance support a genuine learned readout. [experiment_sc4]

### A.4 Eleven-head repair and preservation

**Target:** repair at least 30% of all original errors and change at most 3% of original correct decisions. **Model:** common Qwen checkpoint. **Data:** FT4x4-RowRepair-v1; 256 pilot problems evaluated under four presentations, 1,024 discovery, 512 validation and 1,200 test problems; seeded 128/128 development/test assignment pools.

**Procedure:** (1) Select the pilot presentation using donor coverage and authorization outcomes. (2) Enumerate all 23 nonidentity row permutations and choose the first correct donor lexicographically. (3) Rank heads by gradient-times-donor-difference, exact-test sparse candidates and select on independent validation. (4) Freeze heads, alignment and donor rules; evaluate originals, selected patches and controls. Missing or capture-invalid donors leave the target unchanged without removing it from either denominator.

| Setting | Actual value |
|---|---|
| Presentation / readout | Ordinary identifiers; File–Permitted recipient table / A versus B |
| Patch operation | Query-head outputs before output projection; exact token-ID alignment of prefix, row interiors by file identity, and suffix |
| Fixed heads, zero-based (layer, head) | (12,24), (15,3), (17,22), (18,4), (18,13), (18,15), (18,18), (18,21), (19,23), (19,24), (20,3) |
| Discovery / validation candidates | 237 exact discovery evaluations; 24 validation candidates |
| Numerical execution | BF16 backbone; FP32 binary unembedding accumulation; fixed execution shape |
| Compute / seeds | One H100 80GB; 2,321 s; global 42, partition 421, test 425; batches 16, gradient batches 2 |

| Condition | Errors repaired / all errors | Repair (%) [95% interval] | Correct decisions changed / all correct | Change (%) [95% interval] |
|---|---:|---:|---:|---:|
| Fixed 11 heads | 112/123 | 91.06 [84.69–94.93] | 2/1,077 | 0.1857 [0.05094–0.6746] |
| Random 11 heads | 5/123 | 4.065 [not reported] | 21/1,077 | 1.950 [not reported] |
| Self-patch control | 0/123 | 0 [not reported] | 0/1,077 | 0 [not reported] |

Qualifying captured donors covered 121/123 errors and all 1,077 correct decisions; all-head reconstruction and unselected-slice checks passed. Bonferroni-adjusted intervals jointly supported both intervention bounds. [experiment_sc5]

### A.5 Nine-head final-token repair and preservation

**Target:** the same coupled repair/preservation bounds. **Model:** common Qwen checkpoint. **Data:** SyntheticFileTransfer4x4-v1; eight pilots of 128, 384 discovery, 384 search and 768 validation problems. Assignment pools were 32/64/64/32/64 for pilot/discovery/search/validation/test; fresh identifiers and uniform within-pool assignment sampling preceded model scoring.

**Procedure:** (1) Select the least-severe eligible identifier configuration. (2) Rank all heads using donor-difference attribution; greedily build sets in final-token and suffix scopes. (3) Evaluate 24 candidates on validation and freeze the selected set. (4) For every test case, rank correct reordered donors by signed authorization margin, revalidate at capture, and patch; unavailable donors remain unchanged in the denominators.

| Setting | Actual value |
|---|---|
| Presentation / readout | Common-stem identifiers of length 16 differing at final character; request after table / A versus B |
| Donor budget / ordering | All 23 nonidentity permutations; largest correct signed margin, lexicographic ties |
| Patch operation | Selected query-head outputs before output projection at final prompt token only |
| Fixed heads, zero-based (layer, head) | (18,4), (18,13), (18,15), (18,18), (19,23), (19,24), (20,1), (20,3), (26,26) |
| Compute | One H100 80GB; 926.7 s; seed 42; inference batches 16, gradient batches 2 |

| Condition | Errors repaired / all errors | Repair (%) [95% Wilson interval] | Correct decisions changed / all correct | Change (%) [95% Wilson interval] |
|---|---:|---:|---:|---:|
| Fixed nine heads | 213/229 | 93.01 [88.95–95.65] | 0/971 | 0 [0–0.3941] |
| Random nine heads | 2/229 | 0.8734 [0.2398–3.128] | 0/971 | 0 [0–0.3941] |

Usable donors covered 219/229 errors and 970/971 correct cases. Self-patching reproduced sampled decisions exactly; the custom/ordinary forward comparison agreed on decisions but missed its strict logit tolerance, with maximum difference 0.125. [experiment_sc6]

### A.6 Higher-data recipient decoder

**Target:** at least 1,080 recipient predictions correct out of 1,200; error-conditioned results were supplementary. **Model:** common Qwen checkpoint. **Data:** FourFilePermissionBinding-v1/higher-data-independent-v2; 65,536 training and 8,192 selection problems; independent 160/32/64 permission-vector pools and fresh names. Test cells and forbidden alternatives were exactly balanced.

**Procedure:** (1) Use the fixed shared-stem presentation with independently randomized suffix-to-slot assignments. (2) Extract all 28 blocks and fit 196 linear candidates using every training run, including 47,705 correct and 17,831 incorrect authorization decisions. (3) Select a converged candidate by overall selection accuracy, run development-only nested-subset diagnostics, and freeze. (4) Generate the untouched test, replay novelty checks and score the selected decoder and shuffled control.

| Setting | Actual value |
|---|---|
| Presentation / labels | Request before recipient-first table; recipient catalog A–D |
| Selected block / L2 penalty | 20 / 0.0001 |
| Fitting | Float64 full-batch L-BFGS; seven penalties across 28 blocks; training-only affine standardization |
| Compute | One H100 80GB; 6,246 s; inference batches 32 |
| Seeds | Partition 20261011; training 20261012; selection 20261013; probe 20261014; test 20261015 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Recipient, full test | 1,141/1,200 | 95.08 | 93.71–96.17 |
| Recipient, initial errors; supplementary | 300/309 | 97.09 | 94.56–98.46 |
| Shuffled-label decoder | 296/1,200 | 24.67 | 22.31–27.18 |
| Selection, training subset 8,192; diagnostic | 7,350/8,192 | 89.72 | 89.05–90.36 |
| Selection, training subset 32,768; diagnostic | 7,644/8,192 | 93.31 | 92.75–93.83 |
| Selection, full training 65,536 | 7,793/8,192 | 95.13 | 94.64–95.57 |

The full-test assignment-cluster bootstrap interval was 93.86–96.27%. The nested learning-curve rows used the same selected block and penalty and did not alter the frozen decoder. [experiment_sc102] [compute_2]

### Attempts without an accepted measurement

| What it tested | Why it supplies no usable measurement | Record |
|---|---|---|
| Requested-file decoding among authorization errors | The result judgment classifies the record as unrun and unsound; its reported outcome is excluded from the assessment. | [experiment_sc3] [script_sc3] [log_sc3] |

## Appendix B: Artifact Bundle

| Experiment | Code | Results and saved-output pointers | Compute-cost record |
|---|---|---|---|
| Requested-file decoding | [script_sc1] | [experiment_sc1]; decoder, freeze manifest and per-problem predictions | 270.9 s on one H100; [log_sc1] |
| Smaller overall-recipient decoding | [script_sc2] | [experiment_sc2]; frozen decoder, assignment pools and predictions | 273.2 s on one H100; [log_sc2] |
| Recipient decoding on errors | [script_sc4] | [experiment_sc4]; frozen probe/protocol, manifests and predictions | 3,187 s on one H100; [log_sc4] |
| Eleven-head repair | [script_sc5] | [experiment_sc5]; frozen intervention and per-case original/patched decisions | 2,321 s on one H100; [log_sc5] |
| Nine-head preservation and repair | [script_sc6] | [experiment_sc6]; frozen intervention, donor records and held-out measurements | 926.7 s on one H100; [log_sc6] |
| Higher-data recipient decoding | [script_sc102] | [experiment_sc102]; frozen decoder, independent manifests, predictions and learning curves | 6,246 s on one H100; [log_sc102] |

## Appendix C: Claim Card

| Element | Locked interpretation |
|---|---|
| System under test | Qwen2.5-7B-Instruct performing four-file/four-recipient permission-based authorization; original-state linear readouts and inference-time head-output patching |
| Claimed property | Both identities remain linearly decodable, including during authorization errors; a sparse fixed donor patch selectively repairs decisions |
| Conditions | 1,200 held-out problems, 600 permitted and 600 forbidden; unseen test names and permission assignments; decoders trained on correct and incorrect development runs; decoders, heads and donor rules fixed before testing |
| Quantifier | Existential: one admissible configuration suffices, but all criteria must hold together |
| Success threshold | At least 90% requested-file and permitted-recipient accuracy overall and separately among all initial errors; at least 30% of all initial errors repaired; at most 3% of all initially correct decisions changed; at most 12 fixed attention heads |
| Comparator | Ground-truth identities for decoding; the same model's original authorization decisions on the same problems for patching |
| Donors and intervention | Correct donor decisions; identical permission facts with reordered table rows; identical intervention for error and correct-case evaluation; unavailable donors never removed from denominators |
| Assumptions locked before analysis | Unambiguous ground truth; prespecified identity-label mapping for unseen names; consistent decision extraction; nonempty original-error and original-correct subsets; accessible and alignable activations; comparable controlled inference; enforceable split novelty and freezing; prespecified correctness verification and missing-donor handling |
| Open design choices | Prompt and identifier distribution, development size, residual layer, affine preprocessing and fitting, specific heads and patch positions, alignment, donor search/ranking, response format and numerical execution |