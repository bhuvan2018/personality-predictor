from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Sample dataset
# Format: [Color, Theme]
X = [
    ["Red", "Abstract"],
    ["Blue", "Nature"],
    ["Yellow", "People"],
    ["Black", "Tech"],
    ["Green", "Nature"],
    ["Purple", "Abstract"],
    ["Orange", "People"],
    ["Grey", "Tech"]
]

# Labels: Personality types
y = [
    "Creative",
    "Calm",
    "Energetic",
    "Logical",
    "Grounded",
    "Imaginative",
    "Outgoing",
    "Analytical"
]

# Initialize encoders
color_encoder = LabelEncoder()
theme_encoder = LabelEncoder()

# Fit encoders and transform X
X_encoded = list(zip(
    color_encoder.fit_transform([row[0] for row in X]),
    theme_encoder.fit_transform([row[1] for row in X])
))

# Train model
clf = DecisionTreeClassifier()
clf.fit(X_encoded, y)

# Predict function
def predict_personality(color: str, theme: str) -> str:
    try:
        color_val = color_encoder.transform([color])[0]
        theme_val = theme_encoder.transform([theme])[0]
        prediction = clf.predict([[color_val, theme_val]])[0]
        return prediction
    except ValueError:
        return "Invalid input (color or theme not recognized)"
