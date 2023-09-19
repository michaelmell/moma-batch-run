# MoMA batch run

This project contains a companion script for processing large datasets with [MoMA (Mother Machine Analyzer)](https://github.com/nimwegenLab/moma).

## Table of Contents

- [MoMA batch run](#moma-batch-run)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [About MoMA](#about-moma)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
  - [Usage](#usage)

## About

[MoMA (Mother Machine Analyzer)](https://github.com/nimwegenLab/moma) loads and processes each growthlane of in a Mother machine experiment separately. The Python companion script `moma_batch_run.py` in this project is a command line interface for processing large sets of Growthlanes with MoMA. The script is included in the [containerized distribution of MoMA](https://github.com/nimwegenLab/moma-module). It achieves the following:

- facilitate efficient workflow for processing large datasets by separating steps of (1) tracking, (2) curation, and (3) data export (see [here](https://github.com/nimwegenLab/moma/wiki/moma-batch-processing) for more information)
- provide convenient command line interface for this workflow
- (optionally) use Slurm for concurrent processing of growthlanes allowing to process hundreds of growthlanes with in a few minutes

### About MoMA

The MoMA (Mother Machine Analyzer) software is designed to process data from Mother machine experiments. Mother machines are microfluidic devices used to study bacterial growth over extended periods of time (spanning multiple days) at the single-cell level. MoMA aids in tracking and segmenting individual cells in these experiments. MoMA combines deep learning for image processing with mathematical optimization for tracking to achieve low error rates and to enable semi-automatic curation of tracking solutions to efficiently correct errors in segmentation and tracking.

More information on MoMA can be found [here](https://github.com/nimwegenLab/moma).

## Getting Started

The script `moma_batch_run.py` is included in the containerized distribution of MoMA and not meant to be set up separately. You can look at the `Dockerfile` in the [MoMA Git repository](https://github.com/nimwegenLab/moma), if you are interested in its usage inside the container and to understand how you might set it up outside a container.

## Usage

You can find usage information [here](https://github.com/nimwegenLab/moma/wiki/moma-batch-processing).

