# Grill Impact Level and Uncertainty

**MUST MARK** each question's impact level.

### Low Level (0)
- Constant value
- Configuration value
- Local variable / internal logic
- Function implementation
- Single-module internal structure
- Single-module data structure

### Medium Level (1)
- Multi-function logic
- Multi-file change
- Module internal behavior
- Module interface
- Shared data structure

### High Level (2)
- Database schema
- Cross-service logic
- API contract
- Data migration
- External library / service integration
- Protocol / file format
- Deployment architecture
- System architecture
- Cross-system contract
- Platform / OS / hardware dependency
- External organization / vendor contract
- Production-scale breaking change

## Uncertainty
**MUST MARK** each question's uncertainty.
- High: Can not known until execute and see the result
- Low: Obviously know the expected result

For every High uncertainty question, recommend the smallest experiment (spike, prototype, one-off script, manual probe) that would turn it into Low uncertainty before committing to an answer.

## Action
- Low impact level + Low uncertainty = Always show the question; asking for confirmation is optional (skip-if-obvious).
- Low impact level + High uncertainty = Always show the question; asking for confirmation is optional (skip-if-obvious). Mark to add assertion point (like assert in c++ or something). Recommend an experiment.
- High impact level + Low uncertainty = Ask question and confirm.
- High impact level + High uncertainty = Ask question and confirm. Mark to add assertion point. Recommend an experiment.
