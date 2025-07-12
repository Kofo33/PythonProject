import os
from ..utils.helpers import ensure_data_directory


def load_products() -> None:
    """
     Load products from all warehouse*.txt files in data directory.

     File format: name1:price1;name2:price2;...
     Assigns sequential IDs and default stock of 10 to each product.
     Skips empty files and malformed entries.
     """
    global products
    products = []
    ensure_data_directory()

    # Find all warehouse files
    warehouse_files = []
    for file in os.listdir('data'):
        if file.startswith('warehouse') and file.endswith('.txt'):
            warehouse_files.append(os.path.join('data', file))

    # Load products from each file
    product_id = 1
    for file_path in warehouse_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    continue

                items = content.split(';')
                for item in items:
                    if not item:
                        continue
                    try:
                        name, price = item.split(':')
                        products.append({
                            'id': product_id,
                            'name': name.strip(),
                            'price': float(price.strip()),
                            'stock': 10  # Default stock
                        })
                        product_id += 1
                    except ValueError:
                        continue
        except FileNotFoundError:
            continue