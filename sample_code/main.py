def calculate_delay(arrival, scheduled):
    # simple demo function — intentionally tiny for review
    return (arrival - scheduled) if arrival and scheduled else None


def unused_function(x):
    # this is unused and should be flagged
    return x * 2
