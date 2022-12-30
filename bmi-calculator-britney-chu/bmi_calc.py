def user_input():
    x = input("Enter weight with units (kg or lb): ")
    weight = float(x.split()[0])
    weightUnits = x.split()[1]
    y = input("Enter height with units (m or in): ")
    height = float(y.split()[0])
    heightUnits = y.split()[1]
    return (weight, weightUnits,height, heightUnits)
def convertUnits(weight, weightUnits, height, heightUnits):
    #BMI = kg / m^2
    if weightUnits == "lb":
        weight = 0.453592 * weight
    if heightUnits == "in":
        height = 0.0254 * height
    return (weight, height)
def calculateBMI(weight, height):
    bmi = weight / (height**2)
    return bmi
def classify_bmi(bmi):
    if bmi < 18.5:
        return "underweight"
    if bmi <= 24.9:
        return "normal weight"
    if bmi <= 29.9:
        return "overweight"
    else:
        return "obese"

if __name__ == "__main__":
    (weight, weightUnits, height, heightUnits) = user_input()
    (weight, height) = convertUnits(weight, weightUnits, height, heightUnits)
    bmi = calculateBMI(weight, height)
    print("Calculated BMI: {:.1f}".format(bmi))
    classification = classify_bmi(bmi)
    print("This BMI is classified as " + classification)

