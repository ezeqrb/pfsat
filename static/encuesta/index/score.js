document.addEventListener("DOMContentLoaded", () => {
    const csrf = Cookies.get('csrftoken');
    document.querySelectorAll("#textarea-adjust").forEach(tx => {
        tx.style.height = "auto";
        tx.style.height = (10 + tx.scrollHeight)+"px";
        tx.addEventListener('input', e => {
            tx.style.height = "auto";
            tx.style.height = (10 + tx.scrollHeight)+"px";
        })
    })
    document.querySelectorAll("#input-score").forEach(element => {
        element.addEventListener("input", function(){
            fetch('edit_score', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    question_id: this.dataset.id,
                    score: this.value
                })
            })
        })
    })
    document.querySelectorAll("[answer-key]").forEach(element => {
        element.addEventListener("input", function(event){
            event.preventDefault();
            if(this.dataset.question_type === "checkbox"){
                fetch('answer_key', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question_id": this.dataset.id,
                        "answer_key": document.querySelector(`input[name="${this.name}"]:checked`).value
                    })
                })
            }else if(this.dataset.question_type === "multiple choice"){
                answers = []
                document.getElementsByName(this.name).forEach(element => {
                    if(element.checked) answers.push(element.value)
                })
                fetch('answer_key', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question_id": this.dataset.id,
                        "answer_key": answers
                    })
                })
            }
            else{
                fetch('answer_key', {
                    method: "POST",
                    headers: {'X-CSRFToken': csrf},
                    body: JSON.stringify({
                        "question_id": this.dataset.id,
                        "answer_key": this.value
                    })
                })
            }
        })
    })
    document.getElementsByName('feedback').forEach(element => {
        element.addEventListener("input", function(){
            fetch('feedback', {
                method: "POST",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    "question_id": this.dataset.id,
                    "feedback": this.value
                })
            })
        })
    })
})