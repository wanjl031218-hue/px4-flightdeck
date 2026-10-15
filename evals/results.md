# Evaluation record

Version: 0.2.0. Date: 2026-10-15. Fixtures are synthetic.
Local checks ran on macOS arm64 with Python 3.14.7. CI targets Python 3.9 and 3.12;
those environments and remote GitHub Actions have not run in this session.

| Layer | Status | Meaning |
| --- | --- | --- |
| Skill frontmatter/package | Passed local validator, UI/CI YAML parsing and local reference checks | Structural validity, not task competence |
| Helpers, installation/update, scorer and archives | 23 local unittest checks passed | Includes analytic metric cases, failed-update recovery, reproducible ZIPs and installation from an extracted source ZIP; no simulator |
| Technical provenance | 15 upstream files recorded by commit and SHA-256 | PX4 v1.17.0 source APIs, px4_msgs local-position schema and a documentation snapshot inspected; not a compatibility certification |
| Python example syntax | Passed locally with Python 3.9 grammar | ROS dependencies were not imported and no ROS node ran |
| Independent-agent response review | Four requests reviewed on v0.1.0 | Historical response-only review; not rerun after v0.2.0 technical additions |
| With/without-skill comparison | Not run | No quantified improvement claimed |
| PX4/ROS 2 simulation acceptance | Not run | No flight behavior verified |
| Hardware/client compatibility | Not run | No real vehicle or other-client acceptance |

## v0.2.0 executable checks

The synthetic step example has squared errors `[1, .04, .01, 0, 0]` at one-second
intervals. Independent hand calculation gives trapezoidal area `.55`, vector RMSE
`sqrt(.55/4) = 0.37080992435478316 m`, overshoot `0.1 m` / `10%`, and settling `3 s`
with tolerance `.05 m` and dwell `1 s`. The scorer produced those values. Additional
cases cover irregular time weighting, negative steps, late excursions, invalid samples,
non-finite values, missing window boundaries, zero steps, duplicate timestamps and gaps.
These checks validate the declared table calculations, not ULog conversion or flight health.

Archive tests compare repeated builds byte-for-byte, validate ZIP entries/integrity,
extract a source archive and run its installer into a temporary discovery directory,
then compare installed content with the standalone skill archive. Failed-copy update
testing confirms restoration of the prior installation and its local notes.

The read-only C++ example was checked against upstream module/scheduler/subscription
patterns. Both example runbooks state that PX4/ROS compilation and runtime acceptance
remain unrun. No VM connection or vehicle operation was performed.

## Historical independent response review (v0.1.0)

A fresh evaluator received the skill, requests, and raw fixtures without expected
answers, prior diagnoses, reviewer criteria, or personal learning notes. The evaluator
used relevant skill references, inspected fixture files, and calculated a small CSV
summary with Python. It did not build or run a simulator, access a VM, or affect a vehicle.

- **Deployment mismatch (case 2):** identified r8 source versus r5 installed/startup
  evidence; withheld claims of a verified landing fix. Separated filesystem skew from
  sensor timing and requested the actual execution/build paths.
- **Policy and missing snapshot (case 10):** detected conflicting change budgets,
  computed the two-row means (RMSE 0.225 m, overshoot 0.165 m), and supplied conditional
  mechanisms rather than invented numeric parameters or rollback values.
- **Style consistency (case 5):** both Plain and Academic responses preserved the
  discovery-versus-delivery distinction and requested actual topic/type/QoS evidence.
  This premise is already illustrated in the style reference, so this checks faithful
  use of an example rather than demonstrating unseen transfer.
- **Coordinate/style transfer (case 13):** both styles derived `target.z = -1.8 m`
  from the supplied NED reference, distinguished relative height from ground height,
  and required fresh valid feedback plus declared tolerances/dwell before arrival
  acceptance. No actual arrival was claimed. The topic differs from the style example;
  its underlying frame principle is included in the development reference.

These are qualitative observations from one evaluator, not repeated independent trials
or a with/without-skill benchmark. Some requests deliberately lack evidence needed for
full numeric or runtime completion. No efficiency or flight-performance improvement
is inferred from these responses.
