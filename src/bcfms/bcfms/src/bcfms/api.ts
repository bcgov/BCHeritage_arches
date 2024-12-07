import arches from "arches";
import Cookies from "js-cookie";

function getToken() {
    const token = Cookies.get("csrftoken");
    if (!token) {
        throw new Error("Missing csrftoken");
    }
    return token;
}

export const login = async (username: string, password: string) => {
    const response = await fetch(arches.urls.api_login, {
        method: "POST",
        headers: { "X-CSRFTOKEN": getToken() },
        body: JSON.stringify({ username, password }),
    });
    const parsed = await response.json();
    if (!response.ok) throw new Error(parsed.message || response.statusText);
    return parsed;
};

export const logout = async () => {
    const response = await fetch(arches.urls.api_logout, {
        method: "POST",
        headers: { "X-CSRFTOKEN": getToken() },
    });
    if (response.ok) return true;
    const parsedError = await response.json();
    throw new Error(parsedError.message || response.statusText);
};

export const fetchUser = async () => {
    console.log(arches.urls);
    const response = await fetch(arches.urls.api_user);
    const parsed = await response.json();
    if (!response.ok) throw new Error(parsed.message || response.statusText);
    return parsed;
};

export const fetchSearchResults = async (
    searchTerm: string,
    items: number,
    page: number,
) => {
    const params = new URLSearchParams({
        term: searchTerm,
        items: items.toString(),
        page: page.toString(),
    });

    const url = `${arches.urls.api_search}?${params.toString()}`;
    const response = await fetch(url);
    const parsed = await response.json();
    if (!response.ok) throw new Error(parsed.message || response.statusText);
    return parsed;
};

export const fetchConcepts = async () => {
    const response = await fetch(arches.urls.api_concepts);
    const parsed = await response.json();
    if (!response.ok) throw new Error(parsed.message || response.statusText);
    return parsed;
};
