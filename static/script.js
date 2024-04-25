let recipes = [];
let index = 0;

const get_data = (event) => {
    const ingredients = $('#ingredients').val();
    const dietary = $('#dietary').val();
    const servings = $('#servings').val();

    const vegetarian = $('#vegetarian').get().checked ? 'vegetarian': '';
    const vegan = $('#vegan').get().checked ? 'vegan': '';
    const low_carbs = $('#low-carbs').get().checked ? 'low-carbs': '';
    const gluten_free = $('#gluten-free').get().checked ? 'gluten-free': '';

    let preferences = [dietary, vegetarian, vegan, low_carbs, gluten_free]
    preferences = preferences.filter(e => e !== '').join(", ");

    const counts = 1;
    let request = {
        ingredients,
        servings,
        preferences,
        counts
    }

    console.log('sending...');
    $('.recipe').text('Hmm.. okay! Cooking up some ideas');
    const periodic = setInterval(() => {
        $('.recipe').text($('.recipe').text() + ".");
    }, 3000);
    fetch('/submit', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(request)
    })
    .then(res => res.json())
    .then(data => {
        recipes = data;
        index = 0;
        clearInterval(periodic);
        $('.recipe').text(recipes[index++]);
        $('.retry').removeClass('hidden')

        request.counts = 4;
        fetch('/submit', {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request)
        })
        .then(res => res.json())
        .then(data => {
            recipes = data;
            index = 0;
        })
    });
};

$('#action').on('click', get_data);

$('.retry').on('click', event => {
    if (index >= recipes.length) {
        $('.retry').addClass('hidden')
        get_data();
        return;
    }

    $('.recipe').text(recipes[index++]);
})


