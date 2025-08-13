"""
EOS-06 Satellite Data Histogram Generator
Reads .nc files and computes histograms for all variables, saving results to text files.
"""

import netCDF4 as nc
import numpy as np
import os
import sys
from datetime import datetime
import argparse

def read_nc_file(filepath):
    """
    Read NetCDF file and return dataset object.
    
    Args:
        filepath (str): Path to the .nc file
        
    Returns:
        netCDF4.Dataset: Opened dataset object
    """
    try:
        dataset = nc.Dataset(filepath, 'r')
        return dataset
    except Exception as e:
        print(f"Error reading NetCDF file: {e}")
        return None

def compute_histogram(data, bins=50, var_name=""):
    """
    Compute histogram for given data array.
    
    Args:
        data (numpy.array): Input data array
        bins (int): Number of bins for histogram
        var_name (str): Variable name for labeling
        
    Returns:
        tuple: (bin_edges, histogram_counts, statistics)
    """
    # Remove NaN and infinite values
    clean_data = data[np.isfinite(data)]
    
    if len(clean_data) == 0:
        print(f"Warning: No valid data found for variable {var_name}")
        return None, None, None
    
    # Compute histogram
    hist_counts, bin_edges = np.histogram(clean_data, bins=bins)
    
    # Compute basic statistics
    stats = {
        'count': len(clean_data),
        'mean': np.mean(clean_data),
        'std': np.std(clean_data),
        'min': np.min(clean_data),
        'max': np.max(clean_data),
        'median': np.median(clean_data)
    }
    
    return bin_edges, hist_counts, stats

def write_histogram_to_text(bin_edges, hist_counts, stats, output_file, var_name, var_info=None):
    """
    Write histogram data to text file.
    
    Args:
        bin_edges (numpy.array): Histogram bin edges
        hist_counts (numpy.array): Histogram counts
        stats (dict): Statistical information
        output_file (str): Output file path
        var_name (str): Variable name
        var_info (dict): Additional variable information
    """
    with open(output_file, 'w') as f:
        f.write(f"# Histogram for variable: {var_name}\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if var_info:
            f.write(f"# Variable info:\n")
            for key, value in var_info.items():
                f.write(f"#   {key}: {value}\n")
        
        f.write(f"#\n")
        f.write(f"# Statistics:\n")
        f.write(f"#   Count: {stats['count']}\n")
        f.write(f"#   Mean: {stats['mean']:.6f}\n")
        f.write(f"#   Std Dev: {stats['std']:.6f}\n")
        f.write(f"#   Min: {stats['min']:.6f}\n")
        f.write(f"#   Max: {stats['max']:.6f}\n")
        f.write(f"#   Median: {stats['median']:.6f}\n")
        f.write(f"#\n")
        f.write(f"# Format: bin_center, count, bin_left_edge, bin_right_edge\n")
        f.write(f"#\n")
        
        # Write histogram data
        for i in range(len(hist_counts)):
            bin_center = (bin_edges[i] + bin_edges[i+1]) / 2
            f.write(f"{bin_center:.6f}, {hist_counts[i]}, {bin_edges[i]:.6f}, {bin_edges[i+1]:.6f}\n")

def get_variable_info(dataset, var_name):
    """
    Extract variable metadata information.
    
    Args:
        dataset (netCDF4.Dataset): NetCDF dataset
        var_name (str): Variable name
        
    Returns:
        dict: Variable information
    """
    var = dataset.variables[var_name]
    info = {}
    
    # Get variable attributes
    for attr_name in var.ncattrs():
        info[attr_name] = getattr(var, attr_name)
    
    # Add shape and data type
    info['shape'] = var.shape
    info['dtype'] = str(var.dtype)
    info['dimensions'] = var.dimensions
    
    return info

def process_eos06_nc_file(filepath, output_dir=None, bins=50, variables=None):
    """
    Main function to process EOS-06 NetCDF file and generate histograms.
    
    Args:
        filepath (str): Path to input .nc file
        output_dir (str): Output directory for histogram files
        bins (int): Number of bins for histograms
        variables (list): List of specific variables to process (None for all)
    """
    # Open NetCDF file
    dataset = read_nc_file(filepath)
    if dataset is None:
        return
    
    # Setup output directory
    if output_dir is None:
        output_dir = os.path.dirname(filepath)
        # If dirname returns empty string (file in current directory), use current directory
        if output_dir == '':
            output_dir = '.'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename for output files
    base_filename = os.path.splitext(os.path.basename(filepath))[0]
    
    print(f"Processing file: {filepath}")
    print(f"Output directory: {output_dir}")
    print(f"Available variables: {list(dataset.variables.keys())}")
    print(f"Global attributes: {dict(dataset.__dict__)}")
    print("-" * 50)
    
    # Process variables
    processed_vars = 0
    
    for var_name in dataset.variables:
        var = dataset.variables[var_name]
        
        # Skip if specific variables requested and this isn't one of them
        if variables and var_name not in variables:
            continue
        
        # Skip coordinate variables (usually 1D)
        if len(var.shape) <= 1:
            print(f"Skipping coordinate variable: {var_name}")
            continue
        
        print(f"Processing variable: {var_name}")
        print(f"  Shape: {var.shape}")
        print(f"  Data type: {var.dtype}")
        
        try:
            # Read data
            data = var[:]
            
            # Flatten multi-dimensional arrays
            data_flat = data.flatten()
            
            # Compute histogram
            bin_edges, hist_counts, stats = compute_histogram(data_flat, bins=bins, var_name=var_name)
            
            if bin_edges is not None:
                # Get variable info
                var_info = get_variable_info(dataset, var_name)
                
                # Create output filename
                output_file = os.path.join(output_dir, f"{base_filename}_{var_name}_histogram.txt")
                
                # Write histogram to file
                write_histogram_to_text(bin_edges, hist_counts, stats, output_file, var_name, var_info)
                
                print(f"  Histogram saved to: {output_file}")
                print(f"  Valid data points: {stats['count']}")
                print(f"  Range: [{stats['min']:.6f}, {stats['max']:.6f}]")
                
                processed_vars += 1
            else:
                print(f"  Skipped - no valid data")
                
        except Exception as e:
            print(f"  Error processing {var_name}: {e}")
        
        print("-" * 30)
    
    # Close dataset
    dataset.close()
    
    print(f"Processing complete. {processed_vars} variables processed.")

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Generate histograms from EOS-06 satellite NetCDF data')
    parser.add_argument('input_file', help='Path to input .nc file')
    parser.add_argument('-o', '--output', help='Output directory (default: same as input file)')
    parser.add_argument('-b', '--bins', type=int, default=50, help='Number of histogram bins (default: 50)')
    parser.add_argument('-v', '--variables', nargs='+', help='Specific variables to process (default: all data variables)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    process_eos06_nc_file(
        filepath=args.input_file,
        output_dir=args.output,
        bins=args.bins,
        variables=args.variables
    )

if __name__ == "__main__":
    main()

# Example usage:
# python eos06_histogram.py data.nc
# python eos06_histogram.py data.nc -o histograms -b 100
# python eos06_histogram.py data.nc -v temperature humidity -b 75
