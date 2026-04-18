# Goal

Optimize ten continuous composition variables to minimize `regret`, where:

- `regret = Target.max() - Target`
- lower regret is better
- minimizing regret is equivalent to seeking high predicted HER performance

Each evaluation queries a random-forest mock oracle trained on the bundled HER dataset and returns a standard `EvaluationResult` with primary objective `regret`.
