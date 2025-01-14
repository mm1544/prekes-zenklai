# Odoo Module: Custom Fields and Functionality for Sales Orders and Invoices

## Overview
This Odoo module introduces custom functionality for managing sales orders and invoices. The module adds new fields, enhances data flow between sales orders and invoices, and provides a detailed comment summary for invoice lines.

## Features

1. **New Many2many Field for Brands**
    - Adds a `Many2many` field named `Prekės Ženklai` (Brands) to sales order lines and invoice lines.
    - The `Many2many` field links to a newly created table for managing brand data.

2. **Data Synchronization**
    - Upon confirming a sales order, the selected brand information is automatically transferred to the corresponding invoice lines.

3. **Enhanced Invoice Comments**
    - Generates a detailed summary in the invoice comment field, listing product codes and their associated brands in the following format:
      ```
      Prekės kodas1 – (Prekės ženklas1, Prekės ženklas2, ...)
      Prekės kodas2 – (Prekės ženklas2, Prekės ženklas1, ...)
      ```

4. **Unit Tests**
    - Includes comprehensive unit tests to ensure functionality and data integrity. Tests cover:
      - Creation of sales orders and invoices with brand data.
      - Verification of data synchronization.
      - Validation of the invoice comment formatting.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

2. Add the module to your Odoo custom addons directory.

3. Update the Odoo apps list:
   ```bash
   ./odoo-bin -u all
   ```

4. Install the module via the Odoo Apps menu.

## Usage

1. **Adding Brand Information**
   - Navigate to Sales Orders.
   - Add or select brands in the `Prekės Ženklai` field for each order line.

2. **Confirming Sales Orders**
   - Confirm the sales order to automatically transfer brand data to the corresponding invoice lines.

3. **Viewing Invoice Comments**
   - Open the invoice to see the generated comment summarizing product codes and their associated brands.

## Configuration
No additional configuration is required. The module is ready to use upon installation.

## Technical Details

- **Models:**
  - New model for managing brands (`custom.brand`).
  - Extended models for `sale.order.line` and `account.move.line`.

- **Data Transfer:**
  - Implemented via Odoo ORM methods to ensure seamless synchronization.

- **Comment Generation:**
  - Built using custom methods to aggregate and format brand information.

- **Unit Tests:**
  - Located in the `tests` directory.
  - Can be executed using the following command:
    ```bash
    ./odoo-bin --test-enable -d <database_name>
    ```

## Bonus Points
The inclusion of unit tests adds robustness and reliability to the module, ensuring smooth operation and maintainability.

## License
This module is licensed under the MIT License. See `LICENSE` for more details.

---

For any issues or feature requests, please create a new issue in this repository.

