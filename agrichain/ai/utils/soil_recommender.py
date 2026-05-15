SOIL_TYPES = [
    "Sandy",
    "Clay",
    "Loamy",
    "Silt",
    "Peaty",
    "Lateritic"
]

FERTILIZATION_METHODS = [
    "Organic (compost, manure)",
    "Inorganic (NPK, Urea)",
    "Mixed (both organic and inorganic)",
    "None"
]

SOIL_DESCRIPTIONS = {
    "Sandy": "Well-draining, warms up quickly, low nutrient retention",
    "Clay": "Heavy soil, rich in nutrients, poor drainage, good for paddy",
    "Loamy": "Ideal balanced soil with good drainage and nutrients",
    "Silt": "Smooth texture, moderate drainage, fertile",
    "Peaty": "High organic matter, acidic, good moisture retention",
    "Lateritic": "Iron-rich, common in tropical Nigeria, needs organic enrichment"
}

FERTILIZER_RECOMMENDATIONS = {
    "Sandy": {
        "Organic (compost, manure)": "Continue using organic matter. Add more compost and well-rotted manure to improve water retention. Consider green manure cover crops.",
        "Inorganic (NPK, Urea)": "Use split application of NPK 15-15-15 at 200kg/ha. Apply Urea in 2-3 splits to prevent leaching. Add micronutrients like Zinc.",
        "Mixed (both organic and inorganic)": "Good approach. Apply 5-10 tons/ha of compost before planting, then supplement with NPK 15-15-15 at 150kg/ha during growth.",
        "None": "Start with 5-10 tons/ha of compost or poultry manure. Follow with NPK 15-15-15 at 200kg/ha split into two applications."
    },
    "Clay": {
        "Organic (compost, manure)": "Organic matter helps improve drainage. Use well-decomposed compost. Avoid fresh manure which can waterlog.",
        "Inorganic (NPK, Urea)": "Apply NPK 15-15-15 at 150kg/ha. Use single application as clay retains nutrients well. Avoid excess Nitrogen.",
        "Mixed (both organic and inorganic)": "Apply 3-5 tons/ha compost + NPK 15-15-15 at 100kg/ha. Clay retains nutrients so lower rates work.",
        "None": "Apply 3-5 tons/ha of organic matter to improve structure. Add NPK 15-15-15 at 150kg/ha. Consider raised beds for drainage."
    },
    "Loamy": {
        "Organic (compost, manure)": "Maintain soil health with 3-5 tons/ha of compost per season. Rotate with leguminous cover crops.",
        "Inorganic (NPK, Urea)": "Apply NPK 15-15-15 at 200kg/ha as basal. Top-dress with Urea at 100kg/ha 4 weeks after planting.",
        "Mixed (both organic and inorganic)": "Ideal. Apply 3 tons/ha compost + NPK 15-15-15 at 150kg/ha. This maintains long-term fertility.",
        "None": "Apply NPK 15-15-15 at 200kg/ha and Urea at 100kg/ha. Incorporate compost (3 tons/ha) for best results."
    },
    "Silt": {
        "Organic (compost, manure)": "Organic matter helps bind silt particles. Use 4-6 tons/ha of compost annually.",
        "Inorganic (NPK, Urea)": "Apply NPK 15-15-15 at 180kg/ha. Silt soils are prone to erosion so avoid over-tilling.",
        "Mixed (both organic and inorganic)": "Apply 4 tons/ha compost + NPK 15-15-15 at 120kg/ha. Good for sustained yields.",
        "None": "Apply 4-6 tons/ha of organic matter. Supplement with NPK 15-15-15 at 180kg/ha split into two doses."
    },
    "Peaty": {
        "Organic (compost, manure)": "Peaty soil is already high in organic matter. Use well-composted material. Avoid fresh organic additions.",
        "Inorganic (NPK, Urea)": "Apply phosphorus (SSP at 100kg/ha) and potassium (MOP at 80kg/ha). Peaty soils are often P and K deficient.",
        "Mixed (both organic and inorganic)": "Limit organic additions. Focus on NPK with emphasis on P and K. Apply SSP 80kg/ha + MOP 60kg/ha.",
        "None": "Apply SSP (single superphosphate) at 100kg/ha and MOP (muriate of potash) at 80kg/ha. Lime may be needed to reduce acidity."
    },
    "Lateritic": {
        "Organic (compost, manure)": "Essential. Lateritic soils need high organic matter. Apply 8-10 tons/ha of compost or poultry manure annually.",
        "Inorganic (NPK, Urea)": "Use NPK 15-15-15 at 200kg/ha. Lateritic soils fix phosphorus, so apply phosphate fertilizers regularly.",
        "Mixed (both organic and inorganic)": "Best approach. Apply 5 tons/ha poultry manure + NPK 15-15-15 at 150kg/ha. Rock phosphate at 50kg/ha helps.",
        "None": "Apply 8-10 tons/ha of organic matter plus NPK 15-15-15 at 200kg/ha. Add rock phosphate at 50kg/ha for phosphorus."
    }
}

CROP_SPECIFIC_ADVICE = {
    "Rice": {
        "Sandy": "Sandy soil is not ideal for rice. Use heavy clay or loamy soil. If sandy is your only option, add lots of clay and organic matter. Use NPK 20-10-10.",
        "Clay": "Excellent for paddy rice. Clay retains water well. Apply NPK 20-10-10 at 200kg/ha. Top-dress with Urea at 100kg/ha during tillering.",
        "Loamy": "Good for rice. Maintain 5cm standing water. Apply NPK 20-10-10 at 150kg/ha. Add Zinc sulfate at 25kg/ha for better yield.",
        "Silt": "Good for rice with proper water management. Apply NPK 20-10-10 at 170kg/ha. Ensure bunds are well-maintained.",
        "Peaty": "Acidic for rice. Apply lime at 2 tons/ha first. Then NPK 15-15-15 at 200kg/ha. Monitor for iron toxicity.",
        "Lateritic": "Challenging for rice. Need heavy organic matter (10 tons/ha). Use NPK 15-15-15 at 200kg/ha. Consider raised beds."
    },
    "Maize": {
        "Sandy": "Apply NPK 15-15-15 at 250kg/ha at planting. Top-dress with Urea at 150kg/ha 5 weeks after planting. Use split nitrogen application.",
        "Clay": "Apply NPK 15-15-15 at 150kg/ha at planting. Top-dress with Urea at 100kg/ha at 5 weeks. Good for maize if well-drained.",
        "Loamy": "Ideal for maize. Apply NPK 15-15-15 at 200kg/ha + Urea 100kg/ha. Side-dress nitrogen at V6 and V12 stages.",
        "Silt": "Good for maize. Apply NPK 15-15-15 at 180kg/ha. Top-dress with Urea at 120kg/ha. Watch for erosion.",
        "Peaty": "High acidity may limit maize. Apply lime 1-2 tons/ha. Use NPK 15-15-15 at 200kg/ha plus Zinc and Boron.",
        "Lateritic": "Common in Nigeria. Apply 10 tons/ha poultry manure + NPK 15-15-15 at 250kg/ha. Phosphorus fixation is a concern."
    },
    "Cassava": {
        "Sandy": "Good for cassava. Apply NPK 12-12-17 at 200kg/ha. Add KCl (potassium) at 100kg/ha for tuber development.",
        "Clay": "Use raised beds for drainage. Apply NPK 12-12-17 at 150kg/ha. High potassium is essential for cassava.",
        "Loamy": "Excellent. Apply NPK 12-12-17 at 200kg/ha + KCl 80kg/ha. Harvest at 12 months for best yields.",
        "Silt": "Good. Apply NPK 12-12-17 at 180kg/ha. Ensure good drainage. Add organic matter for soil structure.",
        "Peaty": "Reduce acidity with lime. Apply NPK 12-12-17 at 200kg/ha. Watch for root rot in wet conditions.",
        "Lateritic": "Apply 8 tons/ha organic matter + NPK 12-12-17 at 250kg/ha. Potassium is critical for tuber formation."
    },
    "Yam": {
        "Sandy": "Good for early yam but needs high organic matter. Apply NPK 10-10-20 at 250kg/ha. Use mounds or ridges.",
        "Clay": "Use raised mounds for drainage. Apply NPK 10-10-20 at 200kg/ha. Clay helps hold moisture for yam.",
        "Loamy": "Ideal. Apply NPK 10-10-20 at 220kg/ha + 5 tons/ha compost. Potassium is key for tuber quality.",
        "Silt": "Good. Apply NPK 10-10-20 at 200kg/ha. Ensure mounds are high enough for good drainage.",
        "Peaty": "Lime to reduce acidity. Apply NPK 10-10-20 at 250kg/ha. Organic matter is already high.",
        "Lateritic": "Apply 10 tons/ha poultry manure + NPK 10-10-20 at 250kg/ha. Use large mounds for best tuber development."
    }
}

for crop in ["Sorghum", "Millet", "Groundnut", "Soybean", "Beans", "Cowpea",
             "Tomato", "Onion", "Pepper", "Okra", "Eggplant", "Lettuce",
             "Cucumber", "Watermelon", "Mango", "Coconut", "Cocoyam"]:
    CROP_SPECIFIC_ADVICE[crop] = {
        "Sandy": "Apply 5-8 tons/ha of organic matter. Use NPK 15-15-15 at 200kg/ha. Water management is critical.",
        "Clay": "Ensure good drainage. Apply NPK 15-15-15 at 150kg/ha. Use raised beds if needed.",
        "Loamy": "Apply NPK 15-15-15 at 180kg/ha + 3 tons/ha compost. Maintain regular irrigation schedule.",
        "Silt": "Apply NPK 15-15-15 at 170kg/ha. Good soil for this crop with standard management.",
        "Peaty": "Apply lime 1-2 tons/ha to reduce acidity. Use NPK 15-15-15 at 200kg/ha with micronutrients.",
        "Lateritic": "Apply 8 tons/ha poultry manure + NPK 15-15-15 at 200kg/ha. Address phosphorus fixation."
    }

CROP_SPECIFIC_ADVICE["Sorghum"]["Sandy"] = "Good for sandy soil. Apply NPK 15-15-15 at 150kg/ha. Sorghum is drought-tolerant."
CROP_SPECIFIC_ADVICE["Sorghum"]["Clay"] = "Apply NPK 15-15-15 at 120kg/ha. Sorghum tolerates clay but avoid waterlogging."
CROP_SPECIFIC_ADVICE["Sorghum"]["Loamy"] = "Ideal. Apply NPK 15-15-15 at 150kg/ha + Urea 80kg/ha top-dress."
CROP_SPECIFIC_ADVICE["Sorghum"]["Lateritic"] = "Apply 5 tons/ha organic matter + NPK 15-15-15 at 150kg/ha."

CROP_SPECIFIC_ADVICE["Millet"]["Sandy"] = "Ideal for sandy soil. Apply NPK 15-15-15 at 120kg/ha. Millet thrives in sandy conditions."
CROP_SPECIFIC_ADVICE["Millet"]["Loamy"] = "Good. Apply NPK 15-15-15 at 120kg/ha. Millet needs less fertilizer than maize."

CROP_SPECIFIC_ADVICE["Groundnut"]["Sandy"] = "Ideal for groundnut. Apply SSP at 100kg/ha + MOP at 50kg/ha. Avoid excess nitrogen."
CROP_SPECIFIC_ADVICE["Groundnut"]["Loamy"] = "Good. Apply SSP at 80kg/ha. Groundnut fixes its own nitrogen."
CROP_SPECIFIC_ADVICE["Groundnut"]["Lateritic"] = "Apply SSP at 150kg/ha + 5 tons/ha compost. Lime if pH below 5.5."

CROP_SPECIFIC_ADVICE["Soybean"]["Loamy"] = "Apply SSP at 100kg/ha + MOP at 60kg/ha. Inoculate with rhizobium for nitrogen fixation."
CROP_SPECIFIC_ADVICE["Soybean"]["Sandy"] = "Apply SSP at 120kg/ha + MOP at 80kg/ha. Add organic matter for water retention."

CROP_SPECIFIC_ADVICE["Tomato"]["Sandy"] = "Apply NPK 15-15-15 at 300kg/ha. Frequent irrigation needed. Add calcium to prevent blossom end rot."
CROP_SPECIFIC_ADVICE["Tomato"]["Loamy"] = "Ideal. Apply NPK 15-15-15 at 250kg/ha + 5 tons/ha compost. Support with stakes."

CROP_SPECIFIC_ADVICE["Okra"]["Sandy"] = "Apply NPK 15-15-15 at 200kg/ha. Okra needs consistent moisture."
CROP_SPECIFIC_ADVICE["Okra"]["Loamy"] = "Apply NPK 15-15-15 at 180kg/ha. Good yields with proper management."

CROP_SPECIFIC_ADVICE["Pepper"]["Sandy"] = "Apply NPK 15-15-15 at 250kg/ha + organic mulch to retain moisture."
CROP_SPECIFIC_ADVICE["Pepper"]["Loamy"] = "Apply NPK 15-15-15 at 200kg/ha + 3 tons/ha compost."

CROP_SPECIFIC_ADVICE["Onion"]["Sandy"] = "Apply NPK 15-15-15 at 250kg/ha. Onions need consistent moisture and sulfur."
CROP_SPECIFIC_ADVICE["Onion"]["Loamy"] = "Apply NPK 15-15-15 at 200kg/ha + sulfur at 20kg/ha."

CROP_SPECIFIC_ADVICE["Cocoyam"]["Lateritic"] = "Good for cocoyam. Apply NPK 10-10-20 at 200kg/ha + 8 tons/ha organic matter."
CROP_SPECIFIC_ADVICE["Cocoyam"]["Clay"] = "Use raised beds. Apply NPK 10-10-20 at 150kg/ha."
CROP_SPECIFIC_ADVICE["Cocoyam"]["Loamy"] = "Apply NPK 10-10-20 at 180kg/ha. Maintain consistent moisture."


def get_soil_recommendation(soil_type: str, fertilization_method: str, crop: str) -> str:
    soil_type = soil_type.title() if soil_type.title() in SOIL_TYPES else "Loamy"
    fert_key = None
    for fm in FERTILIZATION_METHODS:
        if fm.lower().startswith(fertilization_method.lower()):
            fert_key = fm
            break
    if not fert_key:
        fert_key = "Mixed (both organic and inorganic)"

    soil_desc = SOIL_DESCRIPTIONS.get(soil_type, "Good agricultural soil")

    fert_advice = FERTILIZER_RECOMMENDATIONS.get(soil_type, {}).get(
        fert_key,
        "Apply balanced NPK fertilizer based on soil test results."
    )

    crop_advice = CROP_SPECIFIC_ADVICE.get(crop, {}).get(
        soil_type,
        f"Standard agronomic practices for {crop} on {soil_type} soil."
    )

    return f"""
SOIL TYPE: {soil_type}
CHARACTERISTICS: {soil_desc}
CURRENT METHOD: {fert_key}

FERTILIZATION ADVICE:
{fert_advice}

CROP-SPECIFIC RECOMMENDATION FOR {crop.upper()}:
{crop_advice}
""".strip()


def get_soil_type_description(soil_type: str) -> str:
    return SOIL_DESCRIPTIONS.get(soil_type.title(), "")
