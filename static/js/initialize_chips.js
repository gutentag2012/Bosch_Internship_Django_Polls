document.addEventListener('DOMContentLoaded', () => {
    const [chip_holder] = document.getElementsByClassName("chips")
    let chip_count = 0;

    const elems = document.querySelectorAll('.chips');
    const [instance] = M.Chips.init(elems, {
        autocompleteOptions: {
            data: all_tags,
            limit: Infinity,
            minLength: 1
        },
        onChipAdd: (input, chip) => {
            chip_count++;
            const value = chip.innerText.split("\n")[0]
            const hidden_input = document.createElement("input")
            hidden_input.setAttribute("type", "hidden")
            hidden_input.setAttribute("name", `chip-${chip_holder.childElementCount}`)
            hidden_input.setAttribute("value", `${value}`)
            chip.appendChild(hidden_input)
        },
        onChipDelete: () => {
            chip_count--;
        }
    });

    for (let key in json_tags) {
        instance.addChip(json_tags[key])
    }

    const [create_input] = chip_holder.getElementsByClassName("input")
    const label = document.createElement("label")
    label.setAttribute("for", create_input.getAttribute("id"))
    label.innerText = "Tags"
    chip_holder.appendChild(label)
    create_input.addEventListener("focus", () => {
        label.setAttribute("class", "active")
    })
    create_input.addEventListener("blur", () => {
        if (chip_count === 0 && !create_input.value)
            label.setAttribute("class", "")
    })
    if (chip_count > 0) {
        label.setAttribute("class", "active")
    }

    create_final_chip = () => {
        if (create_input.value) {
            instance.addChip({tag: create_input.value})
            create_input.value = ""
        }
    }
});