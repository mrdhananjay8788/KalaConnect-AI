# Phase 6 Evaluation Metrics

To scientifically evaluate the B2B Matchmaking Engine:

1. **Precision@K / Recall@K**: Is the engine accurately isolating the best subsets of artisans in its highest ranks?
2. **Fulfillment Feasibility Rate**: Percentage of matches historically leading to successful end-to-end B2B completion without cancellation due to capacity/shipping mismatches.
3. **Quantity Coverage Ratio**: In split-order scenarios, what percentage of the buyer's desired quantity is successfully allocated across candidates?
4. **Fairness Gini Coefficient**: Ensuring historical B2B order dominance does not permanently restrict newly onboarded marginalized artisans from securing pipeline visibility.
5. **Zero-Match Rate**: Percentage of searches failing to pass the hard-constraint threshold logic.
6. **Delivery Feasibility Delta**: Absolute difference between `estimated_delivery_days` and real-world SLA.
