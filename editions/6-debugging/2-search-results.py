def search_all(queries):
    all_results = []
    for q in queries:
        results = search(q)
        all_results.append(results)
    return all_results

def search(query):
    """
    This function is a "fake" search engine
    that we use to make this bugsquashing
    exercise more concise. In the original
    program this function queried an
    internet search engine.

    Now it returns "fake" search results
    by appending "-0", "-1", and "-2" to
    the given query. For example, the query
    "banana" will return:

    ["banana-0", "banana-1", "banana-2"]

    Note that using "fake" functions to
    simplify programs while testing or
    debugging is not cheating - it is a very
    common and sensible technique!
    """
    results = []
    for i in range(3):
        results.append(query + "-" + str(i))
    return results

if __name__ == "__main__":
    test_queries = ["cat", "dog", "mouse"]
    test_results = search_all(test_queries)

    expected_results = [
        "cat-0",
        "cat-1",
        "cat-2",
        "dog-0",
        "dog-1",
        "dog-2",
        "mouse-0",
        "mouse-1",
        "mouse-2",
    ]
    # TODO: it looks like there's a bug with
    # our searching function! We should
    # figure out what it is and fix it so
    # that this test passes.
    if test_results == expected_results:
        print("TEST PASSED!!")
    else:
        print("TEST FAILED!!")
