# Happy Home Helper
Our best model encorporates these columns: bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'grade',
'sqft_above', 'sqft_living15', 'sqft_lot15', 'age', 'months_ago_sold';
one hot encoded zip code; and these columns made from multiplying other top correlated models: 'sqft_living&above',
'sqft_living&grade', 'sqft_living&living15', 'grade&sqft_above', 'bathrooms&sqft_living', 'sqft_above&sqft_living15',
'grade&sqft_living15'