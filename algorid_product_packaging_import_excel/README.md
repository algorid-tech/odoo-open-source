# Product Packaging Import from Excel

Import product packaging from Excel files into Odoo with ease.

## Features

- **Excel Import**: Upload .xls or .xlsx files with packaging data
- **Template Download**: Generate pre-formatted Excel templates
- **Smart Buttons**: Quick access from product forms
- **Flexible Import Modes**: Create, update, or both
- **Product Filtering**: Import for specific products or templates
- **Comprehensive Validation**: Detailed error reporting
- **All Fields Supported**: Including routes, package types, barcodes

## Installation

1. Install Python dependencies:
```bash
pip install openpyxl xlrd
```

2. Copy the module to your Odoo addons directory

3. Update the apps list in Odoo

4. Install "Product Packaging Import from Excel"

## Usage

### Method 1: From Configuration Menu

1. Navigate to **Inventory > Configuration > Import Packaging**
2. Click **Download Excel Template**
3. Fill in your packaging data
4. Upload the file and click **Import**

### Method 2: From Product Form

1. Open any product template or product variant
2. Click the **Import Packaging** smart button
3. Download the template (pre-filled with product information)
4. Fill in your packaging data
5. Upload and import (automatically filtered to that product)

## Excel Template Format

### Required Fields
- **Product Code/ID**: Product default_code or database ID in brackets [123]
- **Packaging Name**: Name for the packaging
- **Contained Quantity**: Number of products in this packaging

### Optional Fields
- **Sequence**: Order number (lower = default)
- **Barcode**: Barcode for scanning
- **Package Type**: Package type name (must exist in system)
- **Sales**: Available for sales (TRUE/FALSE)
- **Purchase**: Available for purchase (TRUE/FALSE)
- **Routes**: Comma-separated route names

### Example Data

| Product Code/ID | Packaging Name | Sequence | Contained Quantity | Barcode | Package Type | Sales | Purchase | Routes |
|----------------|---------------|----------|-------------------|---------|-------------|-------|----------|--------|
| PROD001 | Box of 10 | 1 | 10 | 1234567890 | Box | TRUE | TRUE | Buy |
| PROD001 | Pallet of 100 | 2 | 100 | 0987654321 | Pallet | TRUE | FALSE | Buy,Manufacture |
| [123] | Case of 6 | 1 | 6 | | Case | TRUE | TRUE | |

## Import Modes

- **Create New Packaging**: Only creates new packaging records
- **Update Existing Packaging**: Only updates existing packaging (matches by product and name)
- **Create or Update**: Smart mode - creates new or updates existing

## Product Reference Formats

You can reference products in two ways:

1. **By Default Code**: `PROD001`
2. **By Database ID**: `[123]` (ID in brackets)

## Boolean Field Formats

Boolean fields accept multiple formats (case-insensitive):
- TRUE/FALSE
- YES/NO
- 1/0
- T/F
- Y/N

## Notes

- Barcodes are optional and must be unique
- Package types must exist in the system before import
- Routes must be marked as "packaging selectable"
- When using product filtering, only matching products will be imported
- Replace Existing option will delete all packaging before import

## Support

For issues or questions, please contact your Odoo administrator.

## License

LGPL-3

## Author

Algorid Limited
https://www.algorid.com
