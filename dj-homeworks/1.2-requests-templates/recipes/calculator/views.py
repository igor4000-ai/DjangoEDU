from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}


def recipe_view(request, dish_name):
    """
    View-функция для отображения рецепта.
    Принимает название блюда из URL и опциональный параметр servings.
    """
    # Получаем рецепт из DATA
    recipe = DATA.get(dish_name, {})

    # Получаем количество порций из GET-параметра (по умолчанию 1)
    servings_str = request.GET.get('servings')

    # Конвертируем в число, если параметр передан
    try:
        servings = int(servings_str) if servings_str else 1
        if servings < 1:
            servings = 1  # Защита от отрицательных чисел
    except ValueError:
        servings = 1  # Если передано не число, используем 1

    # Если рецепт найден, умножаем ингредиенты на количество порций
    if recipe:
        # Создаем новый словарь с умноженными значениями
        scaled_recipe = {
            ingredient: amount * servings
            for ingredient, amount in recipe.items()
        }
    else:
        scaled_recipe = {}

    # Формируем контекст для шаблона
    context = {
        'recipe': scaled_recipe,
        'dish_name': dish_name,
        'servings': servings,
    }

    # Рендерим шаблон
    return render(request, 'calculator/recipe.html', context)




# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
