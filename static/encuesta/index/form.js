document.addEventListener("DOMContentLoaded", () => {
    const csrf = Cookies.get('csrftoken');
    document.querySelectorAll(".input-form-title").forEach(title => {
        title.addEventListener("input", function(){
            fetch(`edit_title`, {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    "title": this.value
                })

            })
            document.title = `${this.value} - Google Forms CLONE`
            document.querySelectorAll(".input-form-title").forEach(ele => {
                ele.value = this.value;
            })
        })
    })
    document.querySelector("#input-form-description").addEventListener("input", function(){
        fetch('edit_description', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({
                "description": this.value
            })
        })
    })

    document.querySelectorAll("#send-form-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelector("#send-form").style.display = "block";
        })
        document.querySelector("#close-send-form").addEventListener("click", () => {
            document.querySelector("#send-form").style.display = "none";
        })
        window.onclick = e => {
            if(e.target == document.querySelector("#send-form")) document.querySelector("#send-form").style.display = "none";
        }
    })
    document.querySelectorAll("#open-setting").forEach(ele => {
        ele.addEventListener('click', () => {
            document.querySelector("#setting").style.display = "block";
        })
        document.querySelector("#close-setting").addEventListener('click', () => {
            document.querySelector("#setting").style.display = "none";
        })
        window.onclick = e => {
            if(e.target == document.querySelector("#setting")) document.querySelector("#setting").style.display = "none";
        }
    })
    document.querySelectorAll("[copy-btn]").forEach(btn => {
        btn.addEventListener("click", () => {
            var url = document.getElementById("copy-url");
            navigator.clipboard.writeText(url.value);
        })
    })
    document.querySelector("#setting-form").addEventListener("submit", e => {
        e.preventDefault();
        fetch('edit_setting', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({
                "collect_email": document.querySelector("#collect_email").checked,
                "is_quiz": document.querySelector("#is_quiz").checked,
                "authenticated_responder": document.querySelector("#authenticated_responder").checked,
                "confirmation_message": document.querySelector("#comfirmation_message").value,
                "edit_after_submit": document.querySelector("#edit_after_submit").checked,
                "allow_view_score": document.querySelector("#allow_view_score").checked,
            })
        })
        document.querySelector("#setting").style.display = "none";
        if(!document.querySelector("#collect_email").checked){
            if(document.querySelector(".collect-email")) document.querySelector(".collect-email").parentNode.removeChild(document.querySelector(".collect-email"))
        }else{
            if(!document.querySelector(".collect-email")){
                let collect_email = document.createElement("div");
                collect_email.classList.add("collect-email")
                collect_email.classList.add("txt-clr")
                collect_email.innerHTML = `
                <div class="card card-header-actions mb-4">
                    <div class="card-header question-title">
                        Dirección de correo electrónico
                    </div>
                    <div class="card-body">
                        <input type="text" autocomplete="off" aria-label="Valid email address" disabled dir = "auto" class="require-email-edit txtColor form-control"
                        placeholder = "Ingrese su correo electrónico" />
                    </div>
                </div>
                `
                document.querySelector("#form-head").appendChild(collect_email)
            }
        }
        if(document.querySelector("#is_quiz").checked){
            if(!document.querySelector("#add-score")){
                let is_quiz = document.createElement('a')
                is_quiz.setAttribute("href", "score");
                is_quiz.setAttribute("id", "add-score");
                is_quiz.setAttribute("class","d-grid mb-3");
                is_quiz.innerHTML = `<button class = "fw-500 btn btn-primary" title = "Add score" alt = "Score icon">Agregar puntaje</button>`;
                document.querySelector(".question-score").appendChild(is_quiz)
            }
            if(!document.querySelector(".score")){
                let quiz_nav = document.createElement("span");
                quiz_nav.classList.add("col-4");
                quiz_nav.classList.add("navigation");
                quiz_nav.classList.add('score');
                quiz_nav.innerHTML =   `<a href = "score" class="link">Scores</a>`;
                [...document.querySelector(".form-navigation").children].forEach(element => {
                    element.classList.remove("col-6")
                    element.classList.add('col-4')
                })
                document.querySelector(".form-navigation").insertBefore(quiz_nav, document.querySelector(".form-navigation").childNodes[2])
            }
        }else{
            if(document.querySelector("#add-score")) document.querySelector("#add-score").parentNode.removeChild(document.querySelector("#add-score"))
            if(document.querySelector(".score")){
                [...document.querySelector(".form-navigation").children].forEach(element => {
                    element.classList.remove("col-4")
                    element.classList.add('col-6')
                })
                document.querySelector(".score").parentNode.removeChild(document.querySelector(".score"))
            }
        }
    })
    document.querySelector("#delete-form").addEventListener("submit", e => {
        e.preventDefault();
        if(window.confirm("¿Está seguro que desea eliminar la encuesta? Debe tener en cuenta que no podrá volver atrás...")){
            fetch('delete', {
                method: "DELETE",
                headers: {'X-CSRFToken': csrf}
            })
            .then(() => window.location = "list_encuestas")
        }
    })
    const editQuestion = () => {
        document.querySelectorAll(".input-question").forEach(question => {
            question.addEventListener('input', function(){
                let question_type;
                let required;
                document.querySelectorAll(".input-question-type").forEach(qp => {
                    if(qp.dataset.id === this.dataset.id) question_type = qp.value
                })
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) required = rc.checked;
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: this.value,
                        question_type: question_type,
                        required: required
                    })
                })
            })
        })
    }
    editQuestion();
    
    const editRequire = () => {
        document.querySelectorAll(".required-checkbox").forEach(checkbox => {
            checkbox.addEventListener('input', function(){
                let question;
                let question_type;
                document.querySelectorAll(".input-question-type").forEach(qp => {
                    if(qp.dataset.id === this.dataset.id) question_type = qp.value
                })
                document.querySelectorAll('.input-question').forEach(q => {
                    if(q.dataset.id === this.dataset.id) question = q.value
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: question,
                        question_type: question_type,
                        required: this.checked
                    })
                })
            })
        })
    }
    editRequire()
    const editChoice = () => {
        document.querySelectorAll(".edit-choice").forEach(choice => {
            choice.addEventListener("input", function(){
                fetch('edit_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id,
                        "choice": this.value
                    })
                })
            })
        })
    }
    editChoice()
    const removeOption = () => {
        document.querySelectorAll(".remove-option").forEach(ele => {
            ele.addEventListener("click",function(){
                fetch('remove_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "id": this.dataset.id
                    })
                })
                .then(() => {
                    this.parentNode.parentNode.removeChild(this.parentNode)
                })
            })
        })
    }
    removeOption()
    const addOption = () => {
        document.querySelectorAll(".add-option").forEach(question =>{
            question.addEventListener("click", function(){
                fetch('add_choice', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question": this.dataset.question
                    })
                })
                .then(response => response.json())
                .then(result => {
                    let element = document.createElement("div");
                    element.classList.add('choice');
                    if(this.dataset.type === "checkbox"){
                        element.innerHTML = `<input type="radio" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="edit-choice form-control" style="margin-bottom: .5rem" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Eliminar Opción" data-id="${result["id"]}">&times;</span>`;
                    }else if(this.dataset.type === "multiple choice"){
                        element.innerHTML = `<input type="checkbox" id="${result["id"]}" disabled>
                        <label for="${result["id"]}">
                            <input type="text" value="${result["choice"]}" class="edit-choice form-control" style="margin-bottom: .5rem" data-id="${result["id"]}">
                        </label>
                        <span class="remove-option" title = "Eliminar Opción" data-id="${result["id"]}">&times;</span>`;
                    }
                    document.querySelectorAll(".choices").forEach(choices => {
                        if(choices.dataset.id === this.dataset.question){
                            choices.insertBefore(element, choices.childNodes[choices.childNodes.length -2]);
                            editChoice()
                            removeOption()
                        }
                    });
                })
            })
        })
    }
    addOption()
    const deleteQuestion = () => {
        document.querySelectorAll(".delete-question").forEach(question => {
            question.addEventListener("click", function(){
                fetch(`delete_question/${this.dataset.id}`, {
                    method: "DELETE",
                    headers: {'X-CSRFToken': csrf},
                })
                .then(() => {
                    document.querySelectorAll(".question").forEach(q =>{
                        if(q.dataset.id === this.dataset.id){
                            q.parentNode.removeChild(q)
                        }
                    })
                })
            })
        })
    }
    deleteQuestion()

    // Función para agregar una pregunta clonada
    const addRepeatedQuestion = () => {
        document.querySelectorAll(".repeat-question").forEach(question => {
            question.addEventListener("click", function(){
                fetch(`repeat_question/${this.dataset.id}`, {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result)
                    let ele = document.createElement('div');
                    ele.classList.add('margin-top-bottom');
                    ele.classList.add('box');
                    ele.classList.add('question-box');
                    ele.classList.add('question');
                    ele.setAttribute("data-id", result["question"].id)
                    ele.innerHTML = `
                    <div class="card card-header-actions mb-4">
                        <div class="card-body">
                            <input type="text" data-id="${result["question"].id}" class="form-control question-title edit-on-click input-question" style="margin-bottom: .5rem;" value="${result["question"].question}">
                            <select class="form-control question-type-select input-question-type" style="margin-bottom: 1rem;" data-id="${result["question"].id}" data-origin_type = "${result["question"].question_type}">
                                <option value="short">Respuesta Breve</option>
                                <option value="paragraph">Respuesta a Desarrollar</option>
                                <option value="multiple choice" selected>Opción Múltiple</option>
                                <option value="checkbox">Opción Única</option>
                            </select>
                            <div class="choices" data-id="${result["question"].id}">
                                ${result["choices"].map(choice => `
                                    <div class="choice">
                                        <input type="checkbox" id="${choice.id}" disabled>
                                        <label for="${choice.id}">
                                            <input type="text" value="${choice.choice}" class="edit-choice form-control mb-1" data-id="${choice.id}">
                                        </label>
                                        <span class="remove-option" title="Eliminar Opción" data-id="${choice.id}">&times;</span>
                                    </div>
                                `).join('')}
                                <div class="choice">
                                    <a for="add-choice" class="add-option" id="add-option" data-question="${result["question"].id}" 
                                    data-type="${result["question"].question_type}">+ Agregar Opción</a>
                                </div>
                            </div>
                            <div class="choice-option">
                                <input type="checkbox" class="required-checkbox" id="${result["question"].id}" data-id="${result["question"].id}">
                                <label for="${result["question"].id}" class="required mt-2">(*) Obligatoria</label>
                                <div class="text-center">
                                    <button class="question-option-icon delete-question btn btn-dark btn-sm" data-id="${result["question"].id}">Eliminar Pregunta</button>
                                    <button class="question-option-icon repeat-question btn btn-dark btn-sm" data-id="${result["question"].id}">Repetir Pregunta</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    `;

                    document.querySelector(".container").insertBefore(ele, document.querySelector(".repeated-questions-container"));

                    // Realiza las configuraciones necesarias para los elementos clonados
                    editChoice();
                    removeOption();
                    changeType();
                    editQuestion();
                    editRequire();
                    addOption();
                    deleteQuestion();
                })
            })
        })
    }
    addRepeatedQuestion()


    const changeType = () => {
        document.querySelectorAll(".input-question-type").forEach(ele => {
            ele.addEventListener('input', function(){
                let required;
                let question;
                document.querySelectorAll('.required-checkbox').forEach(rc => {
                    if(rc.dataset.id === this.dataset.id) required = rc.checked;
                })
                document.querySelectorAll('.input-question').forEach(q => {
                    if(q.dataset.id === this.dataset.id) question = q.value
                })
                fetch('edit_question', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        id: this.dataset.id,
                        question: question,
                        question_type: this.value,
                        required: required
                    })
                })

                if(this.dataset.origin_type === "multiple choice" || this.dataset.origin_type === "checkbox"){
                    document.querySelectorAll(".choices").forEach(choicesElement => {
                        if(choicesElement.dataset.id === this.dataset.id){
                            if(this.value === "multiple choice" || this.value === "checkbox"){
                                fetch(`get_choice/${this.dataset.id}`, {
                                    method: "GET"
                                })
                                .then(response => response.json())
                                .then(result => {
                                    let ele = document.createElement("div");
                                    ele.classList.add('choices');
                                    ele.setAttribute("data-id", result["question_id"])
                                    let choices = '';
                                    if(this.value === "checkbox"){
                                        for(let i in result["choices"]){
                                            if(i){ choices += `<div class="choice">
                                            <input type="checkbox" id="${result["choices"][i].id}" disabled>
                                            <label for="${result["choices"][i].id}">
                                                <input type="text" data-id="${result["choices"][i].id}" class="edit-choice form-control" style="margin-bottom: .5rem;" value="${result["choices"][i].choice}">
                                            </label>
                                            <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                        }
                                    }else if(this.value === "multiple choice"){
                                        for(let i in result["choices"]){
                                            if(i){choices += `<div class="choice">
                                            <input type="radio" id="${result["choices"][i].id}" disabled>
                                            <label for="${result["choices"][i].id}">
                                                <input type="text" data-id="${result["choices"][i].id}" class="edit-choice form-control" style="margin-bottom: .5rem;" value="${result["choices"][i].choice}">
                                            </label>
                                            <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                        }
                                    }
                                    ele.innerHTML = `<div class="choice">${choices}</div>
                                    <div class="choice">
                                        <label for = "add-choice" class="add-option" id="add-option" data-question="${result["question_id"]}"
                                        data-type = "${this.value}">Agregar opcion</label>
                                    </div>`;
                                    choicesElement.parentNode.replaceChild(ele, choicesElement);
                                    editChoice()
                                    removeOption()
                                    changeType()
                                    editQuestion()
                                    editRequire()
                                    addOption()
                                    deleteQuestion()
                                })
                            }else{
                                if(this.value === "short"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                    <input type ="text" class="short-answer" disabled placeholder="Ingrese una respuesta breve" />
                                </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }else if(this.value === "paragraph"){
                                    choicesElement.parentNode.removeChild(choicesElement)
                                    let ele = document.createElement("div");
                                    ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                    <textarea class="long-answer" disabled placeholder="Ingrese una respuesta a desarrollar" ></textarea>
                                </div>`
                                    this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                                }
                            }
                        }
                    })
                }else{
                    document.querySelectorAll(".question-box").forEach(question => {
                        document.querySelectorAll(".answers").forEach(answer => {
                            if(answer.dataset.id === this.dataset.id){
                                answer.parentNode.removeChild(answer)
                            }
                        })
                        if((this.value === "multiple choice" || this.value === "checkbox") && question.dataset.id === this.dataset.id){
                            fetch(`get_choice/${this.dataset.id}`, {
                                method: "GET"
                            })
                            .then(response => response.json())
                            .then(result => {
                                let ele = document.createElement("div");
                                ele.classList.add('choices');
                                ele.setAttribute("data-id", result["question_id"])
                                let choices = '';
                                if(this.value === "checkbox"){
                                    for(let i in result["choices"]){
                                        if(i){ choices += `<div class="choice">
                                        <input type="checkbox" id="${result["choices"][i].id}" disabled>
                                        <label for="${result["choices"][i].id}">
                                            <input type="text" data-id="${result["choices"][i].id}" class="edit-choice form-control" value="${result["choices"][i].choice}">
                                        </label>
                                        <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                    }
                                }else if(this.value === "multiple choice"){
                                    for(let i in result["choices"]){
                                        if(i){choices += `<div class="choice">
                                        <input type="radio" id="${result["choices"][i].id}" disabled>
                                        <label for="${result["choices"][i].id}">
                                            <input type="text" data-id="${result["choices"][i].id}" class="edit-choice form-control" style="margin-bottom: .5rem" value="${result["choices"][i].choice}">
                                        </label>
                                        <span class="remove-option" title="Remove" data-id="${result["choices"][i].id}">&times;</span></div>`}
                                    }
                                }
                                ele.innerHTML = `<div class="choice">${choices}</div>
                                <div class="choice">
                                    <input type = "radio" id = "add-choice" disabled />
                                    <label for = "add-choice" class="add-option form-control" id="add-option" data-question="${result["question_id"]}"
                                    data-type = "${this.value}">Add option</label>
                                </div>`;
                                question.insertBefore(ele, question.childNodes[4])
                                editChoice()
                                removeOption()
                                changeType()
                                editQuestion()
                                editRequire()
                                addOption()
                                deleteQuestion()
                            })
                        }else{
                            if(this.value === "short"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <input type ="text" class="short-answer" disabled placeholder="Ingrese una respuesta breve" />
                            </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }else if(this.value === "paragraph"){
                                let ele = document.createElement("div");
                                ele.innerHTML = `<div class="answers" data-id="${this.dataset.id}">
                                <textarea class="long-answer" disabled placeholder="Ingrese una respuesta a desarrollar" ></textarea>
                            </div>`
                                this.parentNode.insertBefore(ele, this.parentNode.childNodes[4])
                            }
                        }
                    })
                }
                this.setAttribute("data-origin_type", this.value);
            })
        })
    }
    changeType()
    document.querySelector("#add-question").addEventListener("click", () => {
        fetch('add_question', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            let ele = document.createElement('div')
            ele.classList.add('margin-top-bottom');
            ele.classList.add('box');
            ele.classList.add('question-box');
            ele.classList.add('question');
            ele.setAttribute("data-id", result["question"].id)
            ele.innerHTML = `
            <div class="card card-header-actions mb-4">
                <div class="card-body">
                    <input type="text" data-id="${result["question"].id}" class="form-control question-title edit-on-click input-question" style="margin-bottom: .5rem;" value="${result["question"].question}">
                    <select class="form-control question-type-select input-question-type" style="margin-bottom: 1rem;" data-id="${result["question"].id}" data-origin_type = "${result["question"].question_type}">
                        <option value="short">Respuesta Breve</option>
                        <option value="paragraph">Respuesta a Desarrollar</option>
                        <option value="checkbox" selected>Opción Múltiple</option>
                        <option value="multiple choice">Opción Única</option>
                    </select>
                    <div class="choices" data-id="${result["question"].id}">
                        <div class="choice">
                            <input type="checkbox" id="${result["choices"].id}" disabled>
                            <label for="${result["choices"].id}">
                                <input type="text" value="${result["choices"].choice}" class="edit-choice form-control mb-1" data-id="${result["choices"].id}">
                            </label>
                            <span class="remove-option" title = "Eliminar Opción" data-id="${result["choices"].id}">&times;</span>
                        </div>
                        <div class="choice">
                            <a for = "add-choice" class="add-option" id="add-option" data-question="${result["question"].id}" 
                            data-type = "${result["question"].question_type}">+ Agregar Opción</a>
                        </div>
                    </div>
                    <div class="choice-option">
                        <input type="checkbox" class="required-checkbox" id="${result["question"].id}" data-id="${result["question"].id}">
                        <label for="${result["question"].id}" class="required mt-2">(*) Obligatoria</label>
                        <div class="text-center">
                            <button class="question-option-icon delete-question btn btn-dark btn-sm" data-id="${result["question"].id}">Eliminar Pregunta</button>
                            <button class="question-option-icon repeat-question btn btn-dark btn-sm" data-id="${result["question"].id}">Repetir Pregunta</button>
                        </div>
                    </div>
                </div>
            </div>
            `;
            document.querySelector(".container").appendChild(ele);
            editChoice()
            removeOption()
            changeType()
            editQuestion()
            editRequire()
            addOption()
            deleteQuestion()
        })
    })
})