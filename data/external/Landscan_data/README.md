# LandScan Program

## Overview
The LandScan Program was initiated at Oak Ridge National Laboratory (ORNL) in 1997 to address the need for improved population estimates for consequence assessment. This need arises from natural and manmade disasters that place vast populations at risk with little or no advance warning. The program aims to create a more realistic population distribution model that captures where people are likely to be throughout the day, not just at residential locations as reported in official censuses.

## LandScan Global
LandScan Global was the first product of this effort, launched in 1998 and updated annually since then. It provides highly resolved population estimates useful for evaluating events across multiple geographic scales.

## LandScan Statistics
LandScan Global represents the finest resolution global population distribution data available, providing an ambient (24-hour average) population estimate. The algorithm, an R&D 100 Award Winner, uses spatial data, high-resolution imagery, and a multi-variable dasymetric modeling approach to disaggregate census counts within an administrative boundary. The model is tailored to match the data conditions and geographical nature of each country and region, capturing the full potential activity space of people throughout the day and night.

## Setup
To download the necessary data from Google Drive, follow these steps:

1. Ensure you have the necessary Python packages installed:

    ```sh
    pip install gdown tqdm
    ```

2. Run the download script to fetch and extract the data from Google Drive:

    ```sh
    python download_data.py --type raw
    ```

    or

    ```sh
    python download_data.py --type processed
    ```

## License
These datasets are offered under the Creative Commons Attribution 4.0 International License. Users are free to use, copy, distribute, transmit, and adapt the data for commercial and non-commercial purposes, without restriction, as long as clear attribution of the source is provided. For more information, please refer to the CC BY 4.0 documentation.
