function submitForm(id) {
    let form = document.getElementById(id);
    form.submit();
}

function deletSearch() {
    let search = document.getElementById('search');
    search.value = ''
    submitForm('form_search')
}

function sendSearch() {
    submitForm('form_search')
}