# Bug report for 4D Nucleome (2022/09/23)

## Synopsis

Fetching pixels from several (possibly all) .mcool files from the 4DNucleome data portal using the Cooler Python API
sometimes results in duplicate values for certain columns/rows of pixels.

Script `find_dupl_pixels.py` can be used to look for duplicate pixels in intra-chromosomal regions.

## Example

The following output was obtained by running `find_dupl_pixels.py` on
file [4DNFI9GMP2J8.mcool](https://data.4dnucleome.org/files-processed/4DNFI9GMP2J8/):

```bash
./find_dupl_pixels.py --bin-size 2000 4DNFI9GMP2J8.mcool | head -n 11
```

| chrom1 | start1   | end1     | chrom2 | start2   | end2     | count | balanced     |
|--------|----------|----------|--------|----------|----------|-------|--------------|
| chr1   | 10828000 | 10830000 | chr1   | 11002000 | 11004000 | 1     | 0.000208987  |
| chr1   | 10828000 | 10830000 | chr1   | 11002000 | 11004000 | 1     | 0.000208987  |
| chr1   | 10828000 | 10830000 | chr1   | 11006000 | 11008000 | 1     | 0.000199523  |
| chr1   | 10828000 | 10830000 | chr1   | 11006000 | 11008000 | 3     | 0.000598569  |
| chr1   | 10828000 | 10830000 | chr1   | 11010000 | 11012000 | 4     | 0.000695946  |
| chr1   | 10828000 | 10830000 | chr1   | 11010000 | 11012000 | 2     | 0.000347973  |
| chr1   | 10828000 | 10830000 | chr1   | 11020000 | 11022000 | 1     | 0.000219669  |
| chr1   | 10828000 | 10830000 | chr1   | 11020000 | 11022000 | 1     | 0.000219669  |
| chr1   | 10828000 | 10830000 | chr1   | 11030000 | 11032000 | 3     | 0.000499071  |
| chr1   | 10828000 | 10830000 | chr1   | 11030000 | 11032000 | 2     | 0.000332714  |
| ...    | ...      | ...      | ...    | ...      | ...      | ...   | ...          |

TSVs with duplicate pixels for all resolutions
from [4DNFI9GMP2J8](https://data.4dnucleome.org/files-processed/4DNFI9GMP2J8/) are
available [here](https://github.com/robomics/20220923_4dnucleome_bug_report/files/9635539/4DNFI9GMP2J8.tar.gz).

Datasets [4DNFIFJH2524](https://data.4dnucleome.org/files-processed/4DNFIFJH2524/)
and [4DNFINNZDDXV](https://data.4dnucleome.org/files-processed/4DNFINNZDDXV/) are affected by the same issue (reports
for these datasets are available
here: [link1](https://github.com/robomics/20220923_4dnucleome_bug_report/files/9635594/4DNFIFJH2524.tar.gz)
, [link2](https://github.com/robomics/20220923_4dnucleome_bug_report/files/9635593/4DNFINNZDDXV.tar.gz))

Luckily, the base resolutions do not seem to have any duplicate values, suggesting that the issue is caused
by `cooler zoomify` (Cooler v0.8.3 according to the .mcool metadata).

Indeed, zoomifying the base resolution using Cooler v0.8.11 (the latest version at the time of writing) solves the issue.

