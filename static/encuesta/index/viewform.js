document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#textarea-adjust").forEach(tx => {
        tx.style.height = "auto";
        tx.style.height = (10 + tx.scrollHeight)+"px";
        tx.addEventListener('input', e => {
            tx.style.height = "auto";
            tx.style.height = (10 + tx.scrollHeight)+"px";
        })
    })
    document.querySelectorAll('.multiple-choice input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener("input", function(){
            let selectedChoices = [];
            document.querySelectorAll(`.multiple-choice input[type="checkbox"]:checked`).forEach(checkedCheckbox => {
                selectedChoices.push(checkedCheckbox.value);
            });
    
            if (selectedChoices.length > 0) {
                document.querySelectorAll(`.multiple-choice input[type="checkbox"]`).forEach(checkbox => {
                    checkbox.removeAttribute("required");
                });
            } else {
                document.querySelectorAll(`.multiple-choice input[type="checkbox"]`).forEach(checkbox => {
                    checkbox.setAttribute("required", '');
                });
            }
        });
    });    
    document.querySelectorAll('input[type="radio"]').forEach(element => {
    document.getElementsByName(element.name).forEach(radio => {
        radio.addEventListener("change", function () {
            let anyRadioChecked = false;
            document.getElementsByName(element.name).forEach(radio => {
                if (radio.checked) {
                    anyRadioChecked = true;
                    return; 
                }
            });
            if (anyRadioChecked) {
                document.getElementsByName(element.name).forEach(radio => {
                    radio.removeAttribute("required");
                });
            } else {
                document.getElementsByName(element.name).forEach(radio => {
                    radio.setAttribute("required", "");
                });
            }
        });
    });
})})