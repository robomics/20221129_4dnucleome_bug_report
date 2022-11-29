#!/usr/bin/env python3

# Copyright (C) 2022 Roberto Rossini <roberros@uio.no>
#
# SPDX-License-Identifier: MIT

import argparse
import sys

import cooler


def make_cli():
    cli = argparse.ArgumentParser()
    cli.add_argument("cooler",
                     nargs="+",
                     type=str,
                     help="One or more .(m)cool files to validate")

    cli.add_argument("--bin-size",
                     type=int,
                     required=True,
                     help="Cooler resolution.")
    return cli


def path_to_uri(path, bin_size):
    if bin_size is not None:
        return f"{path}::/resolutions/{bin_size}"
    return path


def fetch_pixels(cooler_fp, name, size):
    try:
        return cooler_fp.matrix(as_pixels=True,
                                balance=True,
                                join=True).fetch(f"{name}:0-{size}")
    except ValueError:
        return cooler_fp.matrix(as_pixels=True,
                                balance=False,
                                join=True).fetch(f"{name}:0-{size}")


if __name__ == "__main__":
    args = make_cli().parse_args()

    cols = ["chrom1", "start1", "end1",
            "chrom2", "start2", "end2"]

    print_header = True

    # Loop over cooler files
    for path in args.cooler:
        c = cooler.Cooler(path_to_uri(path, args.bin_size))
        # Loop over chromosomes
        for name, size in c.chromsizes.items():
            # Fetch intra-chromosomal interactions
            pixels = fetch_pixels(c, name, size)
            coords = pixels[cols]

            # Look for duplicate pixels
            dupl = coords[coords.duplicated(keep=False)].sort_values(by=cols)

            if dupl.shape[0] != 0:
                # Report duplicates
                pixels.iloc[dupl.index].to_csv(sys.stdout,
                                               sep="\t",
                                               header=print_header,
                                               index=False)
                print_header = False
