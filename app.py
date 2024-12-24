from flask import Flask, render_template, jsonify, request, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_url(image_name):
    if not image_name or image_name == 'default.jpg':
        return url_for('static', filename='images/default.jpg')
    return url_for('static', filename=f'images/{image_name}')

def get_excel_sheets():
    excel_file = 'coffee_menu.xlsx'
    xls = pd.ExcelFile(excel_file, engine='openpyxl')
    return xls.sheet_names

def get_sheet_items(sheet_name):
    excel_file = 'coffee_menu.xlsx'
    df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
    items = []
    for _, row in df.iterrows():
        prices = {}
        if 'Price_250ml' in df.columns and not pd.isna(row.get('Price_250ml')):
            prices['250ml'] = row['Price_250ml']
        if 'Price_350ml' in df.columns and not pd.isna(row.get('Price_350ml')):
            prices['350ml'] = row['Price_350ml']
        if 'Price_450ml' in df.columns and not pd.isna(row.get('Price_450ml')):
            prices['450ml'] = row['Price_450ml']
        if 'Price' in df.columns and not pd.isna(row.get('Price')):
            prices['default'] = row['Price']

        image_name = row.get('Image', 'default.jpg')
        item = {
            'name': row['Item Name'],
            'description': row.get('Product Description', ''),
            'prices': prices,
            'image': get_image_url(image_name),
            'tags': row.get('Tags', '').split(',') if pd.notna(row.get('Tags')) else []
        }
        items.append(item)
    return items

def save_excel_file(updated_sheet_name, updated_df):
    """Helper function to save Excel file while preserving other sheets"""
    excel_file = 'coffee_menu.xlsx'
    
    try:
        # First read all existing sheets
        existing_data = {}
        xls = pd.ExcelFile(excel_file, engine='openpyxl')
        for sheet_name in xls.sheet_names:
            if sheet_name != updated_sheet_name:
                existing_data[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
        
        # Now create a new writer and write all sheets
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Write the updated sheet
            updated_df.to_excel(writer, sheet_name=updated_sheet_name, index=False)
            
            # Write all other sheets
            for sheet_name, df in existing_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
    except Exception as e:
        print(f"Error saving Excel file: {str(e)}")
        raise

@app.route('/')
def home():
    categories = get_excel_sheets()
    return render_template('index.html', categories=categories)

@app.route('/category/<sheet_name>')
def category(sheet_name):
    items = get_sheet_items(sheet_name)
    return render_template('category.html', items=items, category_name=sheet_name)

@app.route('/admin')
def admin():
    categories = get_excel_sheets()
    return render_template('admin.html', categories=categories)

@app.route('/get_category_fields/<category>')
def get_category_fields(category):
    df = pd.read_excel('coffee_menu.xlsx', sheet_name=category, engine='openpyxl')
    fields = df.columns.tolist()
    return jsonify(fields)

@app.route('/get_category_items/<category>')
def get_category_items(category):
    df = pd.read_excel('coffee_menu.xlsx', sheet_name=category, engine='openpyxl')
    items = df['Item Name'].tolist()
    return jsonify(items)

@app.route('/get_item_details/<category>/<item_name>')
def get_item_details(category, item_name):
    try:
        df = pd.read_excel('coffee_menu.xlsx', sheet_name=category, engine='openpyxl')
        item = df[df['Item Name'] == item_name].iloc[0]
        details = {}
        for column in df.columns:
            value = item[column]
            if pd.isna(value):
                value = ''
            elif isinstance(value, (int, float)):
                value = str(int(value)) if value.is_integer() else str(value)
            else:
                value = str(value)
            if column == 'Image':
                details['image_url'] = get_image_url(value)
            details[column] = value
        return jsonify(details)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/add_item', methods=['POST'])
def add_item():
    try:
        category = request.form.get('category')
        if not category:
            return jsonify({'success': False, 'message': 'Category is required'})

        # Read the Excel file to get the structure
        df = pd.read_excel('coffee_menu.xlsx', sheet_name=category, engine='openpyxl')
        
        # Get the column names from the existing sheet
        columns = df.columns.tolist()
        
        # Create new item dictionary
        new_item = {}
        
        # Process form data
        for column in columns:
            column_lower = column.lower()
            if column_lower in request.form:
                # Handle numeric fields
                if 'price' in column_lower:
                    try:
                        new_item[column] = float(request.form[column_lower])
                    except ValueError:
                        new_item[column] = None
                else:
                    new_item[column] = request.form[column_lower]
            else:
                new_item[column] = None  # or '' depending on your needs
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    new_item['Image'] = filename
                else:
                    return jsonify({'success': False, 'message': 'Invalid image format. Allowed formats are: ' + ', '.join(ALLOWED_EXTENSIONS)})
            else:
                new_item['Image'] = 'default.jpg'
        else:
            new_item['Image'] = 'default.jpg'

        # Create a new single-row DataFrame with the same structure as the original
        new_row_df = pd.DataFrame([new_item], columns=columns)
        
        # Concatenate with the existing DataFrame
        updated_df = pd.concat([df, new_row_df], ignore_index=True)
        
        # Save the updated DataFrame
        save_excel_file(category, updated_df)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error adding item: {str(e)}")  # Debug print
        return jsonify({'success': False, 'message': str(e)})

@app.route('/update_item', methods=['POST'])
def update_item():
    try:
        category = request.form.get('category')
        item_name = request.form.get('item')
        if not category or not item_name:
            return jsonify({'success': False, 'message': 'Category and item name are required'})

        try:
            df = pd.read_excel('coffee_menu.xlsx', sheet_name=category, engine='openpyxl')
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error reading Excel file: {str(e)}'})

        mask = df['Item Name'] == item_name
        if not mask.any():
            return jsonify({'success': False, 'message': 'Item not found'})
        
        item_idx = mask.idxmax()
        
        updated_data = {}
        for field in df.columns:
            field_lower = field.lower()
            if field_lower in request.form and request.form[field_lower]:
                updated_data[field] = request.form[field_lower]
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    updated_data['Image'] = filename
                else:
                    return jsonify({'success': False, 'message': 'Invalid image format. Allowed formats are: ' + ', '.join(ALLOWED_EXTENSIONS)})
        
        for field, value in updated_data.items():
            df.at[item_idx, field] = value

        try:
            save_excel_file(category, df)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error saving Excel file: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_item', methods=['POST'])
def delete_item():
    try:
        category = request.form['category']
        item_name = request.form['item']
        df = pd.read_excel('coffee_menu.xlsx', sheet_name=category, engine='openpyxl')
        
        df = df[df['Item Name'] != item_name]
        save_excel_file(category, df)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True) 