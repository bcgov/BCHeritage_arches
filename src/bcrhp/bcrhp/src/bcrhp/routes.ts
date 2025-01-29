export const routes = [
    {
        path: "/bcrhp/workflows/",
        name: "root",
        component: () => import("@/bcrhp/pages/HomePage.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuthentication: true,
        },
    },
    {
        path: "/bc-fossil-management/ipa_workflows/",
        name: "ipaWorkflows",
        component: () => import("@/bcrhp/pages/IpaWorkflows.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuthentication: true,
        },
    },
    {
        path: "/bc-fossil-management/ipa_submit/",
        name: "ipaSubmit",
        component: () => import("@/bcrhp/pages/ipa/IpaSubmit.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuthentication: true,
        },
    },
    // {
    //     path: "/login/:next?",
    //     name: "login",
    //     component: () => import("@/bcrhp/pages/LoginPage.vue"),
    //     meta: {
    //         shouldShowNavigation: false,
    //         requiresAuthentication: false,
    //     },
    // },
    // {
    //     path: "/advanced-search",
    //     name: "advanced-search",
    //     component: () => import("@/bcrhp/pages/AdvancedSearch.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
    // {
    //     path: "/schemes",
    //     name: "schemes",
    //     component: () => import("@/bcrhp/pages/SchemeList.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
    // {
    //     path: "/concept/:id",
    //     name: "concept",
    //     component: () =>
    //         import("@/bcrhp/pages/ConceptOrSchemeSplitter.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
    // {
    //     path: "/scheme/:id",
    //     name: "scheme",
    //     component: () =>
    //         import("@/bcrhp/pages/ConceptOrSchemeSplitter.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
];

export const routeNames = {
    root: "root",
    login: "login",
    ipaWorkflows: "ipaWorkflows",
    ipaSubmit: "ipaSubmit",
    // search: "search",
    // advancedSearch: "advanced-search",
    // schemes: "schemes",
    // concept: "concept",
    // scheme: "scheme",
};
