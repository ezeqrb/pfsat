document.addEventListener("DOMContentLoaded", () => {
    const createBlankForm = document.querySelector("#create-blank-form")
    createBlankForm && createBlankForm?.addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/form/create', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({
                title: "Encuesta Nueva"
            })
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/form/${result.code}/edit`
        })
    })
    const createContactForm = document.querySelector("#create-contact-form")
    createContactForm && createContactForm?.addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/form/create/contact', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/form/${result.code}/edit`
        })
    })
    const createCustomerFeedback = document.querySelector("#create-customer-feedback")
    createCustomerFeedback && createCustomerFeedback?.addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/form/create/feedback', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/form/${result.code}/edit`
        })
    })
    const createEventRegistration = document.querySelector("#create-event-registration")
    createEventRegistration && createEventRegistration?.addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/form/create/event', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/form/${result.code}/edit`
        })
    })
})