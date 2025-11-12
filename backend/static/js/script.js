function filterCategory(cat) {
    let cards = document.querySelectorAll('.product-card');
    cards.forEach(c => {
        if(cat === 'All' || c.dataset.category === cat) {
            c.classList.remove('hidden');
        } else {
            c.classList.add('hidden');
        }
    });
}

