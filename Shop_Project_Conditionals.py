products = {
    'Lotion'.upper(): 1500,
    'Biscuit'.upper(): 300,
    'Hair Cream'.upper(): 500,
    'Sweets'.upper(): 100
}
b = products.update({
    'Nivea'.upper(): 1500,
    'Torch'.upper(): 300,
    'Clippers'.upper(): 5000,
    'Oil'.upper(): 90000
})
#print(a)
stock = {
    'Lotion'.upper(): 15,
    'Biscuit'.upper(): 30,
    'Hair Cream'.upper(): 50,
    'Sweets'.upper(): 10
}
stock_update = stock.update({
    'Nivea'.upper(): 15,
    'Torch'.upper(): 30,
    'Clippers'.upper(): 50,
    'Oil'.upper(): 10
})
c = list(products.keys())[5]

# print(c)
Num_of_purchases = 0
Quantity_bought = 1

if Num_of_purchases <= stock['TORCH']:
    Quantity_bought += 1
    Num_of_purchases += 1
    if 'TORCH' in c:
        if Quantity_bought > stock['TORCH']:
            o = list(stock.keys())[5]
            print(f'Sorry, we are out of stock for {o}')
        else:  # You may proceed to purchase LOTION
            cost = products['TORCH'] * Quantity_bought
            print(f'{c} = {cost}')
