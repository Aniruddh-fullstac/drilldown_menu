import pandas as pd

# Hot Coffee data
hot_coffee = {
    'Item Name': [
        'Espresso', 'South Indian', 'Double Restritto', 'Americano', 'Kaapicino',
        'Cafe Latte', 'Cappucino', 'Irish Americano', 'Bella\'tte', 'Flat white',
        'Cafe Mocha', 'Sea Salt Dark Mocha'
    ],
    'Product Description': [
        'The 30ml "Wake Me Up" Coffee Shot',
        'Bass Naam H Kaapi Hai',
        '44ml Extraction From 16gms Of Coffee',
        'Authentic Double Ristreto Served With Warm Water (A.K.A. Up All Night Recovery)',
        'Traditional Filter Coffee Decoction Served In A Classic Cappuccino Fashion',
        '"Looks Like Coffee With A Biased Milk To Milk Foam Ratio And Solid Coffee Composition',
        '"Safest Bet" Coffee With A Balanced Proportion Of Coffee, Milk And Silky Milk Foam',
        'Authentic Double Ristreto Served With Warm Water And Some Sweet Irish Syrup (A.K.A. Up All Night Recovery But Sweet)',
        'Cafe Latte Blended With Jaggery Sourced From Villages in Southern India (A.K.A. Jaggery Bomb)',
        'Just The Way Our Australian Friends Like It "More Milk Less Drama"',
        'Milk Coffee With Special Cocoa From Madagascar',
        'Milk Coffee With Special Cocoa From Madagascar Savoured With Konkan Coastal Sea Salt'
    ],
    'Price_250ml': [140, 140, 160, 185, 215, 225, 225, 225, 225, 230, 235, 275],
    'Price_350ml': [None, 185, None, 210, 240, 250, 250, 250, 250, None, 260, 300],
    'Image': ['default.jpg'] * 12,
    'Tags': [''] * 12
}

# Cold Coffee data
cold_coffee = {
    'Item Name': [
        'Iced Americano', 'Iced Latte', 'Classic Frappe', 'Hazulnut Frappe',
        'Almond Frappe', 'Nariyal Irish Cream Frappe', 'Original South India Frappe',
        'Pop Corn', 'Vietnamese', 'Madagascar Choco Chip Frappe', 'Matcha Frappe'
    ],
    'Product Description': [
        'With manual pour over, the coffee drains directly onto the cold water and ice',
        'A No Brainer To I\'m Thirsty And It\'s Hot',
        'Classic House Special Frappe Served With Twist Of Jaggery',
        'Coffee Frappe With Everyone\'s Favorite Hazelnut Flavour Notes',
        'Almond Milk Based "Lactose Free Beat The Heat Solution"',
        'Tender Coconut And Coffee Frappe Blended With Precision',
        'Traditional Filter Kaapi Frappe',
        'Coffee For The Little "Sweet Tooth", Served With Condensed Milk',
        'Traditional Filter Kaapi On A Bed Of Condensed Milk',
        'Premium Madagascar Chocolate Frappe With Chocolate Chips To Balance Textures',
        'Frappe Using Matcha Tea Decoction'
    ],
    'Price_350ml': [185, 225, 275, 305, 305, 305, 305, 305, 305, 335, 405],
    'Price_450ml': [210, 250, 320, 350, 350, 350, 350, 350, 350, 375, 450],
    'Image': ['default.jpg'] * 11,
    'Tags': [''] * 11
}

# Coffee Coolers data
coffee_coolers = {
    'Item Name': ['Espresso Tonic', 'Malnad Tonic'],
    'Product Description': [
        'Tonic Water/ Ginger Ale Espresso Sitting On A Bed Of Tonic Water/Ginger Ale Full Body Cousin To The Beverage On Your Mind',
        'Tonic Water/ginger Ale Cold Brewed South Indian Coffee Mixed With Tonic/Ginger Ale With A Finish Of Subtle Ginger Notes'
    ],
    'Price': [300, 300],
    'Image': ['default.jpg'] * 2,
    'Tags': [''] * 2
}

# Not Coffee data
not_coffee = {
    'Item Name': ['Hot Tea Latte', 'Madagascar Hot Chocolate', 'Matcha Latte'],
    'Product Description': [
        'Not In The Mood For Coffee But I Want My Daily Caffeine Intake Beverage',
        'Simply Dark Chocolate Beverage',
        '"Drink Your Tea" Matcha'
    ],
    'Price_250ml': [270, 300, 350],
    'Price_350ml': [320, 350, 400],
    'Image': ['default.jpg'] * 3,
    'Tags': [''] * 3
}

# Manual Brew data
manual_brew = {
    'Item Name': ['Pour Over', 'Aeropress', 'French Press', 'Cold Brew'],
    'Product Description': ['', '', '', ''],
    'Price': [250, 250, 250, 300],
    'Image': ['default.jpg'] * 4,
    'Tags': [''] * 4
}

# Create Excel file with multiple sheets
with pd.ExcelWriter('coffee_menu.xlsx', engine='openpyxl') as writer:
    pd.DataFrame(hot_coffee).to_excel(writer, sheet_name='Hot Coffee', index=False)
    pd.DataFrame(cold_coffee).to_excel(writer, sheet_name='Cold Coffee', index=False)
    pd.DataFrame(coffee_coolers).to_excel(writer, sheet_name='Coffee Coolers', index=False)
    pd.DataFrame(not_coffee).to_excel(writer, sheet_name='Not Coffee', index=False)
    pd.DataFrame(manual_brew).to_excel(writer, sheet_name='Manual Brew', index=False)

print("Excel file has been created successfully!") 