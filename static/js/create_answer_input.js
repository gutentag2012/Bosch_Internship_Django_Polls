let id = -1

const remove_input_field = id => {
    const parent = document.getElementById("new-answers")
    const field = document.getElementById(id)
    console.log(id, field)
    parent.removeChild(field)
}

const add_input_field = () => {
    const parent = document.getElementById("new-answers")

    if(id === -1){
        id = parent.childElementCount + 4
    }
    const parent_id = `parent_${id}`
    const answer_id = `answer_${id}`

    const outer_wrapper = document.createElement("div")
    outer_wrapper.setAttribute("class", "input-field col with-prefix full-width")
    outer_wrapper.setAttribute("id", parent_id)
    const prefix = document.createElement("span")
    prefix.setAttribute("class", "prefix")
    const prefix_icon = document.createElement("clear")
    prefix_icon.setAttribute("class", "material-icons")
    prefix_icon.innerText = "clear"
    prefix.appendChild(prefix_icon)
    prefix.addEventListener("click", () => remove_input_field(parent_id))
    outer_wrapper.appendChild(prefix)
    const input = document.createElement("input")
    input.setAttribute("id", answer_id)
    input.setAttribute("name", answer_id)
    input.setAttribute("type", "text")
    outer_wrapper.appendChild(input)
    const label = document.createElement("label")
    label.setAttribute("for", answer_id)
    label.innerText = `Answer ${id}`
    outer_wrapper.appendChild(label)
    parent.appendChild(outer_wrapper)

    id++
}