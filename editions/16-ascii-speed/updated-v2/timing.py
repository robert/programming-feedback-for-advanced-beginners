import timeit
import asciiart

"""
Use the `timeit` module to time and compare the new
and old color mapping approaches.
"""

if __name__ == "__main__":
    filename = 'sample.jpg'
    width = 80

    imarray = asciiart.initial_process(filename, width)

    n = 5

    normal_t = timeit.timeit(lambda: asciiart.color_mask(imarray, asciiart.closest_ANSI_color), number=5)
    # ~6.2s/run
    print(f"normal: {normal_t/n} per run")

    snapper_t = timeit.timeit(lambda: asciiart.color_mask(imarray, snap), number=n)

    # ~0.18s/run - >30x speedup!
    print(f"snapper: {snapper_t/n} per run")
