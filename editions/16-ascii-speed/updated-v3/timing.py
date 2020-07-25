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

    n = 2

    normal_t = timeit.timeit(lambda: asciiart.color_mask(imarray, asciiart.closest_ANSI_color), number=5)
    # ~16.5s/run
    print(f"normal: {normal_t/n} per run")

    snapper_t = timeit.timeit(lambda: asciiart.color_mask(imarray, asciiart.rgb_to_ansi), number=n)

    # ~0.5s/run -> 30x speedup!
    print(f"snapper: {snapper_t/n} per run")

    # NOTE: we don't count the time it takes to load the color map from disk
    converter = asciiart.PrecomputedRgbToAnsiConverter.from_file('./color_map.json')

    # ~0.05s/run -> a further 10x speedup, and a 300x speedup over the original approach!
    precomputed_t = timeit.timeit(lambda: asciiart.color_mask(imarray, converter.rgb_to_ansi), number=n)
    print(f"precomputed: {precomputed_t/n} per run")
