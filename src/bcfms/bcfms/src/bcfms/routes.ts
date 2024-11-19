export const routes = [
    {
        path: "/bc-fossil-management/workflows/",
        name: "root",
        component: () => import("@/bcfms/pages/HomePage.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuthentication: true,
        },
    },
    {
        path: "/bc-fossil-management/ipa_workflows/",
        name: "ipaWorkflows",
        component: () => import("@/bcfms/pages/IpaWorkflows.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuthentication: true,
        },
    },
    {
        path: "/bc-fossil-management/ipa_submit/",
        name: "ipaSubmit",
        component: () => import("@/bcfms/pages/ipa/IpaSubmit.vue"),
        meta: {
            shouldShowNavigation: true,
            requiresAuthentication: true,
        },
    },
    // {
    //     path: "/login/:next?",
    //     name: "login",
    //     component: () => import("@/bcfms/pages/LoginPage.vue"),
    //     meta: {
    //         shouldShowNavigation: false,
    //         requiresAuthentication: false,
    //     },
    // },
    // {
    //     path: "/advanced-search",
    //     name: "advanced-search",
    //     component: () => import("@/bcfms/pages/AdvancedSearch.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
    // {
    //     path: "/schemes",
    //     name: "schemes",
    //     component: () => import("@/bcfms/pages/SchemeList.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
    // {
    //     path: "/concept/:id",
    //     name: "concept",
    //     component: () =>
    //         import("@/bcfms/pages/ConceptOrSchemeSplitter.vue"),
    //     meta: {
    //         shouldShowNavigation: true,
    //         requiresAuthentication: true,
    //     },
    // },
    // {
    //     path: "/scheme/:id",
    //     name: "scheme",
    //     component: () =>
    //         import("@/bcfms/pages/ConceptOrSchemeSplitter.vue"),
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
