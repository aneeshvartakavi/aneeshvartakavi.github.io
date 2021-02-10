Title: Chunked Similarity Matrix Calculations
Date: 2019-08-12 14:21
Modified: 2019-08-12 15:30
Category: python
Tags: python, sklearn, machine learning, gracenote
Slug: My-first-post
Authors: Aneesh Vartakavi
Summary: Computing large similarity matrices efficiently in sklearn using `pairwise_distances_chunked`.
status: draft

I recently found myself working on a content-to-content recommendation problem for movies and TV shows. The goal was to allow a user to combine different 'dimensions' of similarity (eg. Cast and Crew, Audience, Genre etc) in different amounts, leading to a dynamic list of similar programs to a given seed program. This approach dictated that the different dimensions behave predictably and consistently, and have explainable behavior. The project was a small component of a larger project in the video metadata space.

We were tasked to design a similarity score which combined similarity along various descriptive attributes like genre, scenario, mood cast and crew, etc. Our baseline approach was to compute attribute similarity using a simple distance measure (eg. Jaccard, Cosine) and combine the scores as a weighted sum to produce the final score. We decided to learn the weights using Machine Learning using linear regression. We trained and evaluated our model on data annotated by in-house experts (binary annotations of pairwise program similarity). Our initial metrics combined with subjective feedback showed us that our baseline was performing well, and we decided to deploy.

We quickly ran into issues of scale. Our initial approach to compute pairwise distances looked like this:

```python
for feature in features:
    dist_matrix[feature] = sklearn.metrics.pairwise_distances(X[feature], metric=metrics[feature])
```

This worked fine when we were prototyping with small subsets of data, but as we now had to compute pairwise distances between 250K programs along 20 different dimensions before combining them to create a final similarity score. In total, this results in 250K * 250K * 20 (1.25e12) similarity calculations, or half that number if we assume that we don't have to compute the redundant half of the symmetric matrix. By this time, the larger project vision and engineering requirements had crystallized, and spinning up a cluster of machines was infeasible.

The solution we found came about from the understanding that each row of the distance matrix is independent, and the pairwise similarity and similarity can be performed one row at a time. After some frustration and prototyping our own inefficient solution, we found a function that I had somehow missed, `sklearn.metrics.pairwise_distances_chunked`. From the documentation:

```python
sklearn.metrics.pairwise_distances_chunked(X, Y=None, reduce_func=None, metric=’euclidean’, n_jobs=None, working_memory=None, **kwds)

Generate a distance matrix chunk by chunk with optional reduction

In cases where not all of a pairwise distance matrix needs to be stored at once, this is used to calculate pairwise distances in working_memory-sized chunks.
```

This was exactly what we needed. The final approach created a generator for each similarity matrix, which was then combined with a weighted sum like so:

```python
# Create a generator for the distance matrix for each feature
generators = []
for feature in features:
    generators.append(
        pairwise_distances_chunked(
            matrices[f],
            metric=metrics[feature],
            n_jobs=n_jobs,
            working_memory=working_memory,
        )
    )

# Compute the distances
for values in zip(*generators):
    # Combine scores using the regressor
    total_score = combine_scores(values)
    # Store the results
```

By tweaking `n_jobs` and `working_memory` to match our system, we were able to finally compute similarity scores efficiently without large resource requirements.

Things I learnt along the way:

* `pairwise_distances` is a lot faster with built in metrics. Let's say you wanted jaccard similarity but the function only supports to jaccard distance, it's faster to invert the jaccard distance after the calculation than pass in a user defined function for jaccard similarity to `pairwise_distances`.

* PCA helped to reduce the memory footprint, but `pairwise_distances_chunked` wasn't significantly faster on inputs with fewer dimensions.

* Sparsity - If your input data is sparse and distance metrics support sparsity, this could make a large difference.

* We tried MinHashing and learning smaller dimensional dense representations, but didn't get very far in the limited time we had.
