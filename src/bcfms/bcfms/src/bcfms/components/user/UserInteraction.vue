<script setup lang="ts">
import { computed, inject } from "vue";
// import { useRouter } from "vue-router";
import { useGettext } from "vue3-gettext";
import arches from "arches";

// import { useToast } from "primevue/usetoast";
// import { logout } from "@/bcfms/api.ts";

import {
    // DEFAULT_ERROR_TOAST_LIFE,
    // ERROR,
    USER_KEY,
} from "@/bcfms/constants.ts";
// import { routeNames } from "@/bcfms/routes.ts";

import type { UserRefAndSetter } from "@/bcfms/types.ts";

const { $gettext } = useGettext();
// const toast = useToast();
// const router = useRouter();

const { user } = inject(USER_KEY) as UserRefAndSetter;

// const issueLogout = async () => {
//     try {
//         await logout();
//         router.push({ name: routeNames.login });
//     } catch (error) {
//         toast.add({
//             severity: ERROR,
//             life: DEFAULT_ERROR_TOAST_LIFE,
//             summary: $gettext("Sign out failed."),
//             detail: error instanceof Error ? error.message : undefined,
//         });
//     }
// };

// const loginUrl = computed(() => {return arches.urls.user_profile_manager;});
const greeting = computed(() => {
    if (!user.value) {
        return "";
    }
    if (user.value.first_name && user.value.last_name) {
        return $gettext("Hello %{first} %{last}", {
            first: user.value.first_name,
            last: user.value.last_name,
        });
    } else {
        return $gettext("Hello %{username}", { username: user.value.username });
    }
});
</script>

<template>
    <div class="header-link">
        <span v-if="user">
                      <router-link
                          target="_blank"
                          :to="arches.urls.user_profile_manager"
                          style="text-decoration: none; color: inherit"
                      >
                          {{ greeting }}
                      </router-link>
        </span>
<!--        <Button-->
<!--            style="margin-left: 1rem"-->
<!--            @click="issueLogout"-->
<!--        >-->
<!--            {{ $gettext("Sign out") }}-->
<!--        </Button>-->
    </div>
</template>

<style scoped>
.header-link {
  font-size: .61rem !important;
}



</style>
<style>


</style>