# EOS-06 Satellite Data Histogram Generator

A Python tool for processing EOS-06 satellite NetCDF (.nc) files and generating histograms for all data variables. The tool automatically extracts data from NetCDF files, computes statistical summaries, and generates histogram data saved as text files.

## Features

- **Automatic NetCDF Processing**: Reads and processes EOS-06 satellite data files
- **Multi-variable Support**: Processes all data variables in a single run
- **Data Cleaning**: Automatically handles NaN and infinite values
- **Statistical Analysis**: Computes comprehensive statistics (mean, std dev, min, max, median, count)
- **Flexible Output**: Creates separate histogram files for each variable
- **Command-line Interface**: Easy-to-use CLI with multiple options
- **Metadata Preservation**: Includes variable attributes and metadata in output files

## Requirements

### Python Dependencies

```bash
pip install netcdf4 numpy
```

### Python Version
- Python 3.6 or higher

## Installation

1. Download the `eos06_histogram.py` script
2. Install required dependencies:
   ```bash
   pip install netcdf4 numpy
   ```
3. Make the script executable (optional):
   ```bash
   chmod +x eos06_histogram.py
   ```

## Usage

### Basic Usage

Process a NetCDF file with default settings:
```bash
python eos06_histogram.py BAND.nc
```

### Advanced Usage

```bash
# Specify output directory
python eos06_histogram.py BAND.nc -o histogram_results

# Use custom number of bins
python eos06_histogram.py BAND.nc -b 100

# Process specific variables only
python eos06_histogram.py BAND.nc -v temperature radiance chlorophyll

# Combine all options
python eos06_histogram.py BAND.nc -o results -b 75 -v band1 band2 band3
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | Path to input .nc file | Required |
| `-o, --output` | Output directory for histogram files | Same as input file |
| `-b, --bins` | Number of histogram bins | 50 |
| `-v, --variables` | Specific variables to process | All data variables |

## Output Format

### File Naming Convention
Output files are named: `{input_filename}_{variable_name}_histogram.txt`

Example: `BAND_chlorophyll_histogram.txt`

### Output File Structure

Each histogram file contains:

1. **Header Section**:
   - Variable name and generation timestamp
   - Variable metadata (units, description, etc.)
   - Statistical summary

2. **Data Section**:
   - Four columns: `bin_center, count, bin_left_edge, bin_right_edge`

### Example Output File

```
# Histogram for variable: chlorophyll_a
# Generated on: 2025-08-13 14:30:25
# Variable info:
#   units: mg/m^3
#   long_name: Chlorophyll-a concentration
#   valid_range: [0.01, 100.0]
#   shape: (1024, 1024)
#   dtype: float32
#
# Statistics:
#   Count: 1048576
#   Mean: 2.456789
#   Std Dev: 1.234567
#   Min: 0.010000
#   Max: 45.678901
#   Median: 1.987654
#
# Format: bin_center, count, bin_left_edge, bin_right_edge
#
0.325000, 12543, 0.010000, 0.640000
0.955000, 15678, 0.640000, 1.270000
1.585000, 18234, 1.270000, 1.900000
...
```

## EOS-06 Satellite Data

This tool is specifically designed for EOS-06 (Oceansat-3) satellite data, but can work with any NetCDF4 files containing numerical data arrays. Common EOS-06 data products include:

- **OCM (Ocean Colour Monitor)** data
- **SSTM (Sea Surface Temperature Monitor)** data
- **Level-1, Level-2, and Level-3** processed products

## Data Processing Details

### Variable Selection
- Automatically processes all multi-dimensional data variables
- Skips coordinate variables (typically 1D arrays like latitude, longitude, time)
- Option to process specific variables using `-v` flag

### Data Cleaning
- Removes NaN (Not a Number) values
- Removes infinite values
- Reports count of valid data points processed

### Multi-dimensional Data
- Flattens multi-dimensional arrays for histogram computation
- Preserves original array shape information in metadata

## Troubleshooting

### Common Issues

1. **File Not Found Error**:
   ```
   Error: Input file 'filename.nc' not found.
   ```
   - Ensure the file path is correct
   - Use absolute path if file is in different directory

2. **Permission Errors**:
   - Ensure write permissions for output directory
   - Use `-o` flag to specify writable directory

3. **Memory Issues with Large Files**:
   - Process specific variables using `-v` flag
   - Use fewer bins with `-b` flag

4. **No Valid Data Warning**:
   ```
   Warning: No valid data found for variable variable_name
   ```
   - Variable contains only NaN or infinite values
   - Check data quality and valid ranges

### Debugging

Enable verbose output by adding print statements or use Python debugger:

```bash
python -i eos06_histogram.py BAND.nc
```

## Examples

### Process All Variables
```bash
python eos06_histogram.py E06_OCM_GAC_06AUG2025.nc
```

### High-Resolution Histograms
```bash
python eos06_histogram.py data.nc -b 200 -o detailed_histograms
```

### Process Specific Bands
```bash
python eos06_histogram.py BAND.nc -v band_1 band_2 band_3 band_4
```

## File Structure

```
project_directory/
├── eos06_histogram.py     # Main script
├── README.md             # This file
├── BAND.nc              # Example input file
└── histogram_results/    # Output directory (created automatically)
    ├── BAND_band_1_histogram.txt
    ├── BAND_band_2_histogram.txt
    └── ...
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

## License

This tool is provided as-is for processing EOS-06 satellite data. Please ensure compliance with any data usage policies from ISRO/DOS.

## Support

For issues related to:
- **Script functionality**: Check troubleshooting section above
- **EOS-06 data format**: Refer to ISRO documentation
- **NetCDF format**: See [NetCDF documentation](https://www.unidata.ucar.edu/software/netcdf/)

## Version History

- **v1.0**: Initial release with basic histogram generation
- Current features: Multi-variable processing, statistical analysis, flexible output options
