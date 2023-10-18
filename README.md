# **Linear programing**

# **Repository Installation**
Since full unprocessed datasets are too large to be stored in the repository, they are stored elsewhere
online and must be downloaded separately if you want full functionality of all the scripts. Most importantly
the FoodData Central database must be downloaded from [here](https://fdc.nal.usda.gov/download-datasets.html)
It can be done like so:

```bash
cd Data
wget https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2023-04-20.zip
unzip -d FoodData FoodData_Central_csv_2023-04-20.zip
```

## **Basic problem**
Let us minimize the amount of calories, thus creating a diet plan if we need to meet the following
conditions:  

* 70 g of fats
* 310 g of carbohydrates
* 50 g of proteins
* 1000 mg of calcium
* 18 mg of of iron

Additionally it must hold:

* Daily intake of food is < 2 kg
* 60 mg of vitamin C
* 3500 mg of potassium
* acceptable level of sodium (500 - 2400 mg)

## Possible ideas
* Create a diet for an alcoholic so maximize the amount of alcohol in the diet