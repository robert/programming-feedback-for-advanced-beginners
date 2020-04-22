import pandas as pd
import copy

def load_data(file):
    print("Loading data...")
    data = pd.read_csv(file)
    return data

def process_test(t, data):
    """Wrap function call to each test."""
    try:
        func = eval("process_" + t)
        result = func(data)
    except NameError:
        print(f"Error: {t} not implemented")
        result = None
    return result

def report_violations(results):
    print("Reporting violations for correction...")

def do_stats(results):
    print("Calculating statistics...")
    stats = {}
    for k in results.keys():
        stats[k] = results[k].shape[0]
    return stats

# Implementation of tests
# could also be in separate library

def process_T1(data, **kwargs):
    description = "T1: low profit margin products"
    if "description_only" in kwargs.keys():
        description_only = kwargs["description_only"]
    else:
        description_only = False
    if description_only:
        return description
    print("  "+description)
    d = copy.copy(data)
    d['profit']=d['sales_price']-d['cost']
    d['profit_margin'] = d['profit']/d['sales_price']
    res = d.loc[d['profit_margin']<0.1]
    return res

def process_T2(data, **kwargs):
    description = "T2: low sales price products"
    if "description_only" in kwargs.keys():
        description_only = kwargs["description_only"]
    else:
        description_only = False
    if description_only:
        return description
    print("  "+description)
    d = copy.copy(data)
    res = d.loc[d['sales_price']<30]
    return res

# Main program

if __name__=='__main__':
    # list of tests we want to perform
    TESTS = ['T1', 'T2', 'T3']

    fn='sample_data.csv'
    data = load_data(fn)
    results = {}
    print("Processing Tests...")
    for t in TESTS:
        res = process_test(t, data)
        if res is not None:
            results[t] = res
    report_violations(results)
    stats = do_stats(results)
    for k in stats.keys():
        print(f"  Test {k}: {stats[k]} violations found")
