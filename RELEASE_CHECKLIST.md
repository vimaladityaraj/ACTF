# Public release checklist

## Included in software release 2.0.1
- Order-independent protocol comparison in JavaScript, including the unknown-timing gate for observed/estimated records.
- Overflow-safe normalization with finite-result validation and regression tests.
- Regression tests for asymmetric completion bounds, license files, citation metadata, Git configuration, updated documentation, and regenerated verification records.
- Original study inputs, geometry and outputs retained; schema remains 2.0.

## Author actions before making the repository public
- Review and approve the code, mathematical derivations, AI disclosure and proposed MIT/CC0 licensing; confirm figure rights. The license files are prepared for the author to adopt, not independent evidence of rights ownership.
- Verify all remaining manuscript citations and Tamil lexicon entries against the original sources where possible.
- In the manuscript, reconcile ACTF with the expanded name (Arusuvai Computational Taste Framework); add the author's preferred public correspondence email. Update the test description to distinguish the original 29 tests from the additional release regressions if reporting the updated suite.
- Create a public GitHub repository and upload the extracted contents to its root, including hidden Git configuration files. Create tag/release `v2.0.1`. Archive that specific release on Zenodo and add its actual DOI and URL to the manuscript's data/code availability statement and to `CITATION.cff`/README as appropriate. Regenerate the checksums after editing those files. No DOI or repository has been created by this package.
- Submit the corrected manuscript and this supplement to the chosen preprint server; use the server's required manuscript format and disclosure policy. No posting or peer review is implied.
