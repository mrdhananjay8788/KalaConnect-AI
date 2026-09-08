# Phase 5 Evaluation Metrics

To scientifically evaluate the Hybrid Search architecture in Phase 5:

1. **Precision@K**: Of the top `K` results returned, what percentage were actually relevant?
2. **Recall@K**: Did the system successfully retrieve all relevant items in the catalog within the top `K` slots?
3. **NDCG@K (Normalized Discounted Cumulative Gain)**: Are the highly relevant items correctly placed at the *very top* of the list?
4. **Zero-Result Rate**: The percentage of searches returning empty or only alternatives.
5. **Language Boundary Crossing**: Percentage of successful matches where `Query Language != Product Native Language`.
6. **Average Latency**: Embedding generation + Vector Store lookup target < `150ms`.
