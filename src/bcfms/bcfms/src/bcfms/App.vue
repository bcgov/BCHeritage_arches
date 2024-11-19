<script setup lang="ts">
import { provide, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useGettext } from "vue3-gettext";

import Toast from "primevue/toast";
import { useToast } from "primevue/usetoast";

import {
    ANONYMOUS,
    DEFAULT_ERROR_TOAST_LIFE,
    ENGLISH,
    ERROR,
    USER_KEY,
    selectedLanguageKey,
    systemLanguageKey,
} from "@/bcfms/constants.ts";

import { routeNames } from "@/bcfms/routes.ts";
import { fetchUser } from "@/bcfms/api.ts";
import PageHeader from "@/bcfms/components/header/PageHeader.vue";
import SideNav from "@/bcfms/components/sidenav/SideNav.vue";

import type { Ref } from "vue";
import type { Language } from "@/bcfms/types";
import type { User } from "@/bcfms/types";

const user = ref<User | null>(null);
const setUser = (userToSet: User | null) => {
    user.value = userToSet;
};
provide(USER_KEY, { user, setUser });

const selectedLanguage: Ref<Language> = ref(ENGLISH);
provide(selectedLanguageKey, selectedLanguage);
const systemLanguage = ENGLISH; // TODO: get from settings
provide(systemLanguageKey, systemLanguage);

const router = useRouter();
const route = useRoute();
const toast = useToast();
const { $gettext } = useGettext();

router.beforeEach(async (to, _from, next) => {
    try {
        let userData = await fetchUser();
        setUser(userData);

        const requiresAuthentication = to.matched.some(
            (record) => record.meta.requiresAuthentication,
        );
        if (requiresAuthentication && userData.username === ANONYMOUS) {
            throw new Error();
        } else {
            next();
        }
    } catch (error) {
        if (to.name !== routeNames.root) {
            toast.add({
                severity: ERROR,
                life: DEFAULT_ERROR_TOAST_LIFE,
                summary: $gettext("Login required."),
                detail: error instanceof Error ? error.message : undefined,
            });
        }
        next({ name: routeNames.login });
    }
});
</script>

<template>
    <main>
        <PageHeader v-if="route.meta.shouldShowNavigation" />
        <div style="display: flex; flex: auto; flex-direction: row">
            <SideNav v-if="route.meta.shouldShowNavigation" />
            <div style="flex: auto; margin-top: 50px;">
                <RouterView />
            </div>
        </div>
    </main>
    <Toast />
</template>

<style scoped>
main {
    font-family: sans-serif;
    height: 100vh;
    width: 100vw;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
}

.full-height {
  height: 100%;
}
</style>

<style>
.p-tooltip-text, .p-button-label, .p-inputtext {
  font-size: 0.8rem !important;
}
</style>
