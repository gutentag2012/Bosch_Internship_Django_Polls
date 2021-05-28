const get_cookie = (name) => {
    name += '='
    const cookies = decodeURIComponent(document.cookie).split('; ');
    for (let i in cookies) {
        const cookie = cookies[i]
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}

const add_cookie = (k, v) => {
    document.cookie = `${k}=${v};path=/;`
}

const change_dark_mode = (is_dark_mode) => {
    if (is_dark_mode) {
        document.documentElement.style.setProperty("--color-on-background", "#FFF")
        document.documentElement.style.setProperty("--color-surface", "#2a2a2a")
        document.documentElement.style.setProperty("--color-surface-darker", "#242424")
        document.documentElement.style.setProperty("--color-background", "#1d1d1d")
    }

    const was_dark_mode = get_cookie("dark_mode") === "true"
    if (was_dark_mode === is_dark_mode)
        return
    add_cookie("dark_mode", is_dark_mode)

    location.reload()
}

const toggle_dark_mode = () => {
    change_dark_mode(is_dark_mode = !is_dark_mode)
}

let is_dark_mode = window.matchMedia('(prefers-color-scheme: dark)').matches
if (document.cookie.includes("dark_mode=")) {
    is_dark_mode = get_cookie("dark_mode") === "true"
}

change_dark_mode(is_dark_mode)