import pandas as pd
import copy

def load_data(fn):
    return pd.read_csv(fn)

def report_violations(results):
    print("Reporting violations for correction...")

def do_stats(results):
    print("Calculating statistics...")
    stats = {}
    for k in results.keys():
        stats[k] = results[k].shape[0]
    return stats

def low_profit_margin_products(df):
    d = df.copy()
    d['profit'] = d['sales_price'] - d['cost']
    d['profit_margin'] = d['profit'] / d['sales_price']
    return d.loc[d['profit_margin'] < 0.1]

def low_sales_price_products(data):
    d = df.copy()
    return d.loc[d['sales_price'] < 30]


class Filter(object):

    """
    A Filter object is a wrapper around a filter function,
    with some metadata (eg. name, description) attached.
    """

    def __init__(self, name, desc, f):
        """
        f is the filter function itself (not the result of
        calling the function on a dataset). It will be the
        job of the Filter object to run the function on the
        data it is given
        """
        self.name = name
        self.desc = desc
        self.f = f

    def apply(self, data):
        """
        apply actually runs the filter function that was
        passed into the constructor and returns the results.
        """
        return self.f(data)


if __name__=='__main__':
    """
    We can use our Filter class to build up a list of all the
    filters we want to run on our data. Once we have built the
    list, we can run each Filter in turn.
    """
    filters = [
        Filter(
            name="T1",
            desc="Low profit margin products",
            f=low_profit_margin_products,
        ),
        Filter(
            name="T2",
            desc="Low sales price products",
            f=low_sales_price_products,
        ),
    ]

    fn = 'example-data.csv'
    df = load_data(fn)

    # We could also 1-line this using a Python list comprehension:
    #
    # results = {f.name: f.apply(df) for f in filters}
    results = {}
    for f in filters:
        results[f.name] = f.apply(df)

    report_violations(results)
    stats = do_stats(results)
    for k, v in stats.items():
        print(f"  Test {k}: {v} violations found")
