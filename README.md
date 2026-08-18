# Inference campaign contracts

This repository is the neutral canonical source shell for two experimental,
backend-neutral inference contracts incubated in RIFT and exercised through a
private RIFT/R3 radiative-transfer gate:

- `evaluation.record-draft/v0`, a closed request/result envelope vocabulary;
- `campaign.assimilation/v0`, an atomic, replay-safe result-assimilation
  transition plus a standard-library reference reducer.

The gate provides cross-domain mechanical design evidence, not production
conformance or scientific validation. Both contracts remain experimental.

## Scope

This source-only repository contains schemas, synthetic reference fixtures,
the reference reducer, normative documentation, acceptance tests, and source
provenance. It is not an installable package and publishes no release or stable
API.

It deliberately contains no RIFT, SuperNu, or population-inference adapter;
domain schema; proposal policy; scheduler; transport; archive implementation;
native fixture; campaign record; or historical run evidence. Project adapters
and scientific semantics remain owned by their respective projects.

No project should vendor these files or add this repository as a production
dependency yet. Packaging, release, project adoption, and drift-registry edges
require separate reviewed issues.

## Validation

Run the standard-library acceptance suite from the repository root:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

If the optional test-only `jsonschema` library is present, the same command also
checks both Draft 2020-12 schemas and the synthetic positive/negative examples.
The reducer itself imports only the Python standard library.

## Ownership

Richard O'Shaughnessy is the accountable owner and sole initial representative
for both the RIFT and non-GW/R3 workflows. Scientific exceptions remain solely
under each affected project's scientific review process. A registry or runner
may observe adopted versions but cannot waive protocol or scientific semantics.

See `PROVENANCE.json` for the exact RIFT incubation source identities. This
repository is public under the MIT license and contains no private gate evidence
or native science data.
