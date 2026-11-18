I'd focus on **515, 509 and 508**, then 507, 519 and 475. These are the claims where experiments really shaped the verdict, literature carried real weight, the run took 5+ hours, and there's a concrete reason to doubt the call.

Runtime here is the active time across a claim's runs. Several runs have long gaps after a result was flagged "implausible", which look like stalls, so I didn't count those toward the 5 hours. The "reasons to doubt" come from the reports' own numbers, from verdicts that changed between the original and final runs, and from the limits each report admits.

### Top picks

| ID | Claim | Verdict (r1 → final) | Active time | Why it fits | Reason to doubt the prediction |
|---|---|---|---|---|---|
| **515** | Decode file and recipient from Qwen2.5-7B, and repair errors by patching ≤12 attention heads | +1 → +1 (0.78) | 9.2h, 7 GPU jobs | The most complex claim (6 criteria must hold together). 6 experiments plus a strong literature table. | Recipient decoding **failed twice** (70.8%, 67.9%) and passed (95%) only after the prompt layout, labels and training size all changed. The six criteria were **never tested together in one frozen configuration**, which is what the claim requires. The +1 is an extrapolation. |
| **509** | Leave-partition-out poisoning defense | **+2 → −1** (0.82) | 5.9h, 4 attempts | 3 experiments on CIFAR-10 with ResNet-18, read against the published adaptive-poisoning results. | Biggest verdict reversal in the set. The 3% experiment gave 100% attack success both with and without the defense, so its setup is odd. The report says the 1% and 3% runs change trigger and training schedule together, so they don't isolate the effect. Partitions were shuffled rather than split by data source. |
| **508** | Learned label-preserving transformations against clean-label poisoning | **−1 → +1 → 0** (0.70) | 7.9h | One end-to-end experiment carries the verdict, alongside conflicting prior work. | The verdict swung across the whole range. The deciding experiment is **20 trials**: 55% vs 50% attack success, with intervals of roughly 30–77%. It didn't reproduce the published attack's strength. |
| **507** | Reward-trained LegalBench models rely on shortcuts that only certain inputs can detect | −1 → 0 → −1 (0.72) | 7.6h, 5 jobs | 4 experiments, including a training run that reached 79/79 on the verifier. Multi-part claim. | The experiments mostly **support** the claim: near-perfect fit plus measurable sensitivity to legally irrelevant edits. The −1 rests on a literature argument about whether the shortcuts are detectable *only* through those inputs, which wasn't tested. |
| **519** | A defense still works against defense-aware poisoning at ≤1% budget | +2 (0.91) → +1 (0.60) | 10.9h, 5 jobs | One experiment against two adaptive attacks, plus a published adaptive-attack result. | The report admits its attack search was weak (development attack success never above 9.3%), so it **can't tell a robust defense from an under-optimized attacker**. Single seed. The literature notes defenses like this have repeatedly fallen to attacks built against them. |
| **475** | Neuro-symbolic monitors and shields on ToN-IoT | +1 → 0 → +1 (0.50) | 5.4h | Complex claim with 4 parts; 2 experiments plus literature on finite-state monitors. | The shield built to the claim's own spec reached 99.96% blocking, not the required 100%. Trace-level attack detection was never measured. Confidence is 0.5. |

### Meet the first three criteria but less to doubt
- **510** (cyber-defense agent behind an action gate; +2, 0.8, 6.6h): the experiments are decisive (0/137 prohibited actions executed, 1,287/1,287 authorized ones). But the gate blocks prohibited actions by design, so the prediction is probably right.
- **521** (linear probe detects knowledge conflicts; +2, 0.9, 5.1h): replicated three times. It's a simpler claim, and the samples are small (15–27 pairs).
- **511** (constant steering vectors vs prompting; −1, 6.8h of real work): a solid experiment (0 of 64 concepts met all three conditions) that agrees with the literature, so there's little to doubt.

### Excluded
- **Experiments never measured what the claim is about:** 460, 462, 473, 474, 482, 512, 514, 518.
- **Under 5h of real work:** 70, 472, 506, 516, 517. Also 470 and 513, whose long runtimes are mostly a single stall of 11–12 hours.
- **75:** the experiments ran, but the test harness's own control checks failed.

If you can only dig into one, make it 515: it's the most complex claim, and its main weakness is easy to state and check.