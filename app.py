
import streamlit as st
import random

st.set_page_config(
    page_title="Personalized Recipe Studio",
    page_icon="🍲",
    layout="wide"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff8ed, #fce8d5, #fffaf4);
}
.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(120deg, #8b2e16, #e88739);
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.hero h1 {
    color: white;
    font-size: 38px;
}
.hero p {
    font-size: 17px;
}
.recipe-card {
    background: rgba(255,255,255,0.85);
    border: 1px solid #f1d6bb;
    border-radius: 15px;
    padding: 18px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------- RECIPE KNOWLEDGE --------------------

RECIPES = [
    {
        "name": "Tomato Vegetable Rice",
        "cuisine": "Indian",
        "diet": "Vegetarian",
        "time": 25,
        "difficulty": "Easy",
        "ingredients": {
            "rice": "1 cup",
            "tomato": "2 medium",
            "onion": "1 medium",
            "oil": "1 tablespoon",
            "salt": "to taste"
        },
        "steps": [
            "Wash the rice and prepare the vegetables.",
            "Heat oil in a pan and cook the chopped onion.",
            "Add tomato, salt and your preferred spices.",
            "Add rice and the appropriate amount of water.",
            "Cover and cook until the rice is tender."
        ]
    },
    {
        "name": "Potato Masala",
        "cuisine": "Indian",
        "diet": "Vegan",
        "time": 25,
        "difficulty": "Easy",
        "ingredients": {
            "potato": "3 medium",
            "onion": "1 medium",
            "tomato": "1 medium",
            "oil": "1 tablespoon",
            "salt": "to taste"
        },
        "steps": [
            "Boil the potatoes until tender and cut them.",
            "Heat oil and cook the chopped onion.",
            "Add tomato, salt and spices.",
            "Add the potatoes and mix gently.",
            "Cook for several minutes and serve hot."
        ]
    },
    {
        "name": "Vegetable Pasta",
        "cuisine": "Italian",
        "diet": "Vegetarian",
        "time": 30,
        "difficulty": "Medium",
        "ingredients": {
            "pasta": "200 g",
            "tomato": "2 medium",
            "onion": "1 medium",
            "garlic": "2 cloves",
            "oil": "1 tablespoon",
            "salt": "to taste"
        },
        "steps": [
            "Boil pasta according to its package instructions.",
            "Heat oil and cook the onion and garlic.",
            "Add chopped tomato and cook into a sauce.",
            "Add the drained pasta and mix well.",
            "Season to taste and serve."
        ]
    },
    {
        "name": "Simple Egg Rice",
        "cuisine": "Asian",
        "diet": "Non-vegetarian",
        "time": 20,
        "difficulty": "Easy",
        "ingredients": {
            "rice": "2 cups cooked",
            "egg": "2",
            "onion": "1 small",
            "oil": "1 tablespoon",
            "salt": "to taste"
        },
        "steps": [
            "Prepare cooked rice and chop the onion.",
            "Heat oil in a pan and cook the onion.",
            "Add beaten eggs and scramble until fully cooked.",
            "Add the cooked rice and mix thoroughly.",
            "Season and serve hot."
        ]
    },
    {
        "name": "Banana Oat Bowl",
        "cuisine": "International",
        "diet": "Vegetarian",
        "time": 10,
        "difficulty": "Easy",
        "ingredients": {
            "oats": "1/2 cup",
            "milk": "1 cup",
            "banana": "1",
            "honey": "1 teaspoon"
        },
        "steps": [
            "Add oats and milk to a saucepan.",
            "Cook gently until the oats soften.",
            "Slice the banana.",
            "Place the oats in a bowl and add banana.",
            "Add honey if desired and serve."
        ]
    }
]

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []

# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <h1>🍲 Personalized Recipe Studio</h1>
    <p>Your ingredients, your preferences, your next meal.</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Discover meal ideas, follow cooking instructions, "
    "save favorites and prepare your shopping list."
)

# -------------------- SIDEBAR --------------------

st.sidebar.title("⚙️ Customize Your Recipe")

ingredients_text = st.sidebar.text_input(
    "Ingredients you have",
    placeholder="rice, tomato, onion"
)

diet = st.sidebar.selectbox(
    "Food preference",
    ["Any", "Vegetarian", "Vegan", "Non-vegetarian"]
)

cuisine = st.sidebar.selectbox(
    "Cuisine",
    ["Any", "Indian", "Italian", "Asian", "International"]
)

max_time = st.sidebar.slider(
    "Maximum cooking time (minutes)",
    min_value=10,
    max_value=60,
    value=30,
    step=5
)

difficulty = st.sidebar.selectbox(
    "Cooking difficulty",
    ["Any", "Easy", "Medium"]
)

spice = st.sidebar.select_slider(
    "Spice preference",
    options=["Mild", "Medium", "Hot"],
    value="Medium"
)

servings = st.sidebar.number_input(
    "Number of servings",
    min_value=1,
    max_value=10,
    value=2
)

# -------------------- RECIPE SEARCH --------------------

def find_recipes():
    available = {
        item.strip().lower()
        for item in ingredients_text.split(",")
        if item.strip()
    }

    results = []

    for recipe in RECIPES:
        if diet != "Any":
            # A vegetarian recipe is also suitable for vegan users
            # only if its ingredients are actually vegan.
            if diet == "Vegan" and recipe["diet"] != "Vegan":
                continue
            if diet == "Vegetarian" and recipe["diet"] not in [
                "Vegetarian", "Vegan"
            ]:
                continue
            if diet == "Non-vegetarian" and recipe["diet"] != diet:
                continue

        if cuisine != "Any" and recipe["cuisine"] != cuisine:
            continue

        if recipe["time"] > max_time:
            continue

        if difficulty != "Any" and recipe["difficulty"] != difficulty:
            continue

        recipe_ingredients = set(recipe["ingredients"].keys())
        matches = available.intersection(recipe_ingredients)

        # With no ingredients entered, show all suitable recipes.
        if available and not matches:
            continue

        score = len(matches)
        results.append((score, recipe))

    results.sort(key=lambda item: item[0], reverse=True)
    return results


# -------------------- TABS --------------------

tab1, tab2, tab3 = st.tabs([
    "🍽️ Find Recipes",
    "❤️ Favorites",
    "🛒 Shopping List"
])

with tab1:
    st.subheader("Find your next meal")

    if st.button("✨ Generate My Recipes", type="primary"):
        st.session_state.generated = True

    if st.session_state.get("generated", False):
        matches = find_recipes()

        if not matches:
            st.warning(
                "No matching recipe found. Try different ingredients "
                "or relax your filters."
            )

        for score, recipe in matches:
            with st.container(border=True):
                st.subheader("🍲 " + recipe["name"])
                st.caption(
                    f'{recipe["cuisine"]} • {recipe["time"]} minutes • '
                    f'{recipe["difficulty"]} • {recipe["diet"]}'
                )

                if ingredients_text.strip():
                    st.write(f"Ingredient matches: {score}")

                with st.expander("🥕 Ingredients and quantities"):
                    for ingredient, amount in recipe["ingredients"].items():
                        st.write(f"- {ingredient.title()}: {amount}")

                with st.expander("👩‍🍳 Cooking instructions"):
                    for number, step in enumerate(recipe["steps"], 1):
                        st.write(f"{number}. {step}")

                st.write(f"Servings selected: {servings}")
                st.write(f"Spice preference: {spice}")

                if st.button(
                    "❤️ Save recipe",
                    key="save_" + recipe["name"]
                ):
                    if recipe["name"] not in st.session_state.favorites:
                        st.session_state.favorites.append(recipe["name"])
                    st.success("Recipe saved to Favorites.")

                recipe_text = (
                    f'{recipe["name"]}\n'
                    f'Cuisine: {recipe["cuisine"]}\n'
                    f'Cooking time: {recipe["time"]} minutes\n\n'
                    "Ingredients:\n"
                    + "\n".join(
                        f"- {name}: {amount}"
                        for name, amount in recipe["ingredients"].items()
                    )
                    + "\n\nInstructions:\n"
                    + "\n".join(
                        f"{i}. {step}"
                        for i, step in enumerate(recipe["steps"], 1)
                    )
                )

                st.download_button(
                    "⬇️ Download Recipe",
                    data=recipe_text,
                    file_name=recipe["name"].lower().replace(" ", "_") + ".txt",
                    mime="text/plain",
                    key="download_" + recipe["name"]
                )

                if st.button(
                    "🛒 Add ingredients to shopping list",
                    key="shop_" + recipe["name"]
                ):
                    for ingredient in recipe["ingredients"]:
                        if ingredient not in st.session_state.shopping_list:
                            st.session_state.shopping_list.append(ingredient)
                    st.success("Ingredients added to shopping list.")

with tab2:
    st.subheader("Your saved recipes")

    if not st.session_state.favorites:
        st.info("You have not saved any recipes yet.")
    else:
        for name in st.session_state.favorites:
            st.write("❤️ " + name)

        if st.button("Clear favorites"):
            st.session_state.favorites = []
            st.rerun()

with tab3:
    st.subheader("Your shopping list")

    if not st.session_state.shopping_list:
        st.info("Your shopping list is empty.")
    else:
        for item in st.session_state.shopping_list:
            st.checkbox(item.title(), key="check_" + item)

        shopping_text = "\n".join(st.session_state.shopping_list)

        st.download_button(
            "⬇️ Download Shopping List",
            data=shopping_text,
            file_name="shopping_list.txt",
            mime="text/plain"
        )

        if st.button("Clear shopping list"):
            st.session_state.shopping_list = []
            st.rerun()

# -------------------- FOOTER --------------------

st.divider()
st.caption(
    "Personalized Recipe Studio | Student Prototype | "
    "Generative AI & Agentic AI Systems"
)
