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

Successful linear recovery of the permitted recipient on authorization errors makes **+1 Likely feasible**, score **+1**, confidence **0.78**, the best estimate. Attention-head repair has working instances with substantial margins, so the deciding work is adapting the demonstrated permission decoding and intervention to one common, development-fixed presentation. [experiment_sc102] [experiment_sc6]

## 1. Introduction

> On 1,200 held-out file-transfer problems balanced between permitted and forbidden requests, with four files and four recipients, linear decoders of Qwen2.5-7B-Instruct's final prompt-token residual state identify the requested file and its permitted recipient with at least 90% accuracy each, even among incorrect authorization decisions. Patching a fixed set of at most 12 attention heads from correct runs containing the same permission facts in reordered table rows corrects at least 30% of all initial errors while changing no more than 3% of correct decisions. Decoders, heads, and donor-selection rules are fixed on separate development data, with decoders trained on both correct and incorrect development runs; test names and permission assignments are unseen.

I read this as an existential claim that one development-fixed configuration of the named model meets all six accuracy and intervention-rate criteria on the same held-out set, with identity labels defined consistently for unseen names and correct donors verified by a prespecified procedure.

1. Requested-file identity must be decoded at least 90% accurately overall and separately among all initial authorization errors.
2. Permitted-recipient identity must meet those same two accuracy bounds.
3. One fixed set of at most 12 heads must repair at least 30% of all initial errors while changing at most 3% of initially correct decisions.

All three performance parts are needed under the stated held-out, development-fixed setup; recipient decoding on initial errors is the decisive part. The claim matters because it distinguishes inaccessible permission information from information the model represents but fails to use, enabling targeted adherence interventions.

## 2. What the literature establishes

The closest work concerns **binding**, the internal association between an entity and its attribute—in this case, a file and its permitted recipient.

| Prior work | Published result beside the claim's threshold | Relevance and boundary |
|---|---|---|
| *Legible failures* | Qwen2.5-7B **Base**: failure-conditioned linear binding accuracy 27.6%, seed range 23.6–34.5%, versus the claim's 90%. In a separate residual-state intervention: 29% repair and 79% preservation, versus required 30% repair and at least 97% preservation. | Direct evidence that prompt-supplied bindings can survive wrong answers, but neither the model variant nor adding a learned direction to the residual state matches the claimed head replacement. [web_legible_failures_error_decoding_and_steering](https://arxiv.org/abs/2609.11216) |
| *How do Language Models Bind Entities in Context?* | On two-binding tests, control accuracy exceeds 99%; separate entity or attribute interventions reduce original-association accuracy below 3%; simultaneous interventions restore it above 97%. | Establishes manipulable binding representations in LLaMA/Pythia. Restoration reverses an artificial intervention, not natural authorization errors, and does not establish repair using a small set of attention heads. [web_binding_id_representations](https://arxiv.org/abs/2310.17191) |
| *Mixing Mechanisms* | A model combining retrieval by group position, entity identity, and a stored pointer to the target entity achieves 0.95 Jensen–Shannon similarity, a measure of agreement between probability distributions. Experiments include Qwen2.5-7B-Instruct. | Supports causal accessibility at the final token, but distribution similarity is not identity-decoding accuracy. Different retrieval signals make fact-equivalent row orders potentially different activation donors. [web_mixing_mechanisms_qwen_binding](https://arxiv.org/abs/2510.06182) |

**The strongest published case for the claim** is the instruction-tuned OLMo result in Appendix D, Table 5 of *Legible failures*: 38% repair with 97% preservation meets the claimed intervention-rate trade-off, by adding learned directions to residual states rather than replacing donor heads. **The strongest published case against it** is that paper's Qwen Base decoding and intervention result in the table above. These cases establish an actionable mechanism with substantial model dependence; the positive forecast survives the negative case because task-matched Instruct measurements are appreciably closer than the Base-model analogue. [web_1](https://arxiv.org/abs/2609.11216) [web_legible_failures_error_decoding_and_steering](https://arxiv.org/abs/2609.11216)

## 3. What the literature leaves open

The literature does not settle identity decoding with unseen names and permission assignments on this authorization task. Frozen linear-decoder experiments tested requested-file decoding, overall recipient decoding, and recipient decoding among initial errors; a higher-data experiment tested a stronger decoder on a new held-out set.

Residual-state interventions also do not settle the fixed-head donor intervention. Two experiments tested active head-output replacement from correct row-reordered donors, scoring repair and preservation together; decoders and interventions were evaluated separately.

## 4. What our experiments show

Block numbers below count successive transformer layers; shared-stem names share a common prefix with distinct suffixes. Reported 95% Wilson intervals are binomial-proportion confidence intervals for observed success rates; they supplement, rather than replace, the claim's finite-set point thresholds.

**Requested-file decoding.** A decoder reading the residual state after block 20 achieved 1,175/1,200, or 97.92% accuracy (96.94–98.58%), against 90%. Its supplementary initial-error result was 123/125, or 98.40% (94.35–99.56%), supporting both file-decoding bounds in this distribution. [experiment_sc1]

**Smaller overall-recipient decoder.** A shared-stem, reversed-column presentation with 8,192 training problems achieved 849/1,200, or 70.75% (68.11–73.25%), against 90%. [experiment_sc2]

**Recipient decoding on initial errors.** A converged decoder on a confusable-name presentation with routing history achieved 197/290, or 67.93% (62.35–73.04%), among all initial errors, against 90%. [experiment_sc4]

**Eleven-head patching.** Replacing outputs at corresponding tokens repaired 112/123 errors, or 91.06% (84.69–94.93%), against 30%, while changing 2/1,077 correct decisions, or 0.1857% (0.05094–0.6746%), against 3%. Every original error remained in the denominator, including two without qualifying donors. [experiment_sc5]

**Nine-head final-token patching.** A second development-fixed intervention repaired 213/229 errors, or 93.01% (88.95–95.65%), and changed 0/971 correct decisions, or 0% (upper interval bound 0.3941%). Nonzero activation replacements establish that preservation was measured with an active intervention. [experiment_sc6]

**Higher-data recipient decoder.** With 65.54 thousand training problems, independent shared-stem names and catalog-slot labels, meaning positions in the displayed recipient list, the frozen decoder achieved 1,141/1,200, or 95.08% (93.71–96.17%); its supplementary initial-error result was 300/309, or 97.09% (94.56–98.46%), clearing both recipient bounds. Presentation and fitting also changed from the smaller experiment, so the difference between their test results cannot be attributed solely to dataset size. [experiment_sc102]

See Appendix A for experimental details and for runs that produced no measurement.

## 4b. In the News (non-academic sources)

The news and podcast channel found no relevant items.

## 5. Why the claim succeeds or fails

**The claim can work by separating a stored permission association from the computation that produces an authorization decision.** Binding interventions establish that associations are causally manipulable, while Qwen's mixed retrieval mechanisms explain why equivalent permission facts can produce different internal states. Development-selected layers, matching donor and target token positions by file identity, and correct reordered donors can exploit that distinction; the claim does not require success across every prompt format. [web_binding_id_representations](https://arxiv.org/abs/2310.17191) [web_mixing_mechanisms_qwen_binding](https://arxiv.org/abs/2510.06182)

**The intervention controls distinguish useful head selection from arbitrary activation changes.** A matched random nine-head control repaired only 0.8734% of initial errors, despite using the same donor policy and head count as the selected intervention. Reinserting each sampled run's own captured head outputs reproduced its decision exactly, supporting a causal, component-specific effect. This is important evidence beyond the closest published Qwen residual-state intervention, where moving toward decoded bindings damages many initially correct answers. [experiment_sc6] [web_2](https://arxiv.org/abs/2609.11216)

**The number that still needs dependable generalization is error-conditioned recipient accuracy.** The high-data decoder's 92.00% accuracy on forbidden test requests shows retrieval of the table-assigned recipient rather than the requested destination; a routing-history presentation falls short of this, so presentation choice remains load-bearing. [experiment_sc102] [experiment_sc4]

## 6. Assessment

**The assessment is +1 Likely feasible, score +1, confidence 0.78: a relevant lab is likely to achieve all six criteria in one frozen configuration within the assessment's three-month horizon.** Confidence is below certainty because the reported intervals measure test-sample variation, not variation across independent development selections of decoders and heads. [experiment_sc102] [experiment_sc6]

**An independently frozen configuration meeting all six criteria would justify +2 Feasible.** Repeated well-functioning tests in which the recipient decoder loses error-conditioned accuracy, or the head patch misses the repair/preservation trade-off under the same presentation, would weaken the forecast and move the score down. [experiment_sc102] [experiment_sc6]

### Why not the neighbouring scores

**+2 Feasible would treat the known dependence on query and table positions as a minor detail when combining the demonstrated components; 0 Evenly balanced would underweight the named-model decoder's untouched-test success.** The combination must accommodate the position-dependent retrieval routes described in *Mixing Mechanisms*, rather than assuming interchangeable activation representations across the decoder and intervention presentations. [web_mixing_mechanisms_qwen_binding](https://arxiv.org/abs/2510.06182) [experiment_sc102]

## 7. Limitations and further directions

Donor checking uses task ground truth, which is allowed here but does not demonstrate an autonomous deployment method; the task also does not test persistent adherence in long workflows. [experiment_sc5]

**Further directions**

- Train both identity decoders on a patch-compatible development distribution, freeze every choice, and evaluate all six criteria on the same 1,200 held-out problems. A shortfall would identify which property limits the complete system.
- Compare decoder-training sizes under an unchanged prompt, label mapping and permission split, scoring each frozen decoder on untouched test problems. This would isolate sample-size effects and test a specific remedy for difficult recipient retrieval.
- Repeat the complete configuration with independent development/test draws and fixed donor budgets. Stability would strengthen confidence; unstable conditional decoding or preservation would lower it.

## Appendix A: Experimental Details

All measured experiments used the public Hugging Face **Qwen/Qwen2.5-7B-Instruct** model: 7.616 billion parameters, frozen BF16 weights (bfloat16 floating-point precision), the model's standard conversation formatting, and SDPA attention (scaled dot-product attention). There was no additional low-bit weight compression or generated reasoning. Every test contained four files, four recipients and exactly 600 permitted plus 600 forbidden requests; test names and permission assignments expressed in catalog order were disjoint from development. Decoder inputs were one original, unnormalized post-block residual vector at the final actual prompt token; training-only coordinate standardization and linear classifiers with constant output offsets preserved linear decoding. Model weights were never updated. [experiment_sc1] [experiment_sc102]

Wilson intervals are 95% unless stated; cluster bootstraps resample whole permission-assignment groups. Uncertainty not supplied for a control is marked “not reported.” Linked records retain exact sample counts, checkpoint provenance and seed settings.

### A.1 Requested-file decoder

**Target:** at least 90% requested-file accuracy overall and on initial errors; lower measured accuracy would fail the relevant bound. **Model:** common Qwen model above. **Data:** locally generated four-file transfer problems; 4,096 fitting, 1,024 validation, four pilots of 256, and a separate 512/128 disclosed-label control. Groups formed by cyclically relabeling all recipients divided permission vectors into 128 development and 128 test assignments.

**Procedure:** (1) Select the first prespecified pilot with a nontrivial error signal; independent opaque names were chosen. (2) Extract all block states and fit every candidate combination of layer and coefficient shrinkage using both correctness groups. (3) Select on validation, freeze, generate the test set and score one selected decoder plus controls. Training included 3,691 correct and 405 incorrect authorization runs.

| Setting | Actual value |
|---|---|
| Identity labels / decision scoring | File catalog position / A permitted, B forbidden |
| Selected residual block / weight decay, coefficient shrinkage during fitting | 20 / 0.1 |
| Training | AdamW, Adam gradient optimization with decoupled weight decay; learning rate, the update step size, 0.01; 80 epochs, passes over fitting data; classifier batches 256 |
| Candidate search | 28 blocks × four weight-decay strengths |
| Compute | One H100 80GB; 270.9 s; seed 42; inference batches 8 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Requested file, full test | 1,175/1,200 | 97.92 | 96.94–98.58 |
| Requested file, initial errors; supplementary | 123/125 | 98.40 | 94.35–99.56 |
| Shuffled-label decoder, full test | 258/1,200 | 21.50 | 19.27–23.91 |
| Disclosed-label control, validation | 118/128 | 92.19 | Not reported in the control record |

The selected block passed the extraction comparison; stricter batched/single-example tolerances failed at later, unselected blocks. [experiment_sc1]

### A.2 Smaller overall-recipient decoder

**Target:** at least 1,080 recipient predictions correct out of 1,200. **Model:** common Qwen model. **Data:** generated four-file/four-recipient permission problems; 8,192 training, 2,048 selection, eight pilots of 256; permission pools of 160/32/64 assignments for training/selection/test, with every file–recipient cell represented. Test allocation balanced file, true-recipient and authorization labels.

**Procedure:** (1) Select the most error-producing format-compliant pilot. (2) Fit all linear candidates on original states from 4,874 correct and 3,318 incorrect training runs. (3) Freeze the validation-selected decoder and controls before generating and evaluating test problems.

| Setting | Actual value |
|---|---|
| Presentation | Shared-stem names; request before table; recipient column first |
| Labels / authorization | Recipient catalog slots R1–R4 / Y versus N next-token scores |
| Selected block / L2 penalty, regularization discouraging large coefficients by penalizing their squared size | 20 / 0.01 |
| Search / optimizer | Seven blocks × five penalties; float32, single-precision full-batch fitting; L-BFGS, limited-memory quasi-Newton optimization |
| Compute | One H100; 273.2 s; seed 42; inference batches 16 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Recipient, full test | 849/1,200 | 70.75 | 68.11–73.25 |
| Recipient, initial errors; supplementary | 384/476 | 80.67 | 76.89–83.97 |
| Shuffled-label decoder | 320/1,200 | 26.67 | 24.24–29.24 |
| Request/decision frequency comparator | 600/1,200 | 50.00 | 47.18–52.82 |

The assignment-cluster bootstrap interval for overall decoding was 67.85–73.51%. The selected fit's maximum gradient was 9.638e-5 against a 1e-5 diagnostic tolerance; this limits claims of optimal fitting but does not erase the measured shortfall. [experiment_sc2]

### A.3 Recipient decoder on initial errors

**Target:** at least 90% among all initial errors, requiring 261/290 successes in this test. **Model:** common Qwen model. **Data:** synthetic permission problems with confusable identifiers and routing history; 2,048 calibration, 4,096 fitting and 1,024 validation problems. Cyclic-relabeling groups reserved 64 permission vectors for test and 192 for development; names were globally fresh.

**Procedure:** (1) Select a calibration presentation using authorization errors, not decoder performance. (2) Fit 35 standardized four-class logistic regressions—linear score models fitted to predict class probabilities—on 3,260 correct and 836 incorrect runs. (3) Select by validation-error accuracy, freeze, and score every original test error without confidence filtering.

| Setting | Actual value |
|---|---|
| Presentation | Confusable 24-character stems; request after table; four nonauthoritative history records after table |
| Labels / authorization | Recipient directory position / Yes versus No next-token scores |
| Selected block / inverse regularization C | 20 / 0.01 |
| Search / fitting | Blocks 4, 8, 12, 16, 20, 24, 28; five C values; converged L-BFGS fit |
| Compute / seeds | One H100 80GB; 3,187 s; optimizer 42, split 53, test 442; batches 8 |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Recipient, all initial errors | 197/290 | 67.93 | 62.35–73.04 |
| Recipient, full test | 851/1,200 | 70.92 | 68.28–73.42 |
| Recipient, forbidden-request errors; diagnostic | 25/64 | 39.06 | 28.06–51.31 |
| Recipient, permitted-request errors; diagnostic | 172/226 | 76.11 | 70.14–81.20 |
| Shuffled decoder, initial errors | 75/290 | 25.86 | 21.16–31.19 |
| Copy requested recipient, initial errors | 226/290 | 77.93 | 72.81–82.32 |

Selected-fit convergence and above-shuffled validation performance support a genuine learned decoder. [experiment_sc4]

### A.4 Eleven-head repair and preservation

**Target:** repair at least 30% of all original errors and change at most 3% of original correct decisions. **Model:** common Qwen model. **Data:** generated row-reordered permission problems; 256 pilot problems evaluated under four presentations, 1,024 discovery, 512 validation and 1,200 test problems; seeded 128/128 development/test assignment pools.

**Procedure:** (1) Select the pilot presentation using donor coverage and authorization outcomes. (2) Enumerate all 23 nonidentity row permutations and choose the first correct donor in their fixed sorted order. (3) Rank heads by estimating the effect of donor-minus-original outputs on the decision score, exact-test candidate head sets and select on independent validation. (4) Freeze heads, token correspondence and donor rules; evaluate originals, selected patches and controls, including reinserting the target's own activations, called self-patching. Missing or capture-invalid donors leave the target unchanged without removing it from either denominator.

| Setting | Actual value |
|---|---|
| Presentation / decision scoring | Ordinary identifiers; File–Permitted recipient table / A versus B |
| Patch operation | Individual attention-head outputs before the final attention linear map; match identical tokens in prefix, row interiors by file identity, and suffix |
| Fixed heads, zero-based (layer, head) | (12,24), (15,3), (17,22), (18,4), (18,13), (18,15), (18,18), (18,21), (19,23), (19,24), (20,3) |
| Discovery / validation candidates | 237 exact discovery evaluations; 24 validation candidates |
| Numerical execution | BF16 backbone; float32 computation using the ordinary output-head weights; fixed execution shape |
| Compute / seeds | One H100 80GB; 2,321 s; global 42, partition 421, test 425; batches 16, gradient batches 2 |

| Condition | Errors repaired / all errors | Repair (%) [95% interval] | Correct decisions changed / all correct | Change (%) [95% interval] |
|---|---:|---:|---:|---:|
| Fixed 11 heads | 112/123 | 91.06 [84.69–94.93] | 2/1,077 | 0.1857 [0.05094–0.6746] |
| Random 11 heads | 5/123 | 4.065 [not reported] | 21/1,077 | 1.950 [not reported] |
| Self-patch control | 0/123 | 0 [not reported] | 0/1,077 | 0 [not reported] |

Qualifying captured donors covered 121/123 errors and all 1,077 correct decisions; all-head reconstruction and unselected-activation checks passed. Bonferroni-adjusted intervals, controlling joint uncertainty for the two proportions, supported both intervention bounds. [experiment_sc5]

### A.5 Nine-head final-token repair and preservation

**Target:** the same coupled repair/preservation bounds. **Model:** common Qwen model. **Data:** synthetic permission problems with common-stem identifiers; eight pilots of 128, 384 discovery, 384 search and 768 validation problems. Assignment pools were 32/64/64/32/64 for pilot/discovery/search/validation/test; fresh identifiers and uniform within-pool assignment sampling preceded model scoring.

**Procedure:** (1) Select the least-severe eligible identifier configuration. (2) Rank all heads by estimated changes from donor outputs; greedily build sets at final-token and suffix positions. (3) Evaluate 24 candidates on validation and freeze the selected set. (4) For every test case, rank correct reordered donors by the difference between correct and incorrect authorization scores, revalidate at capture, and patch; unavailable donors remain unchanged in the denominators.

| Setting | Actual value |
|---|---|
| Presentation / decision scoring | Common-stem identifiers of length 16 differing at final character; request after table / A versus B |
| Donor budget / ordering | All 23 nonidentity permutations; largest correct signed score difference, fixed sorted permutation order for ties |
| Patch operation | Selected individual attention-head outputs before the final attention linear map at the final prompt token only |
| Fixed heads, zero-based (layer, head) | (18,4), (18,13), (18,15), (18,18), (19,23), (19,24), (20,1), (20,3), (26,26) |
| Compute | One H100 80GB; 926.7 s; seed 42; inference batches 16, gradient batches 2 |

| Condition | Errors repaired / all errors | Repair (%) [95% Wilson interval] | Correct decisions changed / all correct | Change (%) [95% Wilson interval] |
|---|---:|---:|---:|---:|
| Fixed nine heads | 213/229 | 93.01 [88.95–95.65] | 0/971 | 0 [0–0.3941] |
| Random nine heads | 2/229 | 0.8734 [0.2398–3.128] | 0/971 | 0 [0–0.3941] |

Usable donors covered 219/229 errors and 970/971 correct cases. Self-patching reproduced sampled decisions exactly; the custom/ordinary forward comparison agreed on decisions but missed its strict score tolerance, with maximum difference 0.125. [experiment_sc6]

### A.6 Higher-data recipient decoder

**Target:** at least 1,080 recipient predictions correct out of 1,200; error-conditioned results were supplementary. **Model:** common Qwen model. **Data:** independently generated shared-stem permission problems; 65.54 thousand training and 8,192 selection problems; independent 160/32/64 permission-vector pools and fresh names. Test cells and forbidden alternatives were exactly balanced.

**Procedure:** (1) Use the fixed shared-stem presentation with independently randomized suffix-to-slot assignments. (2) Extract all 28 blocks and fit 196 linear candidates using every training run, including 47.71 thousand correct and 17.83 thousand incorrect authorization decisions. (3) Select a converged candidate by overall selection accuracy and freeze. (4) Generate the untouched test, replay novelty checks and score the selected decoder and shuffled control.

| Setting | Actual value |
|---|---|
| Presentation / labels | Request before recipient-first table; recipient catalog A–D |
| Selected block / L2 penalty | 20 / 0.0001 |
| Fitting | Float64, double-precision full-batch L-BFGS; seven penalties across 28 blocks; training-only linear standardization |
| Compute | One H100 80GB; 6,246 s; inference batches 32 |
| Seeds | Independent streams for partition, training, selection, fitting and test; exact seed bundle in [script_sc102] |

| Condition | Correct / evaluated | Accuracy (%) | 95% Wilson interval (%) |
|---|---:|---:|---:|
| Recipient, full test | 1,141/1,200 | 95.08 | 93.71–96.17 |
| Recipient, initial errors; supplementary | 300/309 | 97.09 | 94.56–98.46 |
| Recipient, forbidden requests; diagnostic | 552/600 | 92.00 | 89.55–93.91 |
| Shuffled-label decoder | 296/1,200 | 24.67 | 22.31–27.18 |

The full-test assignment-cluster bootstrap interval was 93.86–96.27%. Development-only subset fits did not establish untouched-test accuracy. [experiment_sc102]

### Attempts without an accepted measurement

| What it tested | Why it supplies no usable measurement | Record |
|---|---|---|
| Requested-file decoding among authorization errors | The result judgment classifies the record as unrun and unsound; its reported outcome is excluded from the assessment. | [experiment_sc3] [script_sc3] [log_sc3] |

## Appendix B: Artifact Bundle

| Experiment | Code | Results and saved-output pointers | Compute-cost record |
|---|---|---|---|
| Requested-file decoding | [script_sc1] | [experiment_sc1]; decoder, frozen settings and per-problem predictions | 270.9 s on one H100; [log_sc1] |
| Smaller overall-recipient decoding | [script_sc2] | [experiment_sc2]; frozen decoder, assignment pools and predictions | 273.2 s on one H100; [log_sc2] |
| Recipient decoding on errors | [script_sc4] | [experiment_sc4]; frozen decoder and settings, split records and predictions | 3,187 s on one H100; [log_sc4] |
| Eleven-head repair | [script_sc5] | [experiment_sc5]; frozen intervention and per-case original/patched decisions | 2,321 s on one H100; [log_sc5] |
| Nine-head preservation and repair | [script_sc6] | [experiment_sc6]; frozen intervention, donor records and held-out measurements | 926.7 s on one H100; [log_sc6] |
| Higher-data recipient decoding | [script_sc102] | [experiment_sc102]; frozen decoder, independent split records and predictions | 6,246 s on one H100; [log_sc102] |

## Appendix C: Claim Card

| Element | Locked interpretation |
|---|---|
| System under test | Qwen2.5-7B-Instruct performing four-file/four-recipient permission-based authorization; original-state linear decoders and inference-time head-output patching |
| Claimed property | Both identities remain linearly decodable, including during authorization errors; a fixed limited-head donor patch selectively repairs decisions |
| Conditions | 1,200 held-out problems, 600 permitted and 600 forbidden; unseen test names and permission assignments; decoders trained on correct and incorrect development runs; decoders, heads and donor rules fixed before testing |
| Quantifier | Existential: one admissible configuration suffices, but all criteria must hold together |
| Success threshold | At least 90% requested-file and permitted-recipient accuracy overall and separately among all initial errors; at least 30% of all initial errors repaired; at most 3% of all initially correct decisions changed; at most 12 fixed attention heads |
| Comparator | Ground-truth identities for decoding; the same model's original authorization decisions on the same problems for patching |
| Donors and intervention | Correct donor decisions; identical permission facts with reordered table rows; identical intervention for error and correct-case evaluation; unavailable donors never removed from denominators |
| Assumptions locked before analysis | Unambiguous ground truth; prespecified identity-label mapping for unseen names; consistent decision extraction; nonempty original-error and original-correct subsets; accessible and alignable activations; comparable controlled inference; enforceable split novelty and freezing; prespecified correctness verification and missing-donor handling |
| Open design choices | Prompt and identifier distribution, development size, residual layer, linear preprocessing and fitting, specific heads and patch positions, token correspondence, donor search/ranking, response format and numerical execution |