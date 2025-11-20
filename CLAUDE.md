# TargetID - Codebase Documentation for AI Assistants

## Project Overview

**TargetID** is a bioinformatics project focused on protein target identification and surface protein analysis. The repository integrates proteomics data processing with UniProt database mapping to identify and validate surface protein candidates.

### Primary Components

1. **SurfaceGenie** - R Shiny web application for surface protein analysis
2. **UniProt ID Mapping** - Python-based verification and ID mapping utilities
3. **Surfaceome Reference Data** - Curated datasets of surface proteins

## Repository Structure

```
TargetID/
├── data/
│   ├── SurfaceGenie/          # R Shiny application
│   │   ├── ui.R               # UI definition
│   │   ├── server.R           # Server logic
│   │   ├── functions.R        # Core analysis functions
│   │   ├── ref/               # Reference data files
│   │   │   ├── SPC_by_Source_sprot.csv
│   │   │   ├── Mouse_SPC.csv
│   │   │   ├── Rat_SPC.csv
│   │   │   ├── annotation.*.tsv
│   │   │   └── example_data.csv
│   │   ├── Text/              # Documentation (DOCX files)
│   │   ├── Test Data/         # Test datasets
│   │   └── www/               # Web assets
│   └── surfaceome/
│       ├── surfaceome_ids.txt         # ~2800 surface protein IDs
│       └── table_S3_surfaceome.xlsx   # Comprehensive surfaceome data
├── surface-genie-verify.py    # UniProt ID mapping verification
├── uniprot_id_mapping.yaml    # Cached UniProt API responses (~330KB)
├── output                      # API response output (1MB)
└── .gitignore                  # venv excluded
```

## Technology Stack

### Languages & Frameworks
- **Python 3.11.14** - Backend utilities and API integration
- **R** - Data analysis and Shiny web application
- **Shiny** - Interactive web interface for proteomics analysis

### Key Python Dependencies
```python
requests    # UniProt API communication
yaml        # Configuration and data serialization
pprint      # Debugging and output formatting
```

### Key R Dependencies
```r
shiny       # Web application framework
plotly      # Interactive visualizations
plyr        # Data manipulation
stringr     # String processing
gplots      # Plotting utilities
RColorBrewer # Color palettes
xlsx        # Excel file I/O
svglite     # SVG graphics export
```

## Core Functionality

### 1. SurfaceGenie Analysis Pipeline

**Purpose**: Analyze and score proteins for cell surface localization based on abundance data.

**Key Metrics**:
- **Gini Coefficient** - Measures distribution specificity across samples
- **Signal Strength** - Log-transformed maximum abundance
- **Genie Score (GS)** - Combined metric for surface protein likelihood
- **OmniGenie Score** - Incorporates Surface Protein Confidence (SPC)

**Processing Options**:
- Multi-sample grouping (up to 5 groups)
- Aggregation methods: average or median
- HLA molecule exclusion
- SPC-based filtering
- Species-specific annotations (human, mouse, rat)

**Input Format**:
- CSV, TSV, TXT, XLSX, XLS files
- First column MUST be named "Accession" (UniProt accession IDs)
- Subsequent columns: numeric abundance values
- Supports isoform notation (e.g., P02730-1)

**Output**:
- Processed data with scores
- Interactive plots via Plotly
- CSV export with customizable columns
- UniProt linkouts for each protein

### 2. UniProt ID Mapping (`surface-genie-verify.py`)

**Purpose**: Validate and map protein identifiers using UniProt REST API.

**Functions**:

#### `get_UniProt_ID(swissprot_ids)`
- Converts UniProtKB accession/IDs to canonical Swiss-Prot entries
- Uses UniProt ID mapping service
- Filters out isoform-specific entries (contains '-')
- Returns primary accession for reviewed entries

**API Workflow**:
```python
1. POST to /idmapping/run with identifier list
2. Receive jobId
3. Poll /idmapping/status/{jobId} until complete
4. Parse results to extract primary accession
```

#### `get_uniprot_data(entry)`
- Fetches raw UniProt entry in text format
- URL: https://www.uniprot.org/uniprot/{entry}.txt

**Key Implementation Details**:
- Handles both single IDs and lists
- Async job polling (waits for FINISHED status)
- Returns first non-isoform primary accession
- Example usage: `get_UniProt_ID("B3AT_HUMAN")` → `"P02730"`

### 3. Data Files

#### `surfaceome_ids.txt`
- Curated list of surface protein UniProt IDs
- Format: One ID per line (e.g., "1A01_HUMAN", "B3AT_HUMAN")
- ~2800 entries representing the human surfaceome

#### `uniprot_id_mapping.yaml`
- Cached UniProt API responses (~330KB)
- Contains full protein annotations including:
  - Primary accession IDs
  - Gene names and synonyms
  - Isoform information
  - Annotation scores
  - Taxonomic lineage
  - Alternative splicing data

#### SurfaceGenie Reference Files
- **SPC_by_Source_sprot.csv**: Surface Protein Confidence scores
- **annotation.*.tsv**: Species-specific protein annotations
- **Mouse_SPC.csv / Rat_SPC.csv**: Species-specific SPC scores
- **example_data.csv**: Sample dataset for testing

## Development Workflows

### Setting Up Environment

#### Python Environment
```bash
# Create virtual environment (already in .gitignore)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install requests pyyaml
```

#### R Environment
```r
# Install required packages
install.packages(c("shiny", "plotly", "plyr", "stringr",
                   "gplots", "RColorBrewer", "xlsx", "svglite"))
```

### Running SurfaceGenie Locally
```r
# From data/SurfaceGenie/ directory
library(shiny)
runApp()
```

### Testing UniProt Mapping
```bash
# Run verification script
python surface-genie-verify.py

# Expected output: UniProt ID (e.g., "P02730")
```

### Working with the Repository

#### Git Branch Strategy
- Main branch: Production-ready code
- Feature branches: `claude/*` prefix for AI-assisted development
- Current branch: `claude/claude-md-mi6v76z2xuhdq70s-01M6wdMmAyzYp1YHxvB1TstU`

#### Commit Guidelines
```bash
# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "Brief summary of changes

Detailed explanation if needed"

# Push to feature branch
git push -u origin <branch-name>
```

## Key Conventions for AI Assistants

### Code Style

#### Python
- Follow PEP 8 style guidelines
- Use descriptive variable names (e.g., `swissprot_ids`, `primary_accession`)
- Add comments for complex API interactions
- Handle API errors gracefully (network failures, rate limits)

#### R
- Use camelCase for function names (e.g., `get_Gini_coeff`, `group_samples`)
- Prefix internal functions with descriptive comments
- Use meaningful variable names (e.g., `nsamps` for number of samples)
- Document reactive expressions in Shiny apps

### Data Handling

#### Protein Identifiers
- **Accession IDs**: Primary format (e.g., "P02730")
- **Entry Names**: Secondary format (e.g., "B3AT_HUMAN")
- **Isoforms**: Hyphen notation (e.g., "P02730-1", "P02730-2")
- Always strip isoform suffixes when mapping to canonical IDs

#### File Formats
- **CSV**: Comma-delimited, header row required
- **TSV/TXT/TAB**: Tab-delimited
- **XLSX/XLS**: Excel format (uses `xlsx` package)
- **YAML**: Configuration and cached data

### API Usage

#### UniProt REST API
- Base URL: `https://rest.uniprot.org`
- Rate limiting: Be respectful, implement backoff if needed
- Caching: Store responses in `uniprot_id_mapping.yaml` to minimize requests
- Timeout handling: Poll status endpoint until job completes

#### Data Validation
- Check for required columns (e.g., "Accession" in first column)
- Validate numeric data types for abundance values
- Detect and warn about duplicates
- Handle missing values (NA) appropriately

### Error Handling

#### Common Issues

1. **File Upload Errors**
   - Wrong delimiter (comma vs tab)
   - Missing "Accession" column
   - Non-numeric abundance values
   - Single column data (delimiter mismatch)

2. **UniProt API Errors**
   - Network timeouts
   - Invalid job IDs
   - Empty result sets
   - Rate limiting (429 status)

3. **Data Processing Errors**
   - Duplicate accession IDs
   - Missing SPC scores (default to 0)
   - Invalid grouping column specifications

### Testing Strategy

#### Unit Testing
- Test ID mapping with known proteins (e.g., "B3AT_HUMAN" → "P02730")
- Validate Gini coefficient calculations
- Check signal strength formulas
- Verify isoform stripping logic

#### Integration Testing
- Upload example data files
- Process through full SurfaceGenie pipeline
- Verify output CSV structure
- Check plot generation

#### Data Validation
- Compare against `example_data.csv`
- Validate against known surfaceome entries
- Cross-reference with UniProt database

## Project-Specific Notes

### SurfaceGenie Scoring Algorithm

```r
# Gini Coefficient (0-1, higher = more specific)
Gini = sum(|xi - xj|) / (2 * n * sum(x))

# Signal Strength (log scale)
SS = log10(max(abundance) + 1)

# Genie Score (combines specificity and strength)
GS = (Gini / Gmax) * SS

# OmniGenie (incorporates SPC)
OmniGenie = GS * SPC
```

### Species Support
- **Human**: Default, most comprehensive annotations
- **Mouse**: Separate SPC and annotation files
- **Rat**: Separate SPC and annotation files

### Performance Considerations
- Large datasets (>3000 proteins): ~3-14 seconds processing time
- Annotation merge is the most time-intensive step
- Vectorized operations preferred over row-by-row iteration
- Progress bars implemented for long operations

### Data Sources
- **UniProt**: Protein sequence and functional information
- **SurfaceGenie Reference**: Curated surface protein confidence scores
- **Surfaceome**: Literature-derived surface protein catalog

## Maintenance & Updates

### Updating Reference Data

#### UniProt Data
```bash
# Re-run mapping for updated annotations
python surface-genie-verify.py

# Update cached YAML file
# Note: uniprot_id_mapping.yaml may grow large over time
```

#### SPC Scores
- Check for new releases from SurfaceGenie authors
- Update `ref/SPC_by_Source_sprot.csv` and species-specific files
- Verify compatibility with existing pipeline

#### Surfaceome Data
- Monitor literature for updated surfaceome catalogs
- Update `surfaceome_ids.txt` with new entries
- Refresh `table_S3_surfaceome.xlsx` as needed

### Version History
- **SurfaceGenie v0.2**: Current version in repository
- **SurfaceGenie v0.4**: Project file exists, may be newer version
- Changes between versions documented in README

## Common Tasks for AI Assistants

### Adding New Protein IDs
1. Add UniProt entry names to `data/surfaceome/surfaceome_ids.txt`
2. Run verification script to validate IDs
3. Update cached mapping file if needed

### Extending Species Support
1. Obtain species-specific SPC scores
2. Create `ref/{Species}_SPC.csv`
3. Create `ref/annotation.{species}.tsv`
4. Update `get_SPC()` function in `functions.R`
5. Add species option to UI

### Debugging API Issues
1. Check `output` file for raw API responses
2. Verify `jobId` is being returned correctly
3. Check `uniprot_id_mapping.yaml` for cached data
4. Test with known good IDs (e.g., "B3AT_HUMAN")

### Optimizing Performance
1. Use vectorized R operations
2. Cache UniProt API responses
3. Pre-filter data before annotation merge
4. Consider parallel processing for large datasets

## Security & Best Practices

### API Keys
- UniProt API is public, no authentication required
- Be respectful of rate limits
- Cache responses to minimize requests

### Data Privacy
- No user data is stored server-side (Shiny app)
- Uploaded files processed in-memory
- No logging of sensitive information

### Input Validation
- Always validate file extensions
- Check data types before processing
- Sanitize accession IDs (no code injection risk, but validate format)
- Prevent excessively large file uploads

## Additional Resources

### Documentation
- SurfaceGenie instructions: `data/SurfaceGenie/Text/SurfaceGenie Instructions.docx`
- SPC Lookup instructions: `data/SurfaceGenie/Text/SPC Lookup Instructions.docx`
- Home documentation: `data/SurfaceGenie/Text/Home.docx`

### External Links
- UniProt REST API: https://www.uniprot.org/help/api
- UniProt ID Mapping: https://www.uniprot.org/help/id_mapping
- Shiny Documentation: https://shiny.rstudio.com/

### Contact
- Authors: Matthew Waas, Shana Snarrenberg, Dr. Rebekah Gundry

## Troubleshooting Guide

### Issue: "Wrong file extension" error
- **Solution**: Ensure file is CSV, TSV, TXT, XLSX, or XLS format

### Issue: "Only one column of data" error
- **Solution**: Check delimiter matches file format (comma vs tab)

### Issue: First column must be "Accession"
- **Solution**: Rename first column header to exactly "Accession"

### Issue: Non-numeric abundance values
- **Solution**: Remove text/special characters from data columns

### Issue: UniProt API timeout
- **Solution**: Check network connection, retry with exponential backoff

### Issue: Missing SPC scores
- **Solution**: SPC defaults to 0 for unknown proteins (expected behavior)

---

**Last Updated**: 2025-11-20
**Repository**: TargetID
**Purpose**: Protein target identification and surface proteome analysis
