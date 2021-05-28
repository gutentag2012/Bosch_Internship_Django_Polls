const answer_form = document.getElementById("answer_form")

function submitAnswer(answer_id) {
    post({"vote": answer_id})
}

function post(params) {
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];

            answer_form.appendChild(hiddenField);
        }
    }
    answer_form.submit();
}