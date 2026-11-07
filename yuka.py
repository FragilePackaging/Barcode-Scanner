
import requests
import os

barcode = input("Enter barcode: ")

url = "https://api.nal.usda.gov/fdc/v1/foods/search"

parameters = {
    "api_key": os.getenv("USDA_API_KEY"),
    "query": barcode,
    "pageSize": 25
}

response = requests.get(url, params=parameters)

if response.status_code == 200:
    data = response.json()
    print("\nSuccess!")

    found = False

    for food in data["foods"]:
        if food.get("gtinUpc") == barcode:
            found = True

            print("\n========== PRODUCT INFORMATION ==========")
            print("Product:", food["description"])
            print("Food ID:", food["fdcId"])

            nutrients = {}

            for nutrient in food.get("foodNutrients", []):
                name = nutrient.get("nutrientName")
                amount = nutrient.get("value")
                unit = nutrient.get("unitName")

                if name:
                    nutrients[name.lower()] = (amount, unit)

            def get_nutrient(name):
                return nutrients.get(name.lower(), (0, ""))

            calories = get_nutrient("Energy")[0]
            protein = get_nutrient("Protein")[0]
            carbs = get_nutrient("Carbohydrate, by difference")[0]
            fat = get_nutrient("Total lipid (fat)")[0]
            sugar = get_nutrient("Sugars, Total")[0]
            sodium = get_nutrient("Sodium")[0]
            fiber = get_nutrient("Fiber, total dietary")[0]

            print("\n========== NUTRITION FACTS ==========")
            print(f"Calories: {calories} kcal")
            print(f"Protein: {protein} g")
            print(f"Carbohydrates: {carbs} g")
            print(f"Total Fat: {fat} g")
            print(f"Sugar: {sugar} g")
            print(f"Sodium: {sodium} mg")
            print(f"Fiber: {fiber} g")

            # Nutritional scoring system
            score = 10

            if calories > 500:
                score -= 2
            elif calories > 300:
                score -= 1

            if sugar > 20:
                score -= 2
            elif sugar > 10:
                score -= 1

            if sodium > 600:
                score -= 2
            elif sodium > 300:
                score -= 1

            if fat > 20:
                score -= 1

            if fiber >= 5:
                score += 1

            if protein >= 10:
                score += 1

            score = max(0, min(10, score))

            print("\n========== NUTRITIONAL RATING ==========")
            print(f"Rating: {score}/10")

            if score >= 8:
                print("Excellent nutritional profile!")
            elif score >= 6:
                print("Good nutritional profile.")
            elif score >= 4:
                print("Average nutritional profile.")
            else:
                print("Poor nutritional profile.")

            break

    if not found:
        print("Product not found. Try another barcode.")

else:
    print(f"Failed to get data. Error code: {response.status_code}")
