# GobusterBuster

GobusterBuster is a Python script designed to enhance the functionality of the Gobuster tool, which is commonly used for brute force attacks on web directories and DNS subdomains. This script automates the process, handles real-time output, and tracks progress efficiently.

## Features

- **Argument Parsing**: Collects command-line arguments for running the script.
- **Stream Processing**: Reads and processes real-time output from Gobuster.
- **Progress Tracking**: Monitors and prints the progress of the Gobuster scan.
- **Directory Discovery**: Identifies and stores discovered directories.
- **Spacebar Interaction**: Allows the user to print the current progress by pressing the spacebar.
- **Multithreading**: Uses threads to handle standard output and error streams concurrently.

## Prerequisites

- Python 3.x installed on your machine.
- Gobuster tool installed and available in your PATH.

## Installation

Ensure that the necessary Python libraries are installed. You can use `pip` to install the `keyboard` module:

```bash
pip install keyboard
```

## Usage

Save the `GobusterBuster.py` script to your local machine. Open a terminal and navigate to the directory where the script is located. Run the script with the appropriate arguments. For example:

```bash
python GobusterBuster.py -u http://example.com -w wordlist.txt
```

Replace `-u` and `-w` with the actual URL and wordlist file you want to use with Gobuster.

## Running the Script

The script will start Gobuster with the provided arguments. It will process the output in real-time, displaying discovered directories and progress. Press the spacebar at any time to print the current progress of the scan.

### Example Command

```bash
python GobusterBuster.py -u http://example.com -w /path/to/wordlist.txt
```

## Additional Information

- The script processes Gobuster's output to extract and store discovered directories.
- It uses regular expressions to identify directories in the output.
- The progress of the scan can be printed to the console by pressing the spacebar.
