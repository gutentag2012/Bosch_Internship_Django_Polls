let id = 4

const add_input_field = () => {
    const parent = document.getElementById("new-answers")

    const outer_wrapper = document.createElement("div")
    outer_wrapper.setAttribute("class", "input-field col with-prefix full-width")
    const prefix = document.createElement("span")
    prefix.setAttribute("class", "prefix")
    const prefix_icon = document.createElement("clear")
    prefix_icon.setAttribute("class", "material-icons")
    prefix_icon.innerText = "clear"
    prefix.appendChild(prefix_icon)
    prefix.addEventListener("click", () => parent.removeChild(outer_wrapper))
    outer_wrapper.appendChild(prefix)
    const input = document.createElement("input")
    input.setAttribute("id", `answer_${id}`)
    input.setAttribute("name", `answer_${id}`)
    input.setAttribute("type", "text")
    outer_wrapper.appendChild(input)
    const label = document.createElement("label")
    label.setAttribute("for", `answer_${id}`)
    label.innerText = `Answer ${id}`
    outer_wrapper.appendChild(label)
    parent.appendChild(outer_wrapper)

    id++
}